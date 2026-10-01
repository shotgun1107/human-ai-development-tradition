#include "s0_runtime_v0_5.h"

#include <bcrypt.h>

#include <algorithm>
#include <array>
#include <cstddef>
#include <cstring>
#include <cstdio>
#include <cwchar>
#include <iterator>
#include <limits.h>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#pragma comment(lib, "bcrypt.lib")
#pragma comment(lib, "ntdll.lib")

extern "C" NTSYSAPI NTSTATUS NTAPI NtQueryObject(
    HANDLE,
    OBJECT_INFORMATION_CLASS,
    PVOID,
    ULONG,
    PULONG
);

namespace {

constexpr const char* kRuntimeManifestSha =
    "8e151f7ad7d1bd71b8e7375fce28b86e6b614814e7702a40baf1c6e7a0d95798";
constexpr const char* kMaterializationManifestSha =
    "43277a32068fef853b004d90938cf00fe1c77cccd49b6f0c6a65953bc1489f0b";
constexpr const char* kMaterializationStatusSha =
    "e4e8f870f71f0af7ec5b394eb2f07ee5be41c9aac9f351b144ff234ac5e21c25";
constexpr DWORD kCommitTimeoutMs = 30000u;

struct EvidencePin {
    const char* path;
    const char* sha256;
};

constexpr EvidencePin kBaseEvidencePins[] = {
    {"evidence/payload-manifest.json", "8e151f7ad7d1bd71b8e7375fce28b86e6b614814e7702a40baf1c6e7a0d95798"},
    {"evidence/prepublication-record.json", "0281893dce01d1aa54a1ad16cd621786615340844fcec35940095768e7dda9ca"},
    {"evidence/runtime-record.json", "5d6b61194b5a7f0e53aeb78ac0bdee40f6edea294adecb0f8a7462751f6e6a84"},
    {"evidence/status.json", "c8878e9df9d8c5979517efa3a9495b8e65c640b6f2c195fff029def6c262bbc6"}
};

struct S0ObjectBasicInformation {
    ULONG attributes;
    ACCESS_MASK granted_access;
    ULONG handle_count;
    ULONG pointer_count;
    ULONG paged_pool_charge;
    ULONG non_paged_pool_charge;
    ULONG reserved[3];
    ULONG name_information_length;
    ULONG type_information_length;
    ULONG security_descriptor_length;
    LARGE_INTEGER creation_time;
};

class Handle {
  public:
    Handle() noexcept = default;
    explicit Handle(HANDLE value) noexcept : value_(value) {}
    Handle(const Handle&) = delete;
    Handle& operator=(const Handle&) = delete;
    Handle(Handle&& other) noexcept : value_(other.release()) {}
    Handle& operator=(Handle&& other) noexcept {
        if (this != &other) reset(other.release());
        return *this;
    }
    ~Handle() { reset(); }
    HANDLE get() const noexcept { return value_; }
    HANDLE release() noexcept {
        HANDLE result = value_;
        value_ = nullptr;
        return result;
    }
    void reset(HANDLE value = nullptr) noexcept {
        if (value_ && value_ != INVALID_HANDLE_VALUE) CloseHandle(value_);
        value_ = value;
    }
    explicit operator bool() const noexcept {
        return value_ && value_ != INVALID_HANDLE_VALUE;
    }
  private:
    HANDLE value_ = nullptr;
};

struct LockedDirectory {
    Handle handle;
    FILE_ID_INFO identity{};
    std::wstring final_path;
};
class PathLocks {
    std::map<std::wstring, LockedDirectory> directories_;
    std::map<std::wstring, FILE_ID_128> enumerated_;
    static void Measure(HANDLE handle, FILE_ID_INFO& id, std::wstring& final_path) {
        FILE_ID_INFO second{}; FILE_ATTRIBUTE_TAG_INFO tag{}; FILE_STANDARD_INFO standard{};
        if (!GetFileInformationByHandleEx(handle, FileIdInfo, &id, sizeof(id)) ||
            !GetFileInformationByHandleEx(handle, FileIdInfo, &second, sizeof(second)) ||
            !GetFileInformationByHandleEx(handle, FileAttributeTagInfo, &tag, sizeof(tag)) ||
            !GetFileInformationByHandleEx(handle, FileStandardInfo, &standard, sizeof(standard)) ||
            memcmp(&id, &second, sizeof(id)) != 0 || !(tag.FileAttributes & FILE_ATTRIBUTE_DIRECTORY) ||
            (tag.FileAttributes & FILE_ATTRIBUTE_REPARSE_POINT) || standard.NumberOfLinks != 1 ||
            standard.DeletePending) throw std::runtime_error("retained directory identity");
        final_path.assign(S0_MAX_PATH_CHARS, L'\0');
        DWORD count = GetFinalPathNameByHandleW(handle, final_path.data(),
            static_cast<DWORD>(final_path.size()), FILE_NAME_NORMALIZED | VOLUME_NAME_DOS);
        if (!count || count >= final_path.size()) throw std::runtime_error("retained directory final path");
        final_path.resize(count);
    }
  public:
    HANDLE directory(const std::wstring& path) {
        auto existing = directories_.find(path);
        if (existing != directories_.end()) return existing->second.handle.get();
        if (directories_.size() >= 2048 || path.size() < 3 || path.size() > 32766 ||
            path[0] < L'A' || path[0] > L'Z' || path[1] != L':' || path[2] != L'\\')
            throw std::runtime_error("retained path bound");
        Handle handle;
        if (path.size() == 3) {
            handle.reset(CreateFileW(path.c_str(), S0_ROOT_ACCESS, FILE_SHARE_READ, nullptr,
                OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OPEN_REPARSE_POINT, nullptr));
        } else {
            size_t slash = path.rfind(L'\\');
            std::wstring name = path.substr(slash + 1);
            if (name.empty() || name == L"." || name == L".." || name.size() > 255 ||
                name.back() == L'.' || name.back() == L' ' || name.find(L':') != std::wstring::npos)
                throw std::runtime_error("retained path component");
            HANDLE parent = directory(slash == 2 ? path.substr(0, 3) : path.substr(0, slash));
            UNICODE_STRING unicode{};
            unicode.Buffer = name.data(); unicode.Length = static_cast<USHORT>(name.size() * 2);
            unicode.MaximumLength = unicode.Length;
            OBJECT_ATTRIBUTES attributes{};
            InitializeObjectAttributes(&attributes, &unicode, S0_OBJECT_ATTRIBUTES_FLAGS, parent, nullptr);
            IO_STATUS_BLOCK io{}; HANDLE raw = nullptr;
            NTSTATUS status = NtCreateFile(&raw, S0_ROOT_ACCESS, &attributes, &io, nullptr,
                FILE_ATTRIBUTE_DIRECTORY, FILE_SHARE_READ, FILE_OPEN,
                FILE_DIRECTORY_FILE | FILE_SYNCHRONOUS_IO_NONALERT | FILE_OPEN_REPARSE_POINT, nullptr, 0);
            handle.reset(raw);
            if (status != 0 || io.Status != status) throw std::runtime_error("retained relative directory");
        }
        if (!handle) throw std::runtime_error("retained directory open");
        LockedDirectory value{}; value.handle = std::move(handle);
        Measure(value.handle.get(), value.identity, value.final_path);
        if (value.final_path != L"\\\\?\\" + path) throw std::runtime_error("retained directory name rebound");
        auto inserted = directories_.emplace(path, std::move(value));
        return inserted.first->second.handle.get();
    }
    Handle file(const std::wstring& path) {
        size_t slash = path.rfind(L'\\');
        if (slash == std::wstring::npos || slash < 2) throw std::runtime_error("retained file parent");
        HANDLE parent = directory(slash == 2 ? path.substr(0, 3) : path.substr(0, slash));
        std::wstring name = path.substr(slash + 1);
        if (name.empty() || name.size() > 255 || name == L"." || name == L".." ||
            name.back() == L'.' || name.back() == L' ' || name.find(L':') != std::wstring::npos)
            throw std::runtime_error("retained file component");
        UNICODE_STRING unicode{}; unicode.Buffer = name.data();
        unicode.Length = static_cast<USHORT>(name.size() * 2); unicode.MaximumLength = unicode.Length;
        OBJECT_ATTRIBUTES attributes{};
        InitializeObjectAttributes(&attributes, &unicode, S0_OBJECT_ATTRIBUTES_FLAGS, parent, nullptr);
        IO_STATUS_BLOCK io{}; HANDLE raw = nullptr;
        NTSTATUS status = NtCreateFile(&raw, GENERIC_READ, &attributes, &io, nullptr, FILE_ATTRIBUTE_NORMAL,
            FILE_SHARE_READ, FILE_OPEN, FILE_NON_DIRECTORY_FILE | FILE_SYNCHRONOUS_IO_NONALERT | FILE_OPEN_REPARSE_POINT,
            nullptr, 0);
        Handle result(raw);
        if (status != 0 || io.Status != status || !result) throw std::runtime_error("retained relative file");
        auto observed = enumerated_.find(path);
        if (observed != enumerated_.end()) {
            FILE_ID_INFO id{};
            if (!GetFileInformationByHandleEx(result.get(), FileIdInfo, &id, sizeof(id)) ||
                memcmp(id.FileId.Identifier, observed->second.Identifier, 16) != 0)
                throw std::runtime_error("enumerated file was rebound");
        }
        return result;
    }
    void record(const std::wstring& path, const FILE_ID_128& id) {
        auto directory = directories_.find(path);
        if (directory != directories_.end() &&
            memcmp(directory->second.identity.FileId.Identifier, id.Identifier, 16) != 0)
            throw std::runtime_error("enumerated directory rebound");
        auto prior = enumerated_.find(path);
        if (prior != enumerated_.end() && memcmp(prior->second.Identifier, id.Identifier, 16) != 0)
            throw std::runtime_error("enumerated object rebound");
        enumerated_[path] = id;
    }
    void check() const {
        for (const auto& row : directories_) {
            FILE_ID_INFO id{}; std::wstring path;
            Measure(row.second.handle.get(), id, path);
            if (memcmp(&id, &row.second.identity, sizeof(id)) != 0 || path != row.second.final_path)
                throw std::runtime_error("retained ancestry changed");
        }
    }
    void exclude(const std::wstring& output_parent, const std::vector<std::wstring>& denied_roots) {
        directory(output_parent);
        for (const auto& denied : denied_roots) directory(denied);
        for (const auto& row : directories_) {
            if (row.first != output_parent && output_parent.rfind(row.first.back() == L'\\' ?
                row.first : row.first + L"\\", 0) != 0) continue;
            for (const auto& denied : denied_roots) {
                const auto& identity = directories_.at(denied).identity;
                if (memcmp(&identity, &row.second.identity, sizeof(identity)) == 0)
                    throw std::runtime_error("physical output ancestry overlap");
            }
        }
    }
    void exact_directories(const std::wstring& root, const std::set<std::wstring>& expected) const {
        for (const auto& row : directories_)
            if ((row.first == root || row.first.rfind(root + L"\\", 0) == 0) && expected.count(row.first) == 0)
                throw std::runtime_error("unlisted runtime directory");
    }
};
PathLocks* g_path_locks = nullptr;
struct PathScope {
    PathLocks locks;
    PathScope() { if (g_path_locks) throw std::runtime_error("path transaction already active"); g_path_locks = &locks; }
    ~PathScope() { g_path_locks = nullptr; }
};

class SearchHandle {
  public:
    explicit SearchHandle(HANDLE value) noexcept : value_(value) {}
    SearchHandle(const SearchHandle&) = delete;
    SearchHandle& operator=(const SearchHandle&) = delete;
    ~SearchHandle() { if (value_ != INVALID_HANDLE_VALUE) FindClose(value_); }
    HANDLE get() const noexcept { return value_; }
  private:
    HANDLE value_;
};

class TerminateOnFailure {
  public:
    explicit TerminateOnFailure(HANDLE process) noexcept : process_(process) {}
    TerminateOnFailure(const TerminateOnFailure&) = delete;
    TerminateOnFailure& operator=(const TerminateOnFailure&) = delete;
    ~TerminateOnFailure() {
        if (active_ && process_ && process_ != INVALID_HANDLE_VALUE) {
            TerminateProcess(process_, 70);
            WaitForSingleObject(process_, 5000);
        }
    }
    void release() noexcept { active_ = false; }
  private:
    HANDLE process_;
    bool active_ = true;
};

[[noreturn]] void Fail(const char* message) { throw std::runtime_error(message); }

bool IsLowerSha(const std::string& value) {
    if (value.size() != 64) return false;
    for (char ch : value) {
        if (!((ch >= '0' && ch <= '9') || (ch >= 'a' && ch <= 'f'))) return false;
    }
    return true;
}

std::string Hex(const uint8_t* bytes, size_t count) {
    static constexpr char digits[] = "0123456789abcdef";
    std::string result(count * 2, '0');
    for (size_t index = 0; index < count; ++index) {
        result[index * 2] = digits[bytes[index] >> 4];
        result[index * 2 + 1] = digits[bytes[index] & 15];
    }
    return result;
}

S0_SHA256 HashHandle(HANDLE file) {
    LARGE_INTEGER zero{};
    if (!SetFilePointerEx(file, zero, nullptr, FILE_BEGIN)) Fail("file seek failed");
    BCRYPT_ALG_HANDLE algorithm = nullptr;
    BCRYPT_HASH_HANDLE hash = nullptr;
    DWORD object_bytes = 0, result_bytes = 0, digest_bytes = 0;
    if (BCryptOpenAlgorithmProvider(&algorithm, BCRYPT_SHA256_ALGORITHM, nullptr, 0) < 0) {
        Fail("SHA-256 provider unavailable");
    }
    if (BCryptGetProperty(algorithm, BCRYPT_OBJECT_LENGTH,
                          reinterpret_cast<PUCHAR>(&object_bytes), sizeof(object_bytes),
                          &result_bytes, 0) < 0 ||
        BCryptGetProperty(algorithm, BCRYPT_HASH_LENGTH,
                          reinterpret_cast<PUCHAR>(&digest_bytes), sizeof(digest_bytes),
                          &result_bytes, 0) < 0 || digest_bytes != 32) {
        BCryptCloseAlgorithmProvider(algorithm, 0);
        Fail("SHA-256 provider shape differs");
    }
    std::vector<uint8_t> object;
    try { object.resize(object_bytes); }
    catch (...) { BCryptCloseAlgorithmProvider(algorithm, 0); throw; }
    if (BCryptCreateHash(algorithm, &hash, object.data(), object_bytes, nullptr, 0, 0) < 0) {
        BCryptCloseAlgorithmProvider(algorithm, 0);
        Fail("SHA-256 creation failed");
    }
    std::array<uint8_t, 65536> buffer{};
    uint64_t total = 0;
    for (;;) {
        DWORD got = 0;
        if (!ReadFile(file, buffer.data(), static_cast<DWORD>(buffer.size()), &got, nullptr)) {
            BCryptDestroyHash(hash);
            BCryptCloseAlgorithmProvider(algorithm, 0);
            Fail("file hashing read failed");
        }
        if (!got) break;
        total += got;
        if (total > S0_MAX_RUNTIME_BYTES ||
            BCryptHashData(hash, buffer.data(), got, 0) < 0) {
            BCryptDestroyHash(hash);
            BCryptCloseAlgorithmProvider(algorithm, 0);
            Fail("file hashing bound or update failed");
        }
    }
    S0_SHA256 digest{};
    if (BCryptFinishHash(hash, digest.bytes, 32, 0) < 0) {
        BCryptDestroyHash(hash);
        BCryptCloseAlgorithmProvider(algorithm, 0);
        Fail("SHA-256 finish failed");
    }
    BCryptDestroyHash(hash);
    BCryptCloseAlgorithmProvider(algorithm, 0);
    if (!SetFilePointerEx(file, zero, nullptr, FILE_BEGIN)) Fail("file reset failed");
    return digest;
}

S0_SHA256 HashBytes(const std::string& bytes) {
    BCRYPT_ALG_HANDLE algorithm = nullptr;
    BCRYPT_HASH_HANDLE hash = nullptr;
    DWORD object_bytes = 0, result_bytes = 0, digest_bytes = 0;
    if (BCryptOpenAlgorithmProvider(&algorithm, BCRYPT_SHA256_ALGORITHM, nullptr, 0) < 0 ||
        BCryptGetProperty(algorithm, BCRYPT_OBJECT_LENGTH,
                          reinterpret_cast<PUCHAR>(&object_bytes), sizeof(object_bytes),
                          &result_bytes, 0) < 0 ||
        BCryptGetProperty(algorithm, BCRYPT_HASH_LENGTH,
                          reinterpret_cast<PUCHAR>(&digest_bytes), sizeof(digest_bytes),
                          &result_bytes, 0) < 0 || digest_bytes != 32) {
        if (algorithm) BCryptCloseAlgorithmProvider(algorithm, 0);
        Fail("SHA-256 byte provider failed");
    }
    std::vector<uint8_t> object;
    try { object.resize(object_bytes); }
    catch (...) { BCryptCloseAlgorithmProvider(algorithm, 0); throw; }
    if (BCryptCreateHash(algorithm, &hash, object.data(), object_bytes, nullptr, 0, 0) < 0 ||
        BCryptHashData(hash,
                       reinterpret_cast<PUCHAR>(const_cast<char*>(bytes.data())),
                       static_cast<ULONG>(bytes.size()), 0) < 0) {
        if (hash) BCryptDestroyHash(hash);
        BCryptCloseAlgorithmProvider(algorithm, 0);
        Fail("SHA-256 byte hashing failed");
    }
    S0_SHA256 digest{};
    if (BCryptFinishHash(hash, digest.bytes, 32, 0) < 0) {
        BCryptDestroyHash(hash);
        BCryptCloseAlgorithmProvider(algorithm, 0);
        Fail("SHA-256 byte finish failed");
    }
    BCryptDestroyHash(hash);
    BCryptCloseAlgorithmProvider(algorithm, 0);
    return digest;
}

std::wstring Utf8ToWide(const std::string& value) {
    if (value.empty() || value.find('\0') != std::string::npos) Fail("text is empty or NUL-bearing");
    int count = MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, value.data(),
                                    static_cast<int>(value.size()), nullptr, 0);
    if (count <= 0) Fail("text is not strict UTF-8");
    std::wstring result(static_cast<size_t>(count), L'\0');
    if (MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, value.data(),
                            static_cast<int>(value.size()), result.data(), count) != count) {
        Fail("UTF-8 conversion changed");
    }
    return result;
}

std::string WideToUtf8(const std::wstring& value) {
    int count = WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, value.data(),
                                    static_cast<int>(value.size()), nullptr, 0, nullptr, nullptr);
    if (count <= 0) Fail("wide text conversion failed");
    std::string result(static_cast<size_t>(count), '\0');
    if (WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, value.data(),
                            static_cast<int>(value.size()), result.data(), count,
                            nullptr, nullptr) != count) {
        Fail("wide text conversion changed");
    }
    return result;
}

bool IsAbsoluteDrivePath(const std::wstring& value) {
    return value.size() >= 3 &&
           ((value[0] >= L'A' && value[0] <= L'Z') || (value[0] >= L'a' && value[0] <= L'z')) &&
           value[1] == L':' && value[2] == L'\\' &&
           value.find(L'\0') == std::wstring::npos && value.size() < S0_MAX_PATH_CHARS;
}

void RequireNoReparseChain(const std::wstring& path) {
    const bool dot_tail = path.size() >= 2 && path.compare(path.size() - 2, 2, L"\\.") == 0;
    const bool dotdot_tail = path.size() >= 3 && path.compare(path.size() - 3, 3, L"\\..") == 0;
    if (!IsAbsoluteDrivePath(path) || path.find(L"\\.\\") != std::wstring::npos ||
        path.find(L"\\..\\") != std::wstring::npos || dot_tail || dotdot_tail) {
        Fail("path chain is not canonical");
    }
    wchar_t full[S0_MAX_PATH_CHARS]{};
    DWORD count = GetFullPathNameW(path.c_str(), static_cast<DWORD>(std::size(full)), full, nullptr);
    if (!count || count >= std::size(full) ||
        CompareStringOrdinal(path.c_str(), -1, full, -1, FALSE) != CSTR_EQUAL) {
        Fail("path chain full form differs");
    }
    for (size_t index = 2; index <= path.size(); ++index) {
        if (index != path.size() && path[index] != L'\\') continue;
        std::wstring component = path.substr(0, index);
        if (component.size() == 2) continue;
        DWORD attributes = GetFileAttributesW(component.c_str());
        if (attributes == INVALID_FILE_ATTRIBUTES || (attributes & FILE_ATTRIBUTE_REPARSE_POINT)) {
            Fail("path chain contains an absent or reparse component");
        }
    }
}

std::string ReadBounded(HANDLE handle, size_t maximum) {
    std::string result;
    std::array<char, 4096> buffer{};
    for (;;) {
        DWORD got = 0;
        if (!ReadFile(handle, buffer.data(), static_cast<DWORD>(buffer.size()), &got, nullptr)) {
            if (GetLastError() == ERROR_BROKEN_PIPE) break;
            Fail("bounded frame read failed");
        }
        if (!got) break;
        if (result.size() + got > maximum) Fail("bounded frame is oversized");
        result.append(buffer.data(), got);
    }
    if (result.empty() || result.back() != '\n' || result.find('\r') != std::string::npos ||
        result.find('\0') != std::string::npos) {
        Fail("bounded frame is not LF canonical text");
    }
    return result;
}

std::string ParseJsonString(const std::string& raw, size_t& cursor) {
    if (cursor >= raw.size() || raw[cursor++] != '"') Fail("JSON string is absent");
    std::string value;
    while (cursor < raw.size()) {
        unsigned char ch = static_cast<unsigned char>(raw[cursor++]);
        if (ch == '"') return value;
        if (ch < 0x20 || ch > 0x7e) Fail("JSON string is not printable ASCII");
        if (ch == '\\') {
            if (cursor >= raw.size()) Fail("JSON escape is partial");
            char escaped = raw[cursor++];
            if (escaped != '\\' && escaped != '"') Fail("JSON escape is outside exact vocabulary");
            value.push_back(escaped);
        } else {
            value.push_back(static_cast<char>(ch));
        }
    }
    Fail("JSON string is unterminated");
}

std::string EncodeJsonString(const std::string& value) {
    std::string result = "\"";
    for (unsigned char ch : value) {
        if (ch < 0x20 || ch > 0x7e) Fail("JSON value is not printable ASCII");
        if (ch == '\\' || ch == '"') result.push_back('\\');
        result.push_back(static_cast<char>(ch));
    }
    result.push_back('"');
    return result;
}

std::map<std::string, std::string> ParseFlatCanonicalJson(const std::string& raw) {
    if (raw.size() < 3 || raw.back() != '\n') Fail("control JSON framing differs");
    size_t cursor = 0;
    if (raw[cursor++] != '{') Fail("control JSON root differs");
    std::map<std::string, std::string> result;
    std::string previous;
    bool first = true;
    while (cursor < raw.size() && raw[cursor] != '}') {
        if (!first && raw[cursor++] != ',') Fail("control JSON separator differs");
        std::string key = ParseJsonString(raw, cursor);
        if (!previous.empty() && key <= previous) Fail("control JSON keys are not sorted unique");
        if (cursor >= raw.size() || raw[cursor++] != ':') Fail("control JSON key separator differs");
        std::string value = ParseJsonString(raw, cursor);
        result.emplace(key, value);
        previous = key;
        first = false;
    }
    if (cursor + 2 != raw.size() || raw[cursor] != '}' || raw[cursor + 1] != '\n') {
        Fail("control JSON has trailing or missing bytes");
    }
    std::string rebuilt = "{";
    first = true;
    for (const auto& row : result) {
        if (!first) rebuilt.push_back(',');
        rebuilt += EncodeJsonString(row.first) + ":" + EncodeJsonString(row.second);
        first = false;
    }
    rebuilt += "}\n";
    if (rebuilt != raw) Fail("control JSON is not exact canonical ASCII JSON");
    return result;
}

const std::string& Field(const std::map<std::string, std::string>& value,
                         const char* name) {
    auto it = value.find(name);
    if (it == value.end() || it->second.empty()) Fail("required control field is absent");
    return it->second;
}

uint64_t ParseDecimal(const std::string& value) {
    if (value.empty() || (value.size() > 1 && value[0] == '0')) Fail("decimal is not canonical");
    uint64_t result = 0;
    for (char ch : value) {
        if (ch < '0' || ch > '9' || result > (UINT64_MAX - static_cast<uint64_t>(ch - '0')) / 10) {
            Fail("decimal is malformed");
        }
        result = result * 10 + static_cast<uint64_t>(ch - '0');
    }
    return result;
}

HANDLE ParseHandleArgument(const wchar_t* value) {
    constexpr wchar_t prefix[] = L"--s0-control-read=0x";
    if (!value || wcsncmp(value, prefix, 20) != 0 || wcslen(value) != 36) {
        Fail("control handle argument differs");
    }
    uint64_t number = 0;
    for (size_t index = 20; index < 36; ++index) {
        wchar_t ch = value[index];
        unsigned digit = ch >= L'0' && ch <= L'9' ? static_cast<unsigned>(ch - L'0') :
                         ch >= L'a' && ch <= L'f' ? static_cast<unsigned>(ch - L'a' + 10) : 16u;
        if (digit > 15) Fail("control handle locator differs");
        number = (number << 4) | digit;
    }
    if (!number || number == UINT64_MAX) Fail("control handle locator is a sentinel");
    return reinterpret_cast<HANDLE>(static_cast<uintptr_t>(number));
}

struct ManifestRow {
    std::string path;
    std::string sha256;
    uint64_t size = 0;
    Handle handle;
};

struct BaseRuntimeClosure {
    std::vector<ManifestRow> payload;
    std::vector<ManifestRow> evidence;
};

bool SafeVirtualPath(const std::string& value) {
    if (value.empty() || value.size() > 1024 || value.front() == '/' || value.back() == '/' ||
        value.find('\\') != std::string::npos || value.find(':') != std::string::npos ||
        value.find("//") != std::string::npos || value.find('\0') != std::string::npos) return false;
    size_t start = 0;
    while (start < value.size()) {
        size_t end = value.find('/', start);
        if (end == std::string::npos) end = value.size();
        std::string part = value.substr(start, end - start);
        if (part.empty() || part.size() > 255 || part == "." || part == ".." || part.back() == '.' || part.back() == ' ') return false;
        for (unsigned char ch : part) {
            if (!(ch >= 'A' && ch <= 'Z') && !(ch >= 'a' && ch <= 'z') &&
                !(ch >= '0' && ch <= '9') && ch != '.' && ch != '_' && ch != '-') return false;
        }
        start = end + 1;
    }
    return true;
}

bool AllowedBaseProvenance(const std::string& value) {
    static const std::set<std::string> allowed = {
        "attrs-26.1.0-py3-none-any",
        "cpython-3.12.10-embed-amd64",
        "jsonschema-4.26.0-py3-none-any",
        "jsonschema-specifications-2025.9.1-py3-none-any",
        "materializer-fixed-pth-v0.7",
        "materializer-v0.7",
        "referencing-0.37.0-py3-none-any",
        "rpds-py-2026.6.3-cp312-cp312-win_amd64",
        "typing-extensions-4.16.0-py3-none-any"
    };
    return allowed.find(value) != allowed.end();
}

std::string AsciiCaseFold(std::string value) {
    for (char& ch : value) {
        if (ch >= 'A' && ch <= 'Z') ch = static_cast<char>(ch - 'A' + 'a');
    }
    return value;
}

class BasePayloadJsonParser {
  public:
    explicit BasePayloadJsonParser(const std::string& raw) : raw_(raw) {}

    std::vector<ManifestRow> Parse() {
        Expect('{');
        Key("file_count");
        if (Unsigned() != 174) Fail("base JSON file count differs");
        Expect(',');
        Key("files");
        Expect('[');
        std::vector<ManifestRow> rows;
        std::string previous;
        std::set<std::string> casefolded;
        uint64_t total = 0;
        for (size_t index = 0; index < 174; ++index) {
            if (index) Expect(',');
            ManifestRow row = ParseRow();
            if (!SafeVirtualPath(row.path) || row.path.rfind("evidence/", 0) == 0 ||
                (!previous.empty() && row.path <= previous) ||
                !casefolded.insert(AsciiCaseFold(row.path)).second ||
                !IsLowerSha(row.sha256)) {
                Fail("base JSON payload path, order, alias, or digest differs");
            }
            if (UINT64_MAX - total < row.size) Fail("base JSON payload byte count overflows");
            total += row.size;
            previous = row.path;
            rows.push_back(std::move(row));
        }
        Expect(']');
        Expect(',');
        Key("python_stdlib_zip");
        Expect('{');
        Key("entry_count");
        if (Unsigned() == 0) Fail("base JSON stdlib entry count differs");
        Expect(',');
        Key("uncompressed_bytes");
        if (Unsigned() == 0) Fail("base JSON stdlib byte count differs");
        Expect('}');
        Expect(',');
        Key("schema_id");
        if (String() != "S0-PUBLIC-BRM-V0.7-PAYLOAD-MANIFEST-1") {
            Fail("base JSON schema differs");
        }
        Expect(',');
        Key("total_bytes");
        if (Unsigned() != 24138847ull || total != 24138847ull) {
            Fail("base JSON total bytes differ");
        }
        Expect('}');
        Expect('\n');
        if (cursor_ != raw_.size() || rows.size() != 174) {
            Fail("base JSON trailing bytes or rows differ");
        }
        return rows;
    }

  private:
    ManifestRow ParseRow() {
        Expect('{');
        Key("path");
        std::string path = String();
        Expect(',');
        Key("provenance_pin_id");
        std::string provenance = String();
        if (!AllowedBaseProvenance(provenance)) Fail("base JSON provenance pin differs");
        Expect(',');
        Key("sha256");
        std::string sha256 = String();
        Expect(',');
        Key("size");
        uint64_t size = Unsigned();
        Expect('}');
        return ManifestRow{std::move(path), std::move(sha256), size};
    }

    void Key(const char* expected) {
        if (String() != expected) {
            Fail("base JSON object key is duplicate, unknown, or outside canonical order");
        }
        Expect(':');
    }

    std::string String() {
        Expect('"');
        std::string value;
        while (cursor_ < raw_.size()) {
            unsigned char ch = static_cast<unsigned char>(raw_[cursor_++]);
            if (ch == '"') return value;
            if (ch < 0x20 || ch > 0x7e || ch == '\\') {
                Fail("base JSON string encoding differs");
            }
            value.push_back(static_cast<char>(ch));
        }
        Fail("base JSON string is partial");
    }

    uint64_t Unsigned() {
        if (cursor_ >= raw_.size() || raw_[cursor_] < '0' || raw_[cursor_] > '9') {
            Fail("base JSON unsigned integer is absent");
        }
        if (raw_[cursor_] == '0' && cursor_ + 1 < raw_.size() &&
            raw_[cursor_ + 1] >= '0' && raw_[cursor_ + 1] <= '9') {
            Fail("base JSON unsigned integer has a leading zero");
        }
        uint64_t value = 0;
        do {
            unsigned digit = static_cast<unsigned>(raw_[cursor_] - '0');
            if (value > (UINT64_MAX - digit) / 10) Fail("base JSON unsigned integer overflows");
            value = value * 10 + digit;
            ++cursor_;
        } while (cursor_ < raw_.size() && raw_[cursor_] >= '0' && raw_[cursor_] <= '9');
        return value;
    }

    void Expect(char expected) {
        if (cursor_ >= raw_.size() || raw_[cursor_++] != expected) {
            Fail("base JSON syntax, duplicate-key, or canonical-order check failed");
        }
    }

    const std::string& raw_;
    size_t cursor_ = 0;
};

std::vector<ManifestRow> ParseManifest(const std::string& raw, size_t expected) {
    std::vector<ManifestRow> rows;
    size_t start = 0;
    std::string previous;
    std::set<std::string> casefolded;
    while (start + 1 < raw.size()) {
        size_t end = raw.find('\n', start);
        if (end == std::string::npos) Fail("manifest final LF differs");
        std::string line = raw.substr(start, end - start);
        if (line.size() < 67 || line[64] != ' ' || line[65] != ' ') Fail("manifest row differs");
        std::string digest = line.substr(0, 64);
        std::string path = line.substr(66);
        if (!IsLowerSha(digest) || !SafeVirtualPath(path) || (!previous.empty() && path <= previous) ||
            !casefolded.insert(AsciiCaseFold(path)).second) {
            Fail("manifest row identity or order differs");
        }
        rows.push_back(ManifestRow{path, digest});
        previous = path;
        start = end + 1;
    }
    if (start != raw.size() || rows.size() != expected) Fail("manifest row count differs");
    return rows;
}

void RequireSingleUnnamedDataStream(HANDLE handle, bool allow_empty_directory_eof) {
    std::array<uint8_t, 65536> buffer{};
    if (!GetFileInformationByHandleEx(handle, FileStreamInfo, buffer.data(),
                                      static_cast<DWORD>(buffer.size()))) {
        DWORD error = GetLastError();
        if (allow_empty_directory_eof && (error == ERROR_HANDLE_EOF || error == ERROR_NO_MORE_FILES)) return;
        Fail("file stream inventory query failed");
    }
    size_t offset = 0, count = 0;
    for (;;) {
        if (offset > buffer.size() - offsetof(FILE_STREAM_INFO, StreamName)) Fail("stream offset bound");
        const auto* stream = reinterpret_cast<const FILE_STREAM_INFO*>(buffer.data() + offset);
        if (stream->StreamNameLength % 2 ||
            stream->StreamNameLength > buffer.size() - offset - offsetof(FILE_STREAM_INFO, StreamName))
            Fail("stream name bound");
        std::wstring name(stream->StreamName, stream->StreamNameLength / sizeof(wchar_t));
        if (name != L"::$DATA" || ++count != 1) Fail("alternate data stream rejected");
        if (!stream->NextEntryOffset) break;
        if (stream->NextEntryOffset < offsetof(FILE_STREAM_INFO, StreamName) ||
            stream->NextEntryOffset > buffer.size() - offset) Fail("stream next-entry bound");
        offset += stream->NextEntryOffset;
    }
    if (count != 1) Fail("file stream inventory differs");
}

Handle OpenLockedFile(const std::wstring& path) {
    if (!g_path_locks) Fail("retained path transaction absent");
    Handle result = g_path_locks->file(path);
    if (!result) Fail("runtime file open or sharing policy failed");
    FILE_ATTRIBUTE_TAG_INFO tag{};
    FILE_STANDARD_INFO standard{};
    if (!GetFileInformationByHandleEx(result.get(), FileAttributeTagInfo, &tag, sizeof(tag)) ||
        !GetFileInformationByHandleEx(result.get(), FileStandardInfo, &standard, sizeof(standard)) ||
        (tag.FileAttributes & (FILE_ATTRIBUTE_DIRECTORY | FILE_ATTRIBUTE_REPARSE_POINT)) ||
        standard.NumberOfLinks != 1 || standard.DeletePending) {
        Fail("runtime file type, link, reparse, or delete state differs");
    }
    RequireSingleUnnamedDataStream(result.get(), false);
    return result;
}

std::string ReadLockedFile(Handle& file, size_t maximum) {
    LARGE_INTEGER size{};
    if (!GetFileSizeEx(file.get(), &size) || size.QuadPart <= 0 ||
        static_cast<uint64_t>(size.QuadPart) > maximum) Fail("file size bound differs");
    std::string result(static_cast<size_t>(size.QuadPart), '\0');
    DWORD got = 0;
    if (!ReadFile(file.get(), result.data(), static_cast<DWORD>(result.size()), &got, nullptr) ||
        got != result.size()) Fail("file read is partial");
    char extra = 0;
    DWORD extra_count = 0;
    if (!ReadFile(file.get(), &extra, 1, &extra_count, nullptr) || extra_count != 0) {
        Fail("file contains bytes beyond observed size");
    }
    LARGE_INTEGER zero{};
    if (!SetFilePointerEx(file.get(), zero, nullptr, FILE_BEGIN)) Fail("file rewind failed");
    return result;
}

std::wstring JoinRoot(const std::wstring& root, const std::string& relative) {
    std::wstring wide = Utf8ToWide(relative);
    for (wchar_t& ch : wide) if (ch == L'/') ch = L'\\';
    return root + L"\\" + wide;
}

void EnumerateFiles(const std::wstring& root, const std::wstring& relative,
                    std::vector<std::string>& paths) {
    std::wstring directory = relative.empty() ? root : root + L"\\" + relative;
    if (!g_path_locks || relative.size() > 1024 || paths.size() > S0_MAX_RUNTIME_FILES + 16) Fail("inventory resource bound");
    HANDLE retained_directory = g_path_locks->directory(directory);
    RequireSingleUnnamedDataStream(retained_directory, true);
    WIN32_FILE_ATTRIBUTE_DATA root_data{};
    if (!GetFileAttributesExW(directory.c_str(), GetFileExInfoStandard, &root_data) ||
        !(root_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) ||
        (root_data.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT)) Fail("runtime directory differs");
    WIN32_FIND_DATAW data{};
    HANDLE raw = FindFirstFileW((directory + L"\\*").c_str(), &data);
    if (raw == INVALID_HANDLE_VALUE) Fail("runtime enumeration failed");
    SearchHandle search(raw);
    std::vector<std::wstring> discovered;
    for (;;) {
        std::wstring name = data.cFileName;
        if (name != L"." && name != L"..") {
            discovered.push_back(name);
            if (discovered.size() > 2048) Fail("directory discovery bound");
            if (data.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT) Fail("runtime reparse entry rejected");
            std::wstring child = relative.empty() ? name : relative + L"\\" + name;
            if (data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
                EnumerateFiles(root, child, paths);
            } else {
                std::string value = WideToUtf8(child);
                std::replace(value.begin(), value.end(), '\\', '/');
                if (!SafeVirtualPath(value)) Fail("runtime enumerated path is not canonical");
                paths.push_back(value);
            }
        }
        if (!FindNextFileW(search.get(), &data)) {
            if (GetLastError() != ERROR_NO_MORE_FILES) Fail("runtime enumeration changed");
            break;
        }
    }
    std::vector<std::wstring> authoritative;
    std::array<uint8_t, 65536> buffer{};
    bool restart = true;
    for (;;) {
        BOOL ok = GetFileInformationByHandleEx(retained_directory,
            restart ? FileIdExtdDirectoryRestartInfo : FileIdExtdDirectoryInfo,
            buffer.data(), static_cast<DWORD>(buffer.size()));
        restart = false;
        if (!ok) { if (GetLastError() == ERROR_NO_MORE_FILES) break; Fail("retained enumeration failed"); }
        size_t offset = 0;
        for (;;) {
            if (offset > buffer.size() - offsetof(FILE_ID_EXTD_DIR_INFO, FileName)) Fail("directory entry bound");
            const auto* item = reinterpret_cast<const FILE_ID_EXTD_DIR_INFO*>(buffer.data() + offset);
            if (item->FileNameLength % 2 || item->FileNameLength >
                buffer.size() - offset - offsetof(FILE_ID_EXTD_DIR_INFO, FileName)) Fail("directory name bound");
            std::wstring name(item->FileName, item->FileNameLength / 2);
            if (name != L"." && name != L"..") {
                if (authoritative.size() >= 2048) Fail("retained directory count bound");
                authoritative.push_back(name); g_path_locks->record(directory + L"\\" + name, item->FileId);
            }
            if (!item->NextEntryOffset) break;
            if (item->NextEntryOffset < offsetof(FILE_ID_EXTD_DIR_INFO, FileName) ||
                item->NextEntryOffset > buffer.size() - offset) Fail("directory next bound");
            offset += item->NextEntryOffset;
        }
    }
    std::sort(discovered.begin(), discovered.end());
    std::sort(authoritative.begin(), authoritative.end());
    if (discovered != authoritative) Fail("discovery and retained directory inventory differ");
    g_path_locks->check();

}

void RequireExactDirectorySet(const std::wstring& root, const std::vector<std::string>& files) {
    std::set<std::wstring> expected{root};
    for (const std::string& path : files) {
        for (size_t slash = path.find('/'); slash != std::string::npos; slash = path.find('/', slash + 1))
            expected.insert(JoinRoot(root, path.substr(0, slash)));
    }
    if (!g_path_locks) Fail("directory set transaction absent");
    g_path_locks->exact_directories(root, expected);
}

std::vector<ManifestRow> VerifyRuntimeClosure(const std::wstring& root,
                                               const std::wstring& manifest_path,
                                               const std::string& expected_manifest_sha256,
                                               size_t expected_rows,
                                               uint64_t expected_total_bytes) {
    Handle manifest = OpenLockedFile(manifest_path);
    std::string raw = ReadLockedFile(manifest, 512u * 1024u);
    if (Hex(HashBytes(raw).bytes, 32) != expected_manifest_sha256) Fail("runtime manifest pin differs");
    std::vector<ManifestRow> rows = ParseManifest(raw, expected_rows);
    std::vector<std::string> observed;
    EnumerateFiles(root, L"", observed);
    std::sort(observed.begin(), observed.end());
    std::vector<std::string> expected;
    for (const auto& row : rows) expected.push_back(row.path);
    if (observed != expected) Fail("runtime exact file inventory differs");
    RequireExactDirectorySet(root, expected);
    uint64_t total = 0;
    for (auto& row : rows) {
        row.handle = OpenLockedFile(JoinRoot(root, row.path));
        LARGE_INTEGER size{};
        if (!GetFileSizeEx(row.handle.get(), &size) || size.QuadPart < 0) Fail("runtime size failed");
        row.size = static_cast<uint64_t>(size.QuadPart);
        total += row.size;
        if (Hex(HashHandle(row.handle.get()).bytes, 32) != row.sha256) Fail("runtime byte hash differs");
    }
    if (total != expected_total_bytes) Fail("runtime total bytes differ");
    return rows;
}

std::string EvidenceSidecarBytes(const EvidencePin& pin) {
    std::string path = pin.path;
    size_t slash = path.rfind('/');
    std::string filename = slash == std::string::npos ? path : path.substr(slash + 1);
    return std::string(pin.sha256) + "  " + filename + "\n";
}

BaseRuntimeClosure VerifyBaseRuntimeClosure(const std::wstring& root,
                                             const std::wstring& manifest_path) {
    const std::wstring expected_manifest = JoinRoot(root, "evidence/payload-manifest.json");
    if (CompareStringOrdinal(expected_manifest.c_str(), -1, manifest_path.c_str(), -1,
                             FALSE) != CSTR_EQUAL) {
        Fail("base payload manifest path differs");
    }
    Handle manifest = OpenLockedFile(manifest_path);
    std::string raw = ReadLockedFile(manifest, 512u * 1024u);
    if (Hex(HashBytes(raw).bytes, 32) != kRuntimeManifestSha) {
        Fail("base payload JSON pin differs");
    }
    BaseRuntimeClosure closure{};
    closure.payload = BasePayloadJsonParser(raw).Parse();

    std::vector<std::string> observed;
    EnumerateFiles(root, L"", observed);
    std::sort(observed.begin(), observed.end());
    std::vector<std::string> expected;
    for (const auto& row : closure.payload) expected.push_back(row.path);
    for (const auto& pin : kBaseEvidencePins) {
        expected.push_back(pin.path);
        expected.push_back(std::string(pin.path) + ".sha256");
    }
    std::sort(expected.begin(), expected.end());
    if (observed.size() != 182 || expected.size() != 182 || observed != expected) {
        Fail("base root is not the exact 174-payload plus 8-evidence set");
    }

    RequireExactDirectorySet(root, expected);
    uint64_t payload_bytes = 0;
    for (auto& row : closure.payload) {
        row.handle = OpenLockedFile(JoinRoot(root, row.path));
        LARGE_INTEGER size{};
        if (!GetFileSizeEx(row.handle.get(), &size) || size.QuadPart < 0 ||
            static_cast<uint64_t>(size.QuadPart) != row.size ||
            Hex(HashHandle(row.handle.get()).bytes, 32) != row.sha256) {
            Fail("base payload target size or hash differs");
        }
        payload_bytes += row.size;
    }
    if (closure.payload.size() != 174 || payload_bytes != 24138847ull) {
        Fail("base payload aggregate differs");
    }

    for (const auto& pin : kBaseEvidencePins) {
        ManifestRow evidence{pin.path, pin.sha256};
        evidence.handle = OpenLockedFile(JoinRoot(root, evidence.path));
        LARGE_INTEGER evidence_size{};
        if (!GetFileSizeEx(evidence.handle.get(), &evidence_size) || evidence_size.QuadPart <= 0) {
            Fail("base evidence target size differs");
        }
        evidence.size = static_cast<uint64_t>(evidence_size.QuadPart);
        if (Hex(HashHandle(evidence.handle.get()).bytes, 32) != evidence.sha256) {
            Fail("base evidence target hash differs");
        }
        closure.evidence.push_back(std::move(evidence));

        ManifestRow sidecar{};
        sidecar.path = std::string(pin.path) + ".sha256";
        sidecar.handle = OpenLockedFile(JoinRoot(root, sidecar.path));
        std::string sidecar_raw = ReadLockedFile(sidecar.handle, 512);
        if (sidecar_raw != EvidenceSidecarBytes(pin)) {
            Fail("base evidence sidecar bytes differ");
        }
        sidecar.size = sidecar_raw.size();
        sidecar.sha256 = Hex(HashBytes(sidecar_raw).bytes, 32);
        closure.evidence.push_back(std::move(sidecar));
    }
    if (closure.evidence.size() != 8) Fail("base evidence inventory differs");
    return closure;
}

std::vector<ManifestRow> VerifyEffectivePackage(
    const std::wstring& package_root,
    const std::wstring& manifest_path,
    const std::map<std::string, std::string>& control,
    Handle& retained_manifest) {
    const std::wstring expected_manifest =
        package_root + L"\\runtime-profile-package-files-v0.5.sha256";
    if (CompareStringOrdinal(expected_manifest.c_str(), -1, manifest_path.c_str(), -1,
                             FALSE) != CSTR_EQUAL) {
        Fail("effective package manifest path differs");
    }
    retained_manifest = OpenLockedFile(manifest_path);
    std::string raw = ReadLockedFile(retained_manifest, 64u * 1024u);
    if (Hex(HashBytes(raw).bytes, 32) != Field(control, "effective_runtime_package_sha256")) {
        Fail("effective package manifest hash differs");
    }
    std::vector<ManifestRow> rows = ParseManifest(raw, 6);
    static const std::array<const char*, 6> expected_paths = {
        "runtime-files.sha256", "runtime-profile-v0.1.json",
        "runtime-profile-v0.2.json", "runtime-profile-v0.3.json",
        "runtime-profile-v0.4.json", "runtime-profile-v0.5.json"
    };
    static const std::array<const char*, 6> control_hashes = {
        nullptr, "runtime_profile_v0_1_sha256", "runtime_profile_v0_2_sha256",
        "runtime_profile_v0_3_sha256", "runtime_profile_v0_4_sha256", "runtime_profile_v0_5_sha256"
    };
    std::vector<std::string> package_files;
    EnumerateFiles(package_root, L"", package_files);
    std::sort(package_files.begin(), package_files.end());
    std::vector<std::string> expected_package_files = {
        "runtime-files.sha256", "runtime-profile-package-files-v0.5.sha256",
        "runtime-profile-v0.1.json", "runtime-profile-v0.2.json",
        "runtime-profile-v0.3.json", "runtime-profile-v0.4.json", "runtime-profile-v0.5.json"
    };
    std::sort(expected_package_files.begin(), expected_package_files.end());
    if (package_files != expected_package_files) Fail("effective package exact file set differs");
    RequireExactDirectorySet(package_root, expected_package_files);
    for (size_t index = 0; index < rows.size(); ++index) {
        if (rows[index].path != expected_paths[index]) Fail("effective package row order differs");
        rows[index].handle = OpenLockedFile(JoinRoot(package_root, rows[index].path));
        LARGE_INTEGER size{};
        if (!GetFileSizeEx(rows[index].handle.get(), &size) || size.QuadPart <= 0) {
            Fail("effective package target size differs");
        }
        rows[index].size = static_cast<uint64_t>(size.QuadPart);
        if (Hex(HashHandle(rows[index].handle.get()).bytes, 32) != rows[index].sha256) {
            Fail("effective package target hash differs");
        }
        if (index == 0) {
            if (rows[index].sha256 != Field(control, "runtime_files_manifest_sha256")) {
                Fail("runtime manifest package row differs");
            }
        } else if (rows[index].sha256 != Field(control, control_hashes[index])) {
            Fail("runtime profile predecessor or current hash differs");
        }
    }
    return rows;
}

const ManifestRow& RuntimeRow(const std::vector<ManifestRow>& rows, const std::string& path) {
    auto it = std::lower_bound(rows.begin(), rows.end(), path,
        [](const ManifestRow& row, const std::string& name) { return row.path < name; });
    if (it == rows.end() || it->path != path) Fail("runtime launch file is outside manifest");
    return *it;
}

void ReverifyRuntime(const std::wstring& root, std::vector<ManifestRow>& rows,
                     uint64_t expected_total_bytes) {
    std::vector<std::string> observed;
    EnumerateFiles(root, L"", observed);
    std::sort(observed.begin(), observed.end());
    std::vector<std::string> expected;
    for (const auto& row : rows) expected.push_back(row.path);
    if (observed != expected) Fail("runtime inventory changed");
    RequireExactDirectorySet(root, expected);
    uint64_t total = 0;
    for (auto& row : rows) {
        LARGE_INTEGER size{};
        if (!GetFileSizeEx(row.handle.get(), &size) || size.QuadPart < 0 ||
            static_cast<uint64_t>(size.QuadPart) != row.size ||
            Hex(HashHandle(row.handle.get()).bytes, 32) != row.sha256) {
            Fail("retained runtime file changed");
        }
        total += row.size;
    }
    if (total != expected_total_bytes) Fail("retained runtime closure differs");
}

void ReverifyBaseRuntime(const std::wstring& root, BaseRuntimeClosure& closure) {
    std::vector<std::string> observed;
    EnumerateFiles(root, L"", observed);
    std::sort(observed.begin(), observed.end());
    std::vector<std::string> expected;
    for (const auto& row : closure.payload) expected.push_back(row.path);
    for (const auto& row : closure.evidence) expected.push_back(row.path);
    std::sort(expected.begin(), expected.end());
    if (observed.size() != 182 || expected.size() != 182 || observed != expected) {
        Fail("retained base runtime inventory changed");
    }
    RequireExactDirectorySet(root, expected);
    uint64_t payload_bytes = 0;
    for (auto& row : closure.payload) {
        LARGE_INTEGER size{};
        if (!GetFileSizeEx(row.handle.get(), &size) || size.QuadPart < 0 ||
            static_cast<uint64_t>(size.QuadPart) != row.size ||
            Hex(HashHandle(row.handle.get()).bytes, 32) != row.sha256) {
            Fail("retained base payload changed");
        }
        payload_bytes += row.size;
    }
    for (auto& row : closure.evidence) {
        LARGE_INTEGER size{};
        if (!GetFileSizeEx(row.handle.get(), &size) || size.QuadPart < 0 ||
            static_cast<uint64_t>(size.QuadPart) != row.size ||
            Hex(HashHandle(row.handle.get()).bytes, 32) != row.sha256) {
            Fail("retained base evidence changed");
        }
    }
    if (closure.payload.size() != 174 || closure.evidence.size() != 8 ||
        payload_bytes != 24138847ull) {
        Fail("retained base runtime aggregate changed");
    }
}

void RequireBaseSubset(const std::vector<ManifestRow>& base,
                       const std::vector<ManifestRow>& final_rows) {
    for (const auto& base_row : base) {
        auto it = std::lower_bound(final_rows.begin(), final_rows.end(), base_row.path,
            [](const ManifestRow& row, const std::string& name) { return row.path < name; });
        if (it == final_rows.end() || it->path != base_row.path ||
            it->sha256 != base_row.sha256 || it->size != base_row.size) {
            Fail("v0.7 base runtime row is absent or changed in final closure");
        }
    }
}

void ReverifyPackage(const std::wstring& package_root, Handle& manifest,
                     std::vector<ManifestRow>& rows,
                     const std::string& expected_manifest_sha256) {
    if (Hex(HashHandle(manifest.get()).bytes, 32) != expected_manifest_sha256 || rows.size() != 6) {
        Fail("retained package manifest changed");
    }
    std::vector<std::string> package_files;
    EnumerateFiles(package_root, L"", package_files);
    std::sort(package_files.begin(), package_files.end());
    const std::vector<std::string> expected_package_files = {
        "runtime-files.sha256", "runtime-profile-package-files-v0.5.sha256",
        "runtime-profile-v0.1.json", "runtime-profile-v0.2.json",
        "runtime-profile-v0.3.json", "runtime-profile-v0.4.json", "runtime-profile-v0.5.json"
    };
    if (package_files != expected_package_files) Fail("retained package exact set changed");
    RequireExactDirectorySet(package_root, expected_package_files);
    for (auto& row : rows) {
        LARGE_INTEGER size{};
        if (!GetFileSizeEx(row.handle.get(), &size) || size.QuadPart < 0 ||
            static_cast<uint64_t>(size.QuadPart) != row.size ||
            Hex(HashHandle(row.handle.get()).bytes, 32) != row.sha256) {
            Fail("retained package target changed");
        }
    }
}

S0_FILE_IDENTITY FileIdentity(HANDLE handle) {
    FILE_ID_INFO info{};
    if (!GetFileInformationByHandleEx(handle, FileIdInfo, &info, sizeof(info))) {
        Fail("file identity query failed");
    }
    S0_FILE_IDENTITY result{};
    result.volume_serial = info.VolumeSerialNumber;
    memcpy(result.file_id, info.FileId.Identifier, 16);
    return result;
}

bool SameIdentity(const S0_FILE_IDENTITY& left, const S0_FILE_IDENTITY& right) {
    return left.volume_serial == right.volume_serial &&
           memcmp(left.file_id, right.file_id, 16) == 0;
}

ACCESS_MASK GrantedAccess(HANDLE handle) {
    S0ObjectBasicInformation info{};
    ULONG returned = 0;
    NTSTATUS status = NtQueryObject(handle, ObjectBasicInformation,
                                    &info, sizeof(info), &returned);
    if (status < 0 || returned < offsetof(S0ObjectBasicInformation, creation_time)) {
        Fail("created root access query failed");
    }
    return info.granted_access;
}

Handle OpenOutputParent(const std::wstring& path) {
    if (!g_path_locks) Fail("retained output transaction absent");
    HANDLE original = g_path_locks->directory(path), raw = nullptr;
    if (!DuplicateHandle(GetCurrentProcess(), original, GetCurrentProcess(), &raw, S0_ROOT_ACCESS, FALSE, 0))
        Fail("retained output parent duplication failed");
    Handle result(raw);
    if (!result) Fail("output parent open failed");
    FILE_ATTRIBUTE_TAG_INFO tag{};
    if (!GetFileInformationByHandleEx(result.get(), FileAttributeTagInfo, &tag, sizeof(tag)) ||
        !(tag.FileAttributes & FILE_ATTRIBUTE_DIRECTORY) ||
        (tag.FileAttributes & FILE_ATTRIBUTE_REPARSE_POINT)) Fail("output parent is not an ordinary directory");
    FILE_CASE_SENSITIVE_INFO case_info{};
    if (!GetFileInformationByHandleEx(result.get(), FileCaseSensitiveInfo,
                                      &case_info, sizeof(case_info)) || case_info.Flags != 0) {
        Fail("output parent case policy differs");
    }
    wchar_t volume_path[MAX_PATH]{};
    if (!GetVolumePathNameW(path.c_str(), volume_path, static_cast<DWORD>(std::size(volume_path))) ||
        GetDriveTypeW(volume_path) != DRIVE_FIXED) Fail("output volume is not local fixed media");
    wchar_t fs_name[32]{};
    if (!GetVolumeInformationByHandleW(result.get(), nullptr, 0, nullptr, nullptr, nullptr,
                                       fs_name, static_cast<DWORD>(std::size(fs_name))) ||
        _wcsicmp(fs_name, L"NTFS") != 0) Fail("output volume is not NTFS");
    return result;
}

void RequireCreatedRootPostconditions(HANDLE root, const std::string& leaf) {
    if (GrantedAccess(root) != S0_ROOT_ACCESS) Fail("created root granted access differs");

    std::array<uint8_t, 4096> directory_buffer{};
    if (GetFileInformationByHandleEx(root, FileIdBothDirectoryRestartInfo,
                                     directory_buffer.data(),
                                     static_cast<DWORD>(directory_buffer.size()))) {
        auto* entry = reinterpret_cast<FILE_ID_BOTH_DIR_INFO*>(directory_buffer.data());
        for (;;) {
            std::wstring name(entry->FileName, entry->FileNameLength / sizeof(wchar_t));
            if (name != L"." && name != L"..") Fail("created root is not empty");
            if (!entry->NextEntryOffset) break;
            entry = reinterpret_cast<FILE_ID_BOTH_DIR_INFO*>(
                reinterpret_cast<uint8_t*>(entry) + entry->NextEntryOffset);
        }
    } else if (GetLastError() != ERROR_NO_MORE_FILES) {
        Fail("created root enumeration failed");
    }

    RequireSingleUnnamedDataStream(root, true);

    std::wstring final_path(S0_MAX_PATH_CHARS, L'\0');
    DWORD length = GetFinalPathNameByHandleW(root, final_path.data(),
                                             static_cast<DWORD>(final_path.size()),
                                             FILE_NAME_NORMALIZED | VOLUME_NAME_DOS);
    if (!length || length >= final_path.size()) Fail("created root final path query failed");
    final_path.resize(length);
    const std::wstring suffix = L"\\" + Utf8ToWide(leaf);
    if (final_path.size() < suffix.size() ||
        final_path.compare(final_path.size() - suffix.size(), suffix.size(), suffix) != 0) {
        Fail("created root exact leaf case differs");
    }
}

bool CanonicalLeaf(const std::string& leaf) {
    if (leaf.empty() || leaf.size() > 120 || leaf.front() == '.' || leaf.back() == '.' || leaf.back() == ' ') return false;
    for (unsigned char ch : leaf) {
        if (!(ch >= 'A' && ch <= 'Z') && !(ch >= 'a' && ch <= 'z') &&
            !(ch >= '0' && ch <= '9') && ch != '-' && ch != '_') return false;
    }
    return leaf != "." && leaf != "..";
}

Handle CreateAtomicRoot(HANDLE parent, const std::string& leaf) {
    std::wstring wide = Utf8ToWide(leaf);
    if (wide.size() > (USHRT_MAX / sizeof(wchar_t))) Fail("output leaf is too long");
    UNICODE_STRING name{};
    name.Buffer = wide.data();
    name.Length = static_cast<USHORT>(wide.size() * sizeof(wchar_t));
    name.MaximumLength = name.Length;
    OBJECT_ATTRIBUTES attributes{};
    InitializeObjectAttributes(&attributes, &name, S0_OBJECT_ATTRIBUTES_FLAGS, parent, nullptr);
    IO_STATUS_BLOCK io{};
    HANDLE raw = nullptr;
    NTSTATUS status = NtCreateFile(&raw, S0_ROOT_ACCESS, &attributes, &io, nullptr,
                                   S0_ROOT_ATTRIBUTES, S0_ROOT_SHARE,
                                   S0_ROOT_DISPOSITION, S0_ROOT_OPTIONS, nullptr, 0);
    Handle root(raw);
    if (status != 0 || io.Status != status || io.Information != S0_FILE_CREATED ||
        !raw || raw == INVALID_HANDLE_VALUE) Fail("atomic root create result differs");
    FILE_ATTRIBUTE_TAG_INFO tag{};
    FILE_STANDARD_INFO standard{};
    if (!GetFileInformationByHandleEx(root.get(), FileAttributeTagInfo, &tag, sizeof(tag)) ||
        !GetFileInformationByHandleEx(root.get(), FileStandardInfo, &standard, sizeof(standard)) ||
        !(tag.FileAttributes & FILE_ATTRIBUTE_DIRECTORY) ||
        (tag.FileAttributes & FILE_ATTRIBUTE_REPARSE_POINT) || standard.NumberOfLinks != 1 ||
        standard.DeletePending) Fail("created root postconditions differ");
    RequireCreatedRootPostconditions(root.get(), leaf);
    return root;
}

void MakePipe(Handle& parent_end, Handle& child_end, bool child_reads) {
    SECURITY_ATTRIBUTES security{sizeof(security), nullptr, TRUE};
    HANDLE read_raw = nullptr, write_raw = nullptr;
    if (!CreatePipe(&read_raw, &write_raw, &security, 8192)) Fail("pipe creation failed");
    Handle read(read_raw), write(write_raw);
    if (child_reads) {
        child_end = std::move(read);
        parent_end = std::move(write);
    } else {
        parent_end = std::move(read);
        child_end = std::move(write);
    }
    if (!SetHandleInformation(parent_end.get(), HANDLE_FLAG_INHERIT, 0)) Fail("parent pipe inheritance clear failed");
    DWORD flags = 0;
    if (!GetHandleInformation(child_end.get(), &flags) || !(flags & HANDLE_FLAG_INHERIT)) {
        Fail("child pipe is not inheritable");
    }
}

std::string HandleLocator(HANDLE handle) {
    char text[19]{};
    unsigned long long value = static_cast<unsigned long long>(reinterpret_cast<uintptr_t>(handle));
    if (sprintf_s(text, "0x%016llx", value) != 18) Fail("handle locator formatting failed");
    return text;
}

std::wstring QuoteCommand(const std::wstring& value) {
    if (value.empty() || value.find(L'"') != std::wstring::npos || value.find(L'\0') != std::wstring::npos) {
        Fail("command path is malformed");
    }
    return L"\"" + value + L"\"";
}

std::string BuildLaunchEvidence(const std::map<std::string, std::string>& control,
                                const std::string& control_sha,
                                const std::array<std::string, S0_HANDLE_COUNT>& locators) {
    auto fields = control;
    fields["runtime_package_sha256"] = Field(control, "effective_runtime_package_sha256");
    fields["launch_control_sha256"] = control_sha;
    return S0EvidenceV2(fields, locators);

}

std::string CanonicalJson(const std::map<std::string, std::string>& fields) {
    std::string raw = "{";
    bool first = true;
    for (const auto& field : fields) {
        if (!first) raw.push_back(',');
        raw += EncodeJsonString(field.first) + ":" + EncodeJsonString(field.second);
        first = false;
    }
    raw += "}\n";
    if (raw.size() > S0_MAX_ADMISSION_FRAME) Fail("admission frame bound exceeded");
    return raw;
}

void WriteAll(HANDLE handle, const std::string& bytes) {
    size_t offset = 0;
    while (offset < bytes.size()) {
        DWORD wrote = 0;
        DWORD request = static_cast<DWORD>(std::min<size_t>(bytes.size() - offset, 65536));
        if (!WriteFile(handle, bytes.data() + offset, request, &wrote, nullptr) || !wrote) {
            Fail("pipe write failed");
        }
        offset += wrote;
    }
}

std::string ReadCommitWithTimeout(HANDLE pipe, HANDLE process) {
    DWORD started = GetTickCount();
    std::string raw;
    for (;;) {
        DWORD available = 0;
        if (!PeekNamedPipe(pipe, nullptr, 0, nullptr, &available, nullptr)) {
            if (GetLastError() == ERROR_BROKEN_PIPE) break;
            Fail("commit pipe query failed");
        }
        if (available) {
            std::array<char, S0_MAX_COMMIT_FRAME> buffer{};
            DWORD got = 0;
            if (!ReadFile(pipe, buffer.data(),
                          std::min<DWORD>(available, static_cast<DWORD>(buffer.size())),
                          &got, nullptr)) Fail("commit request read failed");
            raw.append(buffer.data(), got);
            if (raw.size() > S0_MAX_COMMIT_FRAME) Fail("commit request oversized");
        } else if (WaitForSingleObject(process, 0) == WAIT_OBJECT_0) {
            Fail("verifier exited before commit");
        }
        if (GetTickCount() - started > kCommitTimeoutMs) Fail("commit request timed out");
        if (raw == "RUNTIME_ADMISSION_COMMIT\n") {
            DWORD later = 0;
            if (!PeekNamedPipe(pipe, nullptr, 0, nullptr, &later, nullptr)) {
                if (GetLastError() == ERROR_BROKEN_PIPE) return raw;
                Fail("commit EOF query failed");
            }
            if (later) Fail("commit request has extra bytes");
        }
        Sleep(2);
    }
    if (raw != "RUNTIME_ADMISSION_COMMIT\n") Fail("commit request or EOF differs");
    return raw;
}

Handle CreateJob() {
    Handle job(CreateJobObjectW(nullptr, nullptr));
    if (!job) Fail("job creation failed");
    JOBOBJECT_EXTENDED_LIMIT_INFORMATION limits{};
    limits.BasicLimitInformation.LimitFlags =
        JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE | JOB_OBJECT_LIMIT_ACTIVE_PROCESS;
    limits.BasicLimitInformation.ActiveProcessLimit = 2;
    if (!SetInformationJobObject(job.get(), JobObjectExtendedLimitInformation,
                                 &limits, sizeof(limits))) Fail("job policy failed");
    return job;
}

std::vector<wchar_t> BuildEnvironment(const std::wstring& system_root) {
    if (!IsAbsoluteDrivePath(system_root) || system_root.size() < 3) Fail("system root differs");
    std::wstring drive = system_root.substr(0, 2);
    std::wstring joined = L"SYSTEMDRIVE=" + drive + L'\0' +
                          L"SYSTEMROOT=" + system_root + L'\0' +
                          L"WINDIR=" + system_root + L'\0';
    std::vector<wchar_t> result(joined.begin(), joined.end());
    result.push_back(L'\0');
    return result;
}

void RequireControlShape(const std::map<std::string, std::string>& control) {
    static const std::array<const char*, 42> names = {
        "application_sha256", "application_virtual_path",
        "base_runtime_files_manifest_path", "base_runtime_root", "bootstrap_sha256",
        "bootstrap_virtual_path", "effective_package_manifest_path",
        "effective_runtime_package_sha256", "effective_interface_map_sha256", "effective_schema_sha256",
        "external_pin_digest", "final_runtime_file_count", "final_runtime_total_bytes",
        "guard_sha256", "guard_virtual_path", "loaded_pe_manifest_sha256",
        "loaded_pe_manifest_virtual_path", "materialization_manifest_sha256",
        "materialization_status_sha256", "output_leaf", "output_parent",
        "platform_manifest_sha256", "platform_manifest_virtual_path",
        "preloader_image_path", "preloader_image_sha256", "preloader_virtual_path", "repository_root", "run_nonce",
        "runtime_files_manifest_path", "runtime_files_manifest_sha256",
        "runtime_profile_v0_1_sha256", "runtime_profile_v0_2_sha256",
        "runtime_profile_v0_3_sha256", "runtime_profile_v0_4_sha256", "runtime_profile_v0_5_sha256",
        "runtime_package_root", "runtime_root", "schema_id", "system_root", "verifier_sha256",
        "verifier_virtual_path", "workspace_root"
    };
    if (control.size() != names.size()) Fail("control field count differs");
    for (const char* name : names) (void)Field(control, name);
    if (Field(control, "schema_id") != "S0-RUNTIME-PRELOADER-V0.5-CONTROL-1" ||
        Field(control, "effective_interface_map_sha256") != "f6aa0f38ad7eb7bf2715fbc6084c5ce9c05db23eccca1af65956735e1e933623" ||
        Field(control, "effective_schema_sha256") != "04ae781b7d71e2954378cf7cdf2aa9070634ddc3a25c883ac52fb83ebe139d7e" ||
        Field(control, "materialization_manifest_sha256") != kMaterializationManifestSha ||
        Field(control, "materialization_status_sha256") != kMaterializationStatusSha ||
        ParseDecimal(Field(control, "final_runtime_file_count")) <= 174 ||
        ParseDecimal(Field(control, "final_runtime_file_count")) > S0_MAX_RUNTIME_FILES ||
        ParseDecimal(Field(control, "final_runtime_total_bytes")) <= 24138847ull ||
        ParseDecimal(Field(control, "final_runtime_total_bytes")) > S0_MAX_RUNTIME_BYTES) {
        Fail("control authority contract differs");
    }
    for (const char* name : {"application_sha256", "bootstrap_sha256",
                             "effective_runtime_package_sha256", "external_pin_digest",
                             "guard_sha256", "loaded_pe_manifest_sha256",
                             "platform_manifest_sha256", "preloader_image_sha256", "run_nonce",
                             "runtime_files_manifest_sha256",
                             "runtime_profile_v0_1_sha256", "runtime_profile_v0_2_sha256",
                             "runtime_profile_v0_3_sha256", "runtime_profile_v0_4_sha256", "runtime_profile_v0_5_sha256",
                             "verifier_sha256"}) {
        if (!IsLowerSha(Field(control, name))) Fail("control SHA-256 field differs");
    }
    if (!SafeVirtualPath(Field(control, "application_virtual_path")) ||
        !SafeVirtualPath(Field(control, "bootstrap_virtual_path")) ||
        !SafeVirtualPath(Field(control, "guard_virtual_path")) ||
        !SafeVirtualPath(Field(control, "loaded_pe_manifest_virtual_path")) ||
        !SafeVirtualPath(Field(control, "platform_manifest_virtual_path")) ||
        !SafeVirtualPath(Field(control, "preloader_virtual_path")) ||
        !SafeVirtualPath(Field(control, "verifier_virtual_path")) ||
        !CanonicalLeaf(Field(control, "output_leaf"))) Fail("control path identity differs");
}

int Run(HANDLE control_handle) {
    DWORD control_flags = 0;
    if (!GetHandleInformation(control_handle, &control_flags) ||
        !(control_flags & HANDLE_FLAG_INHERIT) || GetFileType(control_handle) != FILE_TYPE_PIPE) {
        Fail("control channel identity differs");
    }
    Handle control_owner(control_handle);
    std::string control_raw = ReadBounded(control_owner.get(), S0_MAX_CONTROL_FRAME);
    control_owner.reset();
    std::map<std::string, std::string> control = ParseFlatCanonicalJson(control_raw);
    RequireControlShape(control);
    PathScope retained_paths;

    std::wstring base_runtime_root = Utf8ToWide(Field(control, "base_runtime_root"));
    std::wstring base_runtime_manifest_path = Utf8ToWide(Field(control, "base_runtime_files_manifest_path"));
    std::wstring runtime_root = Utf8ToWide(Field(control, "runtime_root"));
    std::wstring runtime_package_root = Utf8ToWide(Field(control, "runtime_package_root"));
    std::wstring runtime_manifest_path = Utf8ToWide(Field(control, "runtime_files_manifest_path"));
    std::wstring package_manifest_path = Utf8ToWide(Field(control, "effective_package_manifest_path"));
    std::wstring output_parent_path = Utf8ToWide(Field(control, "output_parent"));
    std::wstring system_root = Utf8ToWide(Field(control, "system_root"));
    std::wstring preloader_image_path = Utf8ToWide(Field(control, "preloader_image_path"));
    if (!IsAbsoluteDrivePath(base_runtime_root) || !IsAbsoluteDrivePath(base_runtime_manifest_path) ||
        !IsAbsoluteDrivePath(runtime_root) || !IsAbsoluteDrivePath(runtime_package_root) ||
        !IsAbsoluteDrivePath(runtime_manifest_path) || !IsAbsoluteDrivePath(package_manifest_path) ||
        !IsAbsoluteDrivePath(output_parent_path) || !IsAbsoluteDrivePath(system_root) ||
        !IsAbsoluteDrivePath(preloader_image_path)) {
        Fail("absolute root contract differs");
    }
    RequireNoReparseChain(base_runtime_root);
    RequireNoReparseChain(base_runtime_manifest_path);
    RequireNoReparseChain(runtime_root);
    RequireNoReparseChain(runtime_package_root);
    RequireNoReparseChain(runtime_manifest_path);
    RequireNoReparseChain(package_manifest_path);
    RequireNoReparseChain(output_parent_path);
    RequireNoReparseChain(system_root);
    RequireNoReparseChain(preloader_image_path);
    const std::wstring expected_runtime_manifest = runtime_package_root + L"\\runtime-files.sha256";
    if (CompareStringOrdinal(expected_runtime_manifest.c_str(), -1,
                             runtime_manifest_path.c_str(), -1, FALSE) != CSTR_EQUAL) {
        Fail("runtime manifest path differs from effective package");
    }
    Handle package_manifest;
    std::vector<ManifestRow> package = VerifyEffectivePackage(
        runtime_package_root, package_manifest_path, control, package_manifest);
    BaseRuntimeClosure base_runtime = VerifyBaseRuntimeClosure(
        base_runtime_root, base_runtime_manifest_path);
    const size_t final_file_count = static_cast<size_t>(
        ParseDecimal(Field(control, "final_runtime_file_count")));
    const uint64_t final_total_bytes = ParseDecimal(Field(control, "final_runtime_total_bytes"));
    std::vector<ManifestRow> runtime = VerifyRuntimeClosure(
        runtime_root, runtime_manifest_path, Field(control, "runtime_files_manifest_sha256"),
        final_file_count, final_total_bytes);
    RequireBaseSubset(base_runtime.payload, runtime);
    const ManifestRow& application_row = RuntimeRow(runtime, Field(control, "application_virtual_path"));
    const ManifestRow& bootstrap_row = RuntimeRow(runtime, Field(control, "bootstrap_virtual_path"));
    const ManifestRow& guard_row = RuntimeRow(runtime, Field(control, "guard_virtual_path"));
    const ManifestRow& loaded_pe_row = RuntimeRow(runtime, Field(control, "loaded_pe_manifest_virtual_path"));
    const ManifestRow& platform_row = RuntimeRow(runtime, Field(control, "platform_manifest_virtual_path"));
    const ManifestRow& preloader_row = RuntimeRow(runtime, Field(control, "preloader_virtual_path"));
    const ManifestRow& verifier_row = RuntimeRow(runtime, Field(control, "verifier_virtual_path"));
    if (application_row.sha256 != Field(control, "application_sha256") ||
        bootstrap_row.sha256 != Field(control, "bootstrap_sha256") ||
        guard_row.sha256 != Field(control, "guard_sha256") ||
        loaded_pe_row.sha256 != Field(control, "loaded_pe_manifest_sha256") ||
        platform_row.sha256 != Field(control, "platform_manifest_sha256") ||
        preloader_row.sha256 != Field(control, "preloader_image_sha256") ||
        verifier_row.sha256 != Field(control, "verifier_sha256") ||
        CompareStringOrdinal(JoinRoot(runtime_root, Field(control, "preloader_virtual_path")).c_str(), -1,
                             preloader_image_path.c_str(), -1, FALSE) != CSTR_EQUAL) {
        Fail("launch file hash differs from runtime manifest");
    }

    retained_paths.locks.exclude(output_parent_path, {
        base_runtime_root, runtime_root, runtime_package_root, Utf8ToWide(Field(control, "repository_root"))
    });
    retained_paths.locks.check();
    Handle parent = OpenOutputParent(output_parent_path);
    S0_FILE_IDENTITY parent_identity = FileIdentity(parent.get());
    Handle root = CreateAtomicRoot(parent.get(), Field(control, "output_leaf"));
    S0_FILE_IDENTITY root_identity = FileIdentity(root.get());
    if (SameIdentity(parent_identity, root_identity)) Fail("root and parent identity collide");

    Handle admission_write, admission_read;
    Handle commit_request_read, commit_request_write;
    Handle commit_reply_write, commit_reply_read;
    MakePipe(admission_write, admission_read, true);
    MakePipe(commit_request_read, commit_request_write, false);
    MakePipe(commit_reply_write, commit_reply_read, true);

    Handle child_root;
    HANDLE child_root_raw = nullptr;
    if (!DuplicateHandle(GetCurrentProcess(), root.get(), GetCurrentProcess(), &child_root_raw,
                         S0_ROOT_ACCESS, TRUE, 0)) Fail("root duplicate failed");
    child_root.reset(child_root_raw);
    if (!SameIdentity(root_identity, FileIdentity(child_root.get()))) Fail("root duplicate object differs");

    Handle preloader_process(OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE,
                                         TRUE, GetCurrentProcessId()));
    if (!preloader_process) Fail("preloader process duplicate failed");

    std::array<HANDLE, S0_HANDLE_COUNT> inherited = {
        admission_read.get(), commit_request_write.get(), commit_reply_read.get(),
        child_root.get(), preloader_process.get()
    };
    static_assert(sizeof(inherited) == S0_HANDLE_ARRAY_BYTES_X64);
    std::array<std::string, S0_HANDLE_COUNT> locators{};
    for (size_t index = 0; index < inherited.size(); ++index) {
        DWORD flags = 0;
        if (!GetHandleInformation(inherited[index], &flags) || !(flags & HANDLE_FLAG_INHERIT)) {
            Fail("one child handle is not inheritable");
        }
        locators[index] = HandleLocator(inherited[index]);
    }

    const std::string control_sha = Hex(HashBytes(control_raw).bytes, 32);
    const std::string launch_evidence = BuildLaunchEvidence(control, control_sha, locators);
    const std::string evidence_sha = Hex(HashBytes(launch_evidence).bytes, 32);

    SIZE_T attribute_bytes = 0;
    InitializeProcThreadAttributeList(nullptr, S0_ATTRIBUTE_COUNT, 0, &attribute_bytes);
    if (!attribute_bytes || GetLastError() != ERROR_INSUFFICIENT_BUFFER) Fail("attribute sizing failed");
    std::vector<uint8_t> attribute_storage(attribute_bytes);
    auto* attributes = reinterpret_cast<LPPROC_THREAD_ATTRIBUTE_LIST>(attribute_storage.data());
    if (!InitializeProcThreadAttributeList(attributes, S0_ATTRIBUTE_COUNT, 0, &attribute_bytes)) {
        Fail("attribute initialization failed");
    }
    struct AttributeCleanup {
        LPPROC_THREAD_ATTRIBUTE_LIST value;
        ~AttributeCleanup() { if (value) DeleteProcThreadAttributeList(value); }
    } attribute_cleanup{attributes};
    if (!UpdateProcThreadAttribute(attributes, 0, S0_HANDLE_LIST_ATTRIBUTE,
                                   inherited.data(), sizeof(inherited), nullptr, nullptr)) {
        Fail("handle-list attribute update failed");
    }

    std::wstring application = JoinRoot(runtime_root, Field(control, "application_virtual_path"));
    std::wstring bootstrap = JoinRoot(runtime_root, Field(control, "bootstrap_virtual_path"));
    std::wstring command = QuoteCommand(application) + L" -I -S -B -X utf8 " + QuoteCommand(bootstrap);
    const wchar_t* argument_names[S0_HANDLE_COUNT] = {
        L" --s0-admission-read=", L" --s0-commit-request-write=",
        L" --s0-commit-reply-read=", L" --s0-output-root=",
        L" --s0-preloader-process="
    };
    for (size_t index = 0; index < S0_HANDLE_COUNT; ++index) {
        command += argument_names[index] + Utf8ToWide(locators[index]);
    }
    std::vector<wchar_t> command_buffer(command.begin(), command.end());
    command_buffer.push_back(L'\0');
    std::vector<wchar_t> environment = BuildEnvironment(system_root);

    STARTUPINFOEXW startup{};
    startup.StartupInfo.cb = sizeof(startup);
    startup.StartupInfo.dwFlags = 0;
    startup.lpAttributeList = attributes;
    Handle job = CreateJob();
    PROCESS_INFORMATION process{};
    if (!CreateProcessW(application.c_str(), command_buffer.data(), nullptr, nullptr, TRUE,
                        S0_CREATION_FLAGS, environment.data(), runtime_root.c_str(),
                        &startup.StartupInfo, &process)) Fail("CreateProcessW failed");
    Handle process_handle(process.hProcess);
    Handle thread_handle(process.hThread);
    TerminateOnFailure terminate_on_failure(process_handle.get());

    std::map<std::string, std::string> admission = {
        {"actual_verifier_pid", std::to_string(process.dwProcessId)},
        {"application_path", WideToUtf8(application)},
        {"application_sha256", Field(control, "application_sha256")},
        {"application_virtual_path", Field(control, "application_virtual_path")},
        {"bootstrap_sha256", Field(control, "bootstrap_sha256")},
        {"bootstrap_virtual_path", Field(control, "bootstrap_virtual_path")},
        {"effective_runtime_package_sha256", Field(control, "effective_runtime_package_sha256")},
        {"external_pin_digest", Field(control, "external_pin_digest")},
        {"guard_observation_policy_id", S0_GUARD_POLICY},
        {"kernel_semantics_policy_id", S0_KERNEL_POLICY},
        {"launch_control_sha256", control_sha},
        {"launch_handle_set_evidence_sha256", evidence_sha},
        {"preloader_image_path", Field(control, "preloader_image_path")},
        {"preloader_image_sha256", Field(control, "preloader_image_sha256")},
        {"preloader_pid", std::to_string(GetCurrentProcessId())},
        {"preloader_responsibility_id", S0_PRELOADER_POLICY},
        {"root_file_id", Hex(root_identity.file_id, 16)},
        {"root_volume_serial", Hex(reinterpret_cast<const uint8_t*>(&root_identity.volume_serial), 8)},
        {"run_nonce", Field(control, "run_nonce")},
        {"runtime_profile_v0_1_sha256", Field(control, "runtime_profile_v0_1_sha256")},
        {"runtime_profile_v0_2_sha256", Field(control, "runtime_profile_v0_2_sha256")},
        {"runtime_profile_v0_3_sha256", Field(control, "runtime_profile_v0_3_sha256")},
        {"runtime_profile_v0_4_sha256", Field(control, "runtime_profile_v0_4_sha256")},
        {"schema_id", S0_ADMISSION_SCHEMA},
        {"success_policy_id", S0_SUCCESS_POLICY},
        {"verifier_sha256", Field(control, "verifier_sha256")},
        {"verifier_virtual_path", Field(control, "verifier_virtual_path")},
        {"workspace_root", Field(control, "workspace_root")}
    };
    std::string admission_raw = CanonicalJson(admission);
    WriteAll(admission_write.get(), admission_raw);
    admission_write.reset();

    if (!AssignProcessToJobObject(job.get(), process_handle.get())) Fail("verifier job assignment failed");
    admission_read.reset();
    commit_request_write.reset();
    commit_reply_read.reset();
    child_root.reset();
    preloader_process.reset();
    if (ResumeThread(thread_handle.get()) != 1) Fail("verifier resume count differs");
    thread_handle.reset();

    (void)ReadCommitWithTimeout(commit_request_read.get(), process_handle.get());
    commit_request_read.reset();
    ReverifyBaseRuntime(base_runtime_root, base_runtime);
    ReverifyRuntime(runtime_root, runtime, final_total_bytes);
    ReverifyPackage(runtime_package_root, package_manifest, package,
                    Field(control, "effective_runtime_package_sha256"));
    if (!SameIdentity(root_identity, FileIdentity(root.get())) ||
        !SameIdentity(parent_identity, FileIdentity(parent.get()))) Fail("root identity changed before commit");
    retained_paths.locks.check();
    WriteAll(commit_reply_write.get(), "OK\n");
    commit_reply_write.reset();

    DWORD wait = WaitForSingleObject(process_handle.get(), kCommitTimeoutMs);
    DWORD exit_code = 0;
    if (wait != WAIT_OBJECT_0 || !GetExitCodeProcess(process_handle.get(), &exit_code) || exit_code != 0) {
        Fail("verifier bootstrap result differs");
    }
    terminate_on_failure.release();
    ReverifyBaseRuntime(base_runtime_root, base_runtime);
    ReverifyRuntime(runtime_root, runtime, final_total_bytes);
    ReverifyPackage(runtime_package_root, package_manifest, package,
                    Field(control, "effective_runtime_package_sha256"));
    if (!SameIdentity(root_identity, FileIdentity(root.get()))) Fail("root identity changed after verifier exit");
    retained_paths.locks.check();
    return 0;
}

}  // namespace

int wmain(int argc, wchar_t** argv) {
    if (argc != 2 || !argv) return 64;
    try {
        HANDLE control = ParseHandleArgument(argv[1]);
        return Run(control);
    } catch (...) {
        return 70;
    }
}
