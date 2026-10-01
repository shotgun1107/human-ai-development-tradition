#include "s0_runtime_v0_5.h"
#include <aclapi.h>
#include <bcrypt.h>
#include <algorithm>
#include <cstddef>
#include <climits>
#include <cstdio>
#include <cstring>
#include <limits>
#include <memory>
#include <utility>
#include <vector>

#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "bcrypt.lib")
#pragma comment(lib, "ntdll.lib")
extern "C" NTSYSAPI NTSTATUS NTAPI NtQueryObject(
    HANDLE, OBJECT_INFORMATION_CLASS, PVOID, ULONG, PULONG);

namespace {
constexpr uint64_t kMaximumBytes = 536870912;
constexpr size_t kMaximumEntries = 2048;
constexpr size_t kMaximumFiles = 512;
constexpr size_t kMaximumText = 1024 * 1024;
constexpr const char* kBaseManifest =
    "8e151f7ad7d1bd71b8e7375fce28b86e6b614814e7702a40baf1c6e7a0d95798";
constexpr const char* kMap =
    "f6aa0f38ad7eb7bf2715fbc6084c5ce9c05db23eccca1af65956735e1e933623";
constexpr const char* kSchema =
    "04ae781b7d71e2954378cf7cdf2aa9070634ddc3a25c883ac52fb83ebe139d7e";
constexpr ACCESS_MASK kDirectoryAccess = FILE_LIST_DIRECTORY | FILE_READ_ATTRIBUTES | READ_CONTROL | SYNCHRONIZE;
constexpr ACCESS_MASK kReadAccess = FILE_READ_DATA | FILE_READ_ATTRIBUTES | READ_CONTROL | SYNCHRONIZE;

struct Failure {
    const char* stage;
    unsigned long code;
};
[[noreturn]] void Fail(const char* stage, unsigned long code = 0) { throw Failure{stage, code}; }
void Need(bool value, const char* stage) { if (!value) Fail(stage); }
void Win(bool value, const char* stage) { if (!value) { DWORD error = GetLastError(); Fail(stage, error); } }

class Handle {
    HANDLE value_ = nullptr;
  public:
    Handle() = default;
    explicit Handle(HANDLE value) : value_(value) {}
    Handle(const Handle&) = delete;
    Handle& operator=(const Handle&) = delete;
    Handle(Handle&& other) noexcept : value_(other.value_) { other.value_ = nullptr; }
    Handle& operator=(Handle&& other) noexcept {
        if (this != &other) { if (value_) CloseHandle(value_); value_ = other.value_; other.value_ = nullptr; }
        return *this;
    }
    ~Handle() { if (value_ && value_ != INVALID_HANDLE_VALUE) CloseHandle(value_); }
    HANDLE get() const { return value_; }
};
struct Search {
    HANDLE value;
    explicit Search(HANDLE input) : value(input) {}
    Search(const Search&) = delete;
    Search& operator=(const Search&) = delete;
    ~Search() { if (value != INVALID_HANDLE_VALUE) FindClose(value); }
};
struct LocalSecurity {
    PSECURITY_DESCRIPTOR value = nullptr;
    LocalSecurity() = default;
    LocalSecurity(const LocalSecurity&) = delete;
    LocalSecurity& operator=(const LocalSecurity&) = delete;
    ~LocalSecurity() { if (value) LocalFree(value); }
};

std::string Hex(const void* data, size_t size) {
    const auto* bytes = static_cast<const unsigned char*>(data);
    const char* digits = "0123456789abcdef";
    std::string result;
    result.reserve(size * 2);
    for (size_t i = 0; i < size; ++i) {
        result.push_back(digits[bytes[i] >> 4]); result.push_back(digits[bytes[i] & 15]);
    }
    return result;
}
class Hasher {
    BCRYPT_ALG_HANDLE algorithm_ = nullptr;
    BCRYPT_HASH_HANDLE hash_ = nullptr;
    std::vector<unsigned char> object_;
  public:
    Hasher() {
        NTSTATUS status = BCryptOpenAlgorithmProvider(&algorithm_, BCRYPT_SHA256_ALGORITHM, nullptr, 0);
        if (status < 0) Fail("hash-provider", static_cast<unsigned long>(status));
        DWORD length = 0, returned = 0, digest = 0;
        if (BCryptGetProperty(algorithm_, BCRYPT_OBJECT_LENGTH, reinterpret_cast<PUCHAR>(&length),
                sizeof(length), &returned, 0) < 0 || length == 0 || length > 65536 ||
            BCryptGetProperty(algorithm_, BCRYPT_HASH_LENGTH, reinterpret_cast<PUCHAR>(&digest),
                sizeof(digest), &returned, 0) < 0 || digest != 32) {
            BCryptCloseAlgorithmProvider(algorithm_, 0); algorithm_ = nullptr; Fail("hash-shape");
        }
        try { object_.resize(length); }
        catch (...) { BCryptCloseAlgorithmProvider(algorithm_, 0); algorithm_ = nullptr; throw; }
        if (BCryptCreateHash(algorithm_, &hash_, object_.data(), length, nullptr, 0, 0) < 0) {
            BCryptCloseAlgorithmProvider(algorithm_, 0); algorithm_ = nullptr; Fail("hash-create");
        }
    }
    Hasher(const Hasher&) = delete;
    Hasher& operator=(const Hasher&) = delete;
    ~Hasher() { if (hash_) BCryptDestroyHash(hash_); if (algorithm_) BCryptCloseAlgorithmProvider(algorithm_, 0); }
    void add(const void* bytes, size_t count) {
        Need(count <= (std::numeric_limits<ULONG>::max)(), "hash-input-bound");
        if (BCryptHashData(hash_, reinterpret_cast<PUCHAR>(const_cast<void*>(bytes)),
            static_cast<ULONG>(count), 0) < 0) Fail("hash-update");
    }
    std::string finish() {
        unsigned char result[32]{};
        if (BCryptFinishHash(hash_, result, sizeof(result), 0) < 0) Fail("hash-finish");
        return Hex(result, sizeof(result));
    }
};
std::string Hash(const void* bytes, size_t count) { Hasher h; h.add(bytes, count); return h.finish(); }
std::string Hash(const std::string& bytes) { return Hash(bytes.data(), bytes.size()); }
void Rewind(HANDLE handle) { LARGE_INTEGER zero{}; Win(SetFilePointerEx(handle, zero, nullptr, FILE_BEGIN) != FALSE, "seek"); }
std::string Read(HANDLE handle, size_t maximum) {
    Rewind(handle);
    std::string result;
    std::array<char, 65536> buffer{};
    for (;;) {
        DWORD got = 0;
        Win(ReadFile(handle, buffer.data(), static_cast<DWORD>(buffer.size()), &got, nullptr) != FALSE, "read");
        if (!got) break;
        Need(got <= maximum && result.size() <= maximum - got, "read-bound");
        result.append(buffer.data(), got);
    }
    Rewind(handle);
    return result;
}
std::pair<std::string, uint64_t> HashFile(HANDLE handle) {
    Rewind(handle);
    Hasher hash;
    std::array<unsigned char, 65536> bytes{};
    uint64_t total = 0;
    for (;;) {
        DWORD got = 0;
        Win(ReadFile(handle, bytes.data(), static_cast<DWORD>(bytes.size()), &got, nullptr) != FALSE, "hash-read");
        if (!got) break;
        total += got; Need(total <= kMaximumBytes, "file-byte-bound"); hash.add(bytes.data(), got);
    }
    Rewind(handle);
    return {hash.finish(), total};
}
void Write(HANDLE handle, const char* bytes, size_t count) {
    size_t offset = 0;
    while (offset < count) {
        DWORD done = 0;
        DWORD request = static_cast<DWORD>((std::min)(count - offset, size_t(65536)));
        Win(WriteFile(handle, bytes + offset, request, &done, nullptr) != FALSE, "write");
        Need(done > 0 && done <= request, "write-progress"); offset += done;
    }
}

std::string Narrow(const std::wstring& text) {
    Need(text.size() <= 32766, "path-size");
    std::string result;
    for (wchar_t c : text) { Need(c >= 32 && c <= 126, "path-ascii"); result.push_back(static_cast<char>(c)); }
    return result;
}
std::wstring Wide(const std::string& text) { return std::wstring(text.begin(), text.end()); }
std::string Fold(std::string text) {
    for (char& c : text) if (c >= 'A' && c <= 'Z') c = static_cast<char>(c - 'A' + 'a');
    return text;
}
void Virtual(const std::string& path) { try { S0CanonicalVirtual(path); } catch (...) { Fail("virtual-path"); } }
void Absolute(const std::wstring& path) { try { S0CanonicalWorkspace(Narrow(path)); } catch (...) { Fail("absolute-path"); } }
std::wstring FinalPath(HANDLE handle) {
    std::wstring value(32767, L'\0');
    DWORD count = GetFinalPathNameByHandleW(handle, value.data(), static_cast<DWORD>(value.size()),
        FILE_NAME_NORMALIZED | VOLUME_NAME_DOS);
    Win(count != 0, "final-path"); Need(count < value.size(), "final-path-bound"); value.resize(count);
    return value;
}
Handle Open(HANDLE parent, const std::wstring& name, bool directory, bool create, bool write = false) {
    Need(!name.empty() && name.size() < 32767 && name.size() <= USHRT_MAX / sizeof(wchar_t), "nt-name-bound");
    UNICODE_STRING unicode{};
    unicode.Buffer = const_cast<wchar_t*>(name.data());
    unicode.Length = static_cast<USHORT>(name.size() * sizeof(wchar_t)); unicode.MaximumLength = unicode.Length;
    OBJECT_ATTRIBUTES attributes{};
    InitializeObjectAttributes(&attributes, &unicode, OBJ_CASE_INSENSITIVE | 0x1000, parent, nullptr);
    IO_STATUS_BLOCK io{};
    HANDLE raw = nullptr;
    ACCESS_MASK access = directory ? kDirectoryAccess : kReadAccess;
    if (write) access |= FILE_WRITE_DATA;
    const ULONG options = FILE_SYNCHRONOUS_IO_NONALERT | FILE_OPEN_REPARSE_POINT |
        (directory ? FILE_DIRECTORY_FILE : FILE_NON_DIRECTORY_FILE);
    NTSTATUS status = NtCreateFile(&raw, access, &attributes, &io, nullptr,
        directory ? FILE_ATTRIBUTE_DIRECTORY : FILE_ATTRIBUTE_NORMAL, FILE_SHARE_READ,
        create ? FILE_CREATE : FILE_OPEN, options, nullptr, 0);
    Handle result(raw);
    if (status != 0 || io.Status != status || !raw || raw == INVALID_HANDLE_VALUE ||
        (create && io.Information != 2)) Fail(create ? "relative-create" : "relative-open", static_cast<unsigned long>(status));
    return result;
}

struct ObjectBasic {
    ULONG attributes; ACCESS_MASK granted_access; ULONG handle_count; ULONG pointer_count;
    ULONG paged_pool_charge; ULONG nonpaged_pool_charge; ULONG reserved[3];
    ULONG name_length; ULONG type_length; ULONG security_length; LARGE_INTEGER created;
};
void Access(HANDLE handle, ACCESS_MASK expected) {
    ObjectBasic basic{}; ULONG returned = 0;
    NTSTATUS status = NtQueryObject(handle, ObjectBasicInformation, &basic, sizeof(basic), &returned);
    Need(status >= 0 && returned >= offsetof(ObjectBasic, created) && basic.granted_access == expected, "granted-access");
}
size_t SidSize(PSID sid) {
    Need(sid != nullptr, "token-sid");
    const auto* value = static_cast<const SID*>(sid);
    Need(value->Revision == SID_REVISION && value->SubAuthorityCount <= SID_MAX_SUB_AUTHORITIES, "sid-shape");
    return 8 + size_t(value->SubAuthorityCount) * sizeof(DWORD);
}
HANDLE EffectiveToken() { return reinterpret_cast<HANDLE>(static_cast<INT_PTR>(-6)); }
std::string Token() {
    TOKEN_STATISTICS stats{}; DWORD returned = 0;
    Win(GetTokenInformation(EffectiveToken(), TokenStatistics, &stats, sizeof(stats), &returned) != FALSE, "effective-token-statistics");
    Need(returned == sizeof(stats), "token-statistics-size");
    std::array<unsigned char, 4096> buffer{};
    Win(GetTokenInformation(EffectiveToken(), TokenUser, buffer.data(), static_cast<DWORD>(buffer.size()), &returned) != FALSE, "effective-token-user");
    Need(returned >= sizeof(TOKEN_USER) && returned <= buffer.size(), "token-user-size");
    const auto* user = reinterpret_cast<const TOKEN_USER*>(buffer.data());
    const auto* sid = static_cast<const unsigned char*>(user->User.Sid);
    Need(sid >= buffer.data() && sid + 8 <= buffer.data() + returned, "token-sid-range");
    size_t count = SidSize(user->User.Sid);
    Need(sid + count <= buffer.data() + returned, "token-sid-bound");
    Hasher h; h.add(&stats, sizeof(stats)); h.add(sid, count); return h.finish();
}
std::string Security(HANDLE handle, ACCESS_MASK requested) {
    LocalSecurity security;
    DWORD status = GetSecurityInfo(handle, SE_FILE_OBJECT,
        OWNER_SECURITY_INFORMATION | GROUP_SECURITY_INFORMATION | DACL_SECURITY_INFORMATION,
        nullptr, nullptr, nullptr, nullptr, &security.value);
    if (status != ERROR_SUCCESS) Fail("security-descriptor", status);
    Need(security.value != nullptr, "security-buffer");
    const auto* relative = static_cast<const SECURITY_DESCRIPTOR_RELATIVE*>(security.value);
    Need(relative->Revision == SECURITY_DESCRIPTOR_REVISION && (relative->Control & SE_SELF_RELATIVE), "security-relative");
    size_t length = sizeof(SECURITY_DESCRIPTOR_RELATIVE);
    const auto* bytes = static_cast<const unsigned char*>(security.value);
    for (DWORD offset : {relative->Owner, relative->Group}) {
        if (!offset) continue;
        Need(offset >= sizeof(*relative) && offset < 65536 - 68, "security-sid-offset");
        size_t count = SidSize(const_cast<unsigned char*>(bytes + offset));
        length = (std::max)(length, size_t(offset) + count);
    }
    for (DWORD offset : {relative->Dacl, relative->Sacl}) {
        if (!offset) continue;
        Need(offset >= sizeof(*relative) && offset < 65536 - sizeof(ACL), "security-acl-offset");
        const auto* acl = reinterpret_cast<const ACL*>(bytes + offset);
        Need(acl->AclSize >= sizeof(ACL) && size_t(offset) + acl->AclSize <= 65536, "security-acl-bound");
        length = (std::max)(length, size_t(offset) + acl->AclSize);
    }
    GENERIC_MAPPING mapping{FILE_GENERIC_READ, FILE_GENERIC_WRITE, FILE_GENERIC_EXECUTE, FILE_ALL_ACCESS};
    std::array<unsigned char, 4096> privileges{};
    DWORD privilege_size = static_cast<DWORD>(privileges.size()), granted = 0; BOOL allowed = FALSE;
    Win(AccessCheck(security.value, EffectiveToken(), requested, &mapping,
        reinterpret_cast<PPRIVILEGE_SET>(privileges.data()), &privilege_size, &granted, &allowed) != FALSE, "effective-access-check");
    Need(allowed != FALSE && (granted & requested) == requested, "effective-access-denied");
    return Hash(bytes, length);
}

struct Measurement {
    FILE_ID_INFO identity{};
    bool directory = false;
    std::string security;
    std::string token;
    std::wstring final_path;
};
bool SameId(const FILE_ID_INFO& a, const FILE_ID_INFO& b) {
    return a.VolumeSerialNumber == b.VolumeSerialNumber &&
        memcmp(a.FileId.Identifier, b.FileId.Identifier, 16) == 0;
}
std::string Id(const FILE_ID_INFO& value) { return Hex(&value.VolumeSerialNumber, 8) + ":" + Hex(value.FileId.Identifier, 16); }
Measurement Measure(HANDLE handle, bool directory, bool writable) {
    Measurement result{}; result.directory = directory;
    FILE_ID_INFO second{}; FILE_ATTRIBUTE_TAG_INFO tag{}; FILE_STANDARD_INFO standard{};
    Win(GetFileInformationByHandleEx(handle, FileIdInfo, &result.identity, sizeof(result.identity)) != FALSE, "file-id");
    Win(GetFileInformationByHandleEx(handle, FileIdInfo, &second, sizeof(second)) != FALSE, "file-id-second");
    Win(GetFileInformationByHandleEx(handle, FileAttributeTagInfo, &tag, sizeof(tag)) != FALSE, "file-tag");
    Win(GetFileInformationByHandleEx(handle, FileStandardInfo, &standard, sizeof(standard)) != FALSE, "file-standard");
    Need(SameId(result.identity, second) && result.identity.VolumeSerialNumber != 0 &&
        static_cast<bool>(standard.Directory) == directory && standard.NumberOfLinks == 1 && !standard.DeletePending &&
        static_cast<bool>(tag.FileAttributes & FILE_ATTRIBUTE_DIRECTORY) == directory &&
        !(tag.FileAttributes & FILE_ATTRIBUTE_REPARSE_POINT) && tag.ReparseTag == 0, "file-object");
    wchar_t fs[32]{}; DWORD serial = 0;
    Win(GetVolumeInformationByHandleW(handle, nullptr, 0, &serial, nullptr, nullptr, fs, 32) != FALSE, "volume-information");
    Need(std::wstring(fs) == L"NTFS" && serial == static_cast<DWORD>(result.identity.VolumeSerialNumber), "fixed-ntfs-volume");
    result.final_path = FinalPath(handle);
    Need(result.final_path.size() >= 7 && result.final_path.substr(0, 4) == L"\\\\?\\" &&
        result.final_path[5] == L':' && result.final_path[6] == L'\\', "volume-drive-shape");
    std::wstring drive = result.final_path.substr(4, 3);
    Need(GetDriveTypeW(drive.c_str()) == DRIVE_FIXED, "fixed-drive");
    ACCESS_MASK access = directory ? kDirectoryAccess : kReadAccess;
    if (writable) access |= FILE_WRITE_DATA;
    Access(handle, access);
    result.token = Token(); result.security = Security(handle, access);
    Need(result.token == Token(), "token-changing-during-access");
    return result;
}
struct Node {
    Handle handle;
    Measurement before;
    bool writable = false;
    Node(Handle h, bool directory, bool write = false) : handle(std::move(h)), before(Measure(handle.get(), directory, write)), writable(write) {}
    Node(Node&&) = default;
    Node& operator=(Node&&) = default;
    Node(const Node&) = delete;
    void check() const {
        Measurement after = Measure(handle.get(), before.directory, writable);
        Need(SameId(before.identity, after.identity) && before.security == after.security &&
            before.token == after.token && before.final_path == after.final_path, "retained-identity-acl-token-change");
    }
};
using Nodes = std::vector<std::unique_ptr<Node>>;
struct Path {
    Nodes chain;
    Node& leaf() const { return *chain.back(); }
};
Path BindPath(const std::wstring& absolute, bool directory = true) {
    Absolute(absolute);
    Path result;
    std::wstring root = L"\\??\\" + absolute.substr(0, 3);
    result.chain.push_back(std::make_unique<Node>(Open(nullptr, root, true, false), true));
    size_t start = 3;
    while (start < absolute.size()) {
        size_t end = absolute.find(L'\\', start); if (end == std::wstring::npos) end = absolute.size();
        Need(result.chain.size() < 256, "ancestry-depth");
        bool is_directory = end != absolute.size() || directory;
        result.chain.push_back(std::make_unique<Node>(Open(result.leaf().handle.get(),
            absolute.substr(start, end - start), is_directory, false), is_directory));
        Need(result.chain.front()->before.identity.VolumeSerialNumber == result.leaf().before.identity.VolumeSerialNumber, "cross-volume-ancestor");
        start = end + 1;
    }
    Need(result.leaf().before.directory == directory, "path-kind");
    for (const auto& node : result.chain) node->check();
    return result;
}
void Check(const Path& path) { for (const auto& node : path.chain) node->check(); }
Path BindParent(const std::wstring& absolute, std::wstring& leaf) {
    Absolute(absolute); Need(absolute.size() > 3, "output-is-volume-root");
    size_t slash = absolute.rfind(L'\\'); leaf = absolute.substr(slash + 1);
    Virtual(Narrow(leaf));
    return BindPath(slash == 2 ? absolute.substr(0, 3) : absolute.substr(0, slash));
}

struct Json {
    enum Kind { Object, Array, String, Number } kind = Object;
    std::map<std::string, Json> object;
    std::vector<Json> array;
    std::string text;
    uint64_t number = 0;
    Json() = default;
    explicit Json(std::string value) : kind(String), text(std::move(value)) {}
    explicit Json(uint64_t value) : kind(Number), number(value) {}
    const Json& at(const std::string& key) const {
        auto it = object.find(key); Need(kind == Object && it != object.end(), "json-required"); return it->second;
    }
    const std::string& str() const { Need(kind == String, "json-string-kind"); return text; }
    uint64_t num() const { Need(kind == Number, "json-number-kind"); return number; }
    void keys(std::initializer_list<const char*> names) const {
        Need(kind == Object && object.size() == names.size(), "json-exact-keys");
        for (const char* name : names) (void)at(name);
    }
};
std::string Quote(const std::string& value) {
    std::string raw = "\"";
    for (unsigned char c : value) {
        Need(c >= 32 && c <= 126, "json-ascii");
        if (c == '\\' || c == '"') raw.push_back('\\');
        raw.push_back(static_cast<char>(c));
    }
    return raw + '"';
}
std::string Encode(const Json& value) {
    if (value.kind == Json::String) return Quote(value.text);
    if (value.kind == Json::Number) return std::to_string(value.number);
    std::string result = value.kind == Json::Array ? "[" : "{";
    bool first = true;
    if (value.kind == Json::Array) for (const Json& row : value.array) {
        if (!first) result += ','; first = false; result += Encode(row);
    } else for (const auto& row : value.object) {
        if (!first) result += ','; first = false; result += Quote(row.first) + ":" + Encode(row.second);
    }
    return result + (value.kind == Json::Array ? "]" : "}");
}
class Parser {
    const std::string& raw_; size_t offset_ = 0; size_t nodes_ = 0;
    char take() { Need(offset_ < raw_.size(), "json-partial"); return raw_[offset_++]; }
    std::string string() {
        Need(take() == '"', "json-string"); std::string result;
        for (;;) {
            char c = take(); if (c == '"') return result;
            if (c == '\\') { c = take(); Need(c == '"' || c == '\\', "json-escape"); }
            Need(c >= 32 && c <= 126 && result.size() < 32766, "json-string-byte"); result += c;
        }
    }
    Json value(unsigned depth) {
        Need(depth < 32 && ++nodes_ <= 16384 && offset_ < raw_.size(), "json-resource");
        Json result; char c = raw_[offset_];
        if (c == '"') return Json(string());
        if (c >= '0' && c <= '9') {
            result.kind = Json::Number; do {
                unsigned d = static_cast<unsigned>(take() - '0');
                Need(result.number <= (UINT64_MAX - d) / 10, "json-number-overflow");
                result.number = result.number * 10 + d;
            } while (offset_ < raw_.size() && raw_[offset_] >= '0' && raw_[offset_] <= '9');
            return result;
        }
        Need(c == '{' || c == '[', "json-value");
        ++offset_; result.kind = c == '{' ? Json::Object : Json::Array;
        char end = c == '{' ? '}' : ']';
        if (offset_ < raw_.size() && raw_[offset_] == end) { ++offset_; return result; }
        for (;;) {
            if (result.kind == Json::Object) {
                std::string key = string(); Need(take() == ':', "json-colon");
                Need(result.object.emplace(key, value(depth + 1)).second, "json-duplicate");
            } else result.array.push_back(value(depth + 1));
            char separator = take(); if (separator == end) return result; Need(separator == ',', "json-separator");
        }
    }
  public:
    explicit Parser(const std::string& raw) : raw_(raw) {}
    Json parse() {
        Need(raw_.size() <= kMaximumText, "json-byte-bound"); Json result = value(0);
        Need(offset_ + 1 == raw_.size() && raw_[offset_] == '\n' && Encode(result) + "\n" == raw_, "json-canonical");
        return result;
    }
};

struct Entry {
    std::string path, sha;
    uint64_t size = 0;
};
using Rows = std::map<std::string, Entry>;
Rows Manifest(const std::string& raw, size_t expected) {
    Need(!raw.empty() && raw.back() == '\n' && expected > 0 && expected <= kMaximumFiles, "manifest-frame");
    Rows rows; std::set<std::string> folded; size_t start = 0; std::string previous;
    while (start < raw.size()) {
        size_t end = raw.find('\n', start); Need(end != std::string::npos && end - start >= 67, "manifest-row");
        std::string digest = raw.substr(start, 64), path = raw.substr(start + 66, end - start - 66);
        Need(raw.substr(start + 64, 2) == "  " && S0LowerHex(digest, 64), "manifest-digest");
        Virtual(path); Need(path > previous && folded.insert(Fold(path)).second && rows.size() < kMaximumFiles, "manifest-order-alias");
        rows.emplace(path, Entry{path, digest, 0}); previous = path; start = end + 1;
    }
    Need(rows.size() == expected, "manifest-count"); return rows;
}
Rows BaseRows(const std::string& raw) {
    Need(Hash(raw) == kBaseManifest, "base-manifest-pin");
    Json value = Parser(raw).parse();
    value.keys({"file_count","files","python_stdlib_zip","schema_id","total_bytes"});
    Need(value.at("file_count").num() == 174 && value.at("total_bytes").num() == 24138847 &&
        value.at("schema_id").str() == "S0-PUBLIC-BRM-V0.7-PAYLOAD-MANIFEST-1", "base-manifest-shape");
    value.at("python_stdlib_zip").keys({"entry_count","uncompressed_bytes"});
    Need(value.at("python_stdlib_zip").at("entry_count").num() > 0 &&
        value.at("python_stdlib_zip").at("uncompressed_bytes").num() > 0, "base-stdlib");
    Need(value.at("files").kind == Json::Array && value.at("files").array.size() == 174, "base-rows");
    Rows result; std::set<std::string> folded; std::string previous; uint64_t total = 0;
    for (const Json& row : value.at("files").array) {
        row.keys({"path","provenance_pin_id","sha256","size"});
        std::string path = row.at("path").str(), digest = row.at("sha256").str();
        Virtual(path); Need(path > previous && path.rfind("evidence/", 0) != 0 &&
            folded.insert(Fold(path)).second && S0LowerHex(digest, 64), "base-row");
        Need(!row.at("provenance_pin_id").str().empty(), "base-provenance");
        uint64_t size = row.at("size").num(); Need(size <= kMaximumBytes - total, "base-size-bound"); total += size;
        result.emplace(path, Entry{path, digest, size}); previous = path;
    }
    Need(total == 24138847, "base-total"); return result;
}

std::vector<std::pair<std::wstring, FILE_ID_128>> DirectoryEntries(HANDLE handle) {
    std::vector<std::pair<std::wstring, FILE_ID_128>> result;
    std::array<unsigned char, 65536> buffer{};
    bool first = true;
    for (;;) {
        BOOL ok = GetFileInformationByHandleEx(handle, first ? FileIdExtdDirectoryRestartInfo : FileIdExtdDirectoryInfo,
            buffer.data(), static_cast<DWORD>(buffer.size()));
        first = false;
        if (!ok) { DWORD error = GetLastError(); if (error == ERROR_NO_MORE_FILES) break; Fail("handle-enumeration", error); }
        size_t offset = 0;
        for (;;) {
            Need(offset <= buffer.size() - offsetof(FILE_ID_EXTD_DIR_INFO, FileName), "directory-entry-bound");
            const auto* row = reinterpret_cast<const FILE_ID_EXTD_DIR_INFO*>(buffer.data() + offset);
            Need(row->FileNameLength % 2 == 0 && row->FileNameLength <= buffer.size() - offset - offsetof(FILE_ID_EXTD_DIR_INFO, FileName), "directory-name-bound");
            std::wstring name(row->FileName, row->FileNameLength / 2);
            if (name != L"." && name != L"..") {
                Need(result.size() < kMaximumEntries, "directory-entry-count");
                result.emplace_back(name, row->FileId);
            }
            if (!row->NextEntryOffset) break;
            Need(row->NextEntryOffset >= offsetof(FILE_ID_EXTD_DIR_INFO, FileName) &&
                row->NextEntryOffset <= buffer.size() - offset, "directory-next-bound");
            offset += row->NextEntryOffset;
        }
    }
    std::sort(result.begin(), result.end(), [](const auto& a, const auto& b) { return a.first < b.first; });
    for (size_t i = 1; i < result.size(); ++i) Need(result[i-1].first != result[i].first, "directory-duplicate");
    return result;
}
void Streams(Node& node) {
    node.check();
    std::array<unsigned char, 65536> buffer{};
    std::vector<std::wstring> authoritative;
    BOOL ok = GetFileInformationByHandleEx(node.handle.get(), FileStreamInfo, buffer.data(), static_cast<DWORD>(buffer.size()));
    if (!ok) {
        DWORD error = GetLastError();
        Need(node.before.directory && (error == ERROR_HANDLE_EOF || error == ERROR_NO_MORE_FILES), "stream-query");
    } else {
        size_t offset = 0;
        for (;;) {
            Need(offset <= buffer.size() - offsetof(FILE_STREAM_INFO, StreamName), "stream-bound");
            const auto* row = reinterpret_cast<const FILE_STREAM_INFO*>(buffer.data() + offset);
            Need(row->StreamNameLength % 2 == 0 && row->StreamNameLength <= buffer.size() - offset - offsetof(FILE_STREAM_INFO, StreamName), "stream-name-bound");
            std::wstring name(row->StreamName, row->StreamNameLength / 2);
            Need(name == L"::$DATA" && authoritative.empty(), "alternate-data-stream");
            authoritative.push_back(name);
            if (!row->NextEntryOffset) break;
            Need(row->NextEntryOffset >= offsetof(FILE_STREAM_INFO, StreamName) && row->NextEntryOffset <= buffer.size() - offset, "stream-next-bound");
            offset += row->NextEntryOffset;
        }
    }
    WIN32_FIND_STREAM_DATA data{};
    HANDLE raw = FindFirstStreamW(node.before.final_path.c_str(), FindStreamInfoStandard, &data, 0);
    std::vector<std::wstring> discovered;
    if (raw == INVALID_HANDLE_VALUE) {
        DWORD error = GetLastError();
        Need(authoritative.empty() && (error == ERROR_HANDLE_EOF || error == ERROR_NO_MORE_FILES), "stream-discovery");
    } else {
        Search search(raw);
        for (;;) {
            Need(discovered.empty() && std::wstring(data.cStreamName) == L"::$DATA", "stream-discovery-ads");
            discovered.emplace_back(data.cStreamName);
            if (!FindNextStreamW(search.value, &data)) {
                DWORD error = GetLastError(); Need(error == ERROR_HANDLE_EOF || error == ERROR_NO_MORE_FILES, "stream-discovery-end"); break;
            }
        }
    }
    Need(discovered == authoritative, "stream-discovery-disagrees"); node.check();
}
void Discover(Node& directory, const std::vector<std::pair<std::wstring, FILE_ID_128>>& authoritative) {
    directory.check();
    WIN32_FIND_DATAW data{}; std::vector<std::wstring> names;
    HANDLE raw = FindFirstFileW((directory.before.final_path + L"\\*").c_str(), &data);
    if (raw == INVALID_HANDLE_VALUE) {
        DWORD error = GetLastError(); Need(error == ERROR_FILE_NOT_FOUND && authoritative.empty(), "name-discovery");
    } else {
        Search search(raw);
        for (;;) {
            std::wstring name(data.cFileName);
            if (name != L"." && name != L"..") {
                Need(names.size() < kMaximumEntries, "name-discovery-bound"); names.push_back(name);
            }
            if (!FindNextFileW(search.value, &data)) { DWORD error = GetLastError(); Need(error == ERROR_NO_MORE_FILES, "name-discovery-end"); break; }
        }
    }
    std::sort(names.begin(), names.end()); Need(names.size() == authoritative.size(), "name-discovery-count");
    for (size_t i = 0; i < names.size(); ++i) Need(names[i] == authoritative[i].first, "name-discovery-disagrees");
    directory.check();
}
struct Tree {
    Node* root;
    std::map<std::string, std::unique_ptr<Node>> children;
    Rows rows;
    explicit Tree(Node& value) : root(&value) {}
    Node& node(const std::string& path) { if (path.empty()) return *root; return *children.at(path); }
    void scan(const Rows& expected, const std::string& prefix = "") {
        Node& parent = node(prefix); Streams(parent);
        auto entries = DirectoryEntries(parent.handle.get()); Discover(parent, entries);
        std::set<std::string> folded;
        for (const auto& entry : entries) {
            std::string name = Narrow(entry.first); Virtual(name);
            Need(name.find('/') == std::string::npos && folded.insert(Fold(name)).second, "entry-name-alias");
            std::string path = prefix.empty() ? name : prefix + "/" + name;
            auto file = expected.find(path);
            bool directory = file == expected.end();
            if (directory) {
                auto descendant = expected.lower_bound(path + "/");
                Need(descendant != expected.end() && descendant->first.rfind(path + "/", 0) == 0, "unlisted-directory");
            }
            Need(children.size() < kMaximumEntries, "tree-bound");
            auto child = std::make_unique<Node>(Open(parent.handle.get(), entry.first, directory, false), directory);
            Need(memcmp(child->before.identity.FileId.Identifier, entry.second.Identifier, 16) == 0 &&
                child->before.identity.VolumeSerialNumber == root->before.identity.VolumeSerialNumber, "enumerated-object-rebound");
            Streams(*child);
            if (!directory) {
                auto digest = HashFile(child->handle.get());
                Need(digest.first == file->second.sha && (file->second.size == UINT64_MAX || digest.second == file->second.size), "input-file-hash-size");
                rows.emplace(path, Entry{path, digest.first, digest.second});
            }
            children.emplace(path, std::move(child));
            if (directory) scan(expected, path);
        }
        parent.check();
        if (prefix.empty()) Need(rows.size() == expected.size(), "input-inventory-incomplete");
    }
    void check(const Rows& expected) {
        root->check();
        for (auto& row : children) { row.second->check(); Streams(*row.second); }
        std::vector<std::string> directories{""};
        for (const auto& row : children) if (row.second->before.directory) directories.push_back(row.first);
        for (const auto& dir : directories) {
            Node& parent = node(dir); auto entries = DirectoryEntries(parent.handle.get()); Discover(parent, entries);
            size_t count = 0;
            for (const auto& row : children) {
                size_t slash = row.first.rfind('/');
                std::string parent_path = slash == std::string::npos ? "" : row.first.substr(0, slash);
                if (parent_path == dir) ++count;
            }
            Need(entries.size() == count, "terminal-directory-count");
            for (const auto& entry : entries) {
                std::string path = dir.empty() ? Narrow(entry.first) : dir + "/" + Narrow(entry.first);
                auto found = children.find(path); Need(found != children.end(), "terminal-unlisted");
                Need(memcmp(found->second->before.identity.FileId.Identifier, entry.second.Identifier, 16) == 0, "terminal-object-rebound");
            }
        }
        for (const auto& row : expected) {
            auto hash = HashFile(node(row.first).handle.get());
            Need(hash.first == row.second.sha && hash.second == row.second.size, "terminal-file-change");
        }
    }
    Node& create(const std::string& path, bool directory) {
        Virtual(path); size_t slash = path.rfind('/');
        std::string parent_path = slash == std::string::npos ? "" : path.substr(0, slash);
        if (!parent_path.empty() && children.find(parent_path) == children.end()) create(parent_path, true);
        Need(children.size() < kMaximumEntries && children.find(path) == children.end(), "create-duplicate-bound");
        std::string leaf = slash == std::string::npos ? path : path.substr(slash + 1);
        auto child = std::make_unique<Node>(Open(node(parent_path).handle.get(), Wide(leaf), directory, true, !directory), directory, !directory);
        Node* value = child.get(); children.emplace(path, std::move(child)); return *value;
    }
    void bytes(const std::string& path, const std::string& raw) {
        Node& child = create(path, false);
        Write(child.handle.get(), raw.data(), raw.size()); Win(FlushFileBuffers(child.handle.get()) != FALSE, "flush-evidence");
        Need(Read(child.handle.get(), kMaximumText) == raw, "evidence-readback");
        rows.emplace(path, Entry{path, Hash(raw), raw.size()});
    }
    void copy(const std::string& path, Node& source, const Entry& expected) {
        Node& output = create(path, false); source.check(); Rewind(source.handle.get());
        std::array<char, 65536> buffer{}; uint64_t count = 0;
        for (;;) {
            DWORD got = 0;
            Win(ReadFile(source.handle.get(), buffer.data(), static_cast<DWORD>(buffer.size()), &got, nullptr) != FALSE, "copy-read");
            if (!got) break;
            Need(got <= expected.size - count, "copy-size"); count += got;
            Write(output.handle.get(), buffer.data(), got);
        }
        Win(FlushFileBuffers(output.handle.get()) != FALSE, "flush-copy");
        auto digest = HashFile(output.handle.get());
        Need(count == expected.size && digest.second == expected.size && digest.first == expected.sha, "copy-readback");
        source.check(); rows.emplace(path, Entry{path, expected.sha, expected.size});
    }
};

std::map<std::string, std::wstring> Arguments(int argc, wchar_t** argv) {
    Need(argc == 33 && argv != nullptr, "argument-count");
    std::map<std::string, std::wstring> values;
    const std::set<std::string> names = {"--base-root","--base-manifest","--overlay-root","--overlay-manifest",
        "--overlay-sha256","--overlay-contract","--contract-sha256","--repository-root","--output-root",
        "--final-manifest","--producer-path","--producer-sha256","--run-nonce","--external-pin-digest",
        "--build-trace","--build-trace-sha256"};
    for (int i = 1; i < argc; i += 2) {
        std::string name = Narrow(argv[i]); Need(names.count(name) == 1 && values.emplace(name, argv[i+1]).second, "argument-name");
    }
    Need(values.size() == names.size(), "argument-exact-set");
    for (const char* name : {"--overlay-sha256","--contract-sha256","--producer-sha256","--run-nonce","--external-pin-digest","--build-trace-sha256"})
        Need(S0LowerHex(Narrow(values.at(name)), 64), "argument-hash");
    return values;
}
void Exclude(const Path& output, const Path& base, const Path& repository, const Path& overlay) {
    for (const auto& node : output.chain)
        for (const Path* denied : {&base, &repository, &overlay})
            Need(!SameId(node->before.identity, denied->leaf().before.identity), "physical-output-overlap");
}
int Run(int argc, wchar_t** argv) {
    auto args = Arguments(argc, argv);
    Path base = BindPath(args.at("--base-root")), repository = BindPath(args.at("--repository-root"));
    Path overlay = BindPath(args.at("--overlay-root"));
    Need(!SameId(base.leaf().before.identity, overlay.leaf().before.identity), "base-overlay-identity");
    for (const auto& node : overlay.chain) Need(!SameId(node->before.identity, base.leaf().before.identity), "overlay-under-base");
    for (const auto& node : base.chain) Need(!SameId(node->before.identity, overlay.leaf().before.identity), "base-under-overlay");
    Path base_manifest = BindPath(args.at("--base-manifest"), false);
    Path overlay_manifest = BindPath(args.at("--overlay-manifest"), false);
    Path contract_file = BindPath(args.at("--overlay-contract"), false);
    Path producer = BindPath(args.at("--producer-path"), false);
    Path trace = BindPath(args.at("--build-trace"), false);
    Need(HashFile(producer.leaf().handle.get()).first == Narrow(args.at("--producer-sha256")), "producer-pin");
    std::string trace_raw = Read(trace.leaf().handle.get(), kMaximumText);
    Need(Hash(trace_raw) == Narrow(args.at("--build-trace-sha256")), "build-trace-pin");
    Json trace_value = Parser(trace_raw).parse();
    Need(trace_value.at("schema_id").str() == "S0-RUNTIME-PRELOADER-V0.5-BUILD-TRACE-1" &&
        trace_value.at("effective_interface_map_sha256").str() == kMap &&
        trace_value.at("effective_schema_sha256").str() == kSchema &&
        trace_value.at("compiler").at("sha256").str() == "88c8344236a27a6e727e0a8edc49aaa2690bdc7a9464b9d18cc7abe70a9f1c0d" &&
        trace_value.at("linker").at("sha256").str() == "ca11e6c45debd34bf652dfe984c5360a531a005ed78bf72852330c9c2590cf0d",
        "build-provenance");
    Need(trace_value.at("outputs").kind == Json::Array && trace_value.at("outputs").array.size() == 3, "build-output-set");
    size_t producer_matches = 0;
    for (const Json& row : trace_value.at("outputs").array)
        if (row.at("filename").str() == "s0_runtime_materializer_v0_5.exe") {
            Need(row.at("sha256").str() == Narrow(args.at("--producer-sha256")), "producer-build-binding");
            ++producer_matches;
        }
    Need(producer_matches == 1, "producer-build-count");
    std::string contract_raw = Read(contract_file.leaf().handle.get(), kMaximumText);
    Need(Hash(contract_raw) == Narrow(args.at("--contract-sha256")), "overlay-contract-pin");
    Json contract = Parser(contract_raw).parse();
    contract.keys({"overlay_file_count","overlay_manifest_sha256","overlay_total_bytes","platform_evidence_state","required_rows","schema_id"});
    Need(contract.at("schema_id").str() == "S0-RUNTIME-PRELOADER-V0.4-OVERLAY-CONTRACT-1" &&
        contract.at("platform_evidence_state").str() == "explicitly-pinned-unverified-until-stage70" &&
        contract.at("overlay_manifest_sha256").str() == Narrow(args.at("--overlay-sha256")) &&
        contract.at("overlay_file_count").num() > 0 && contract.at("overlay_file_count").num() <= kMaximumFiles - 174 &&
        contract.at("overlay_total_bytes").num() > 0 && contract.at("overlay_total_bytes").num() <= kMaximumBytes - 24138847, "overlay-contract-shape");
    std::string overlay_raw = Read(overlay_manifest.leaf().handle.get(), kMaximumText);
    Need(Hash(overlay_raw) == Narrow(args.at("--overlay-sha256")), "overlay-manifest-pin");
    Rows overlay_rows = Manifest(overlay_raw, static_cast<size_t>(contract.at("overlay_file_count").num()));
    for (auto& row : overlay_rows) row.second.size = UINT64_MAX;
    const std::set<std::string> classes = {"admitted-system-image","bounded-integration-adapter","loaded-pe-manifest","native-guard",
        "native-preloader","platform-manifest","pre-import-bootstrap","public-assembly-verifier","runtime-preloader-python"};
    std::set<std::string> seen_classes, classified;
    Need(contract.at("required_rows").kind == Json::Array, "overlay-required-array");
    for (const Json& row : contract.at("required_rows").array) {
        row.keys({"class","path","sha256"});
        std::string path = row.at("path").str(), category = row.at("class").str();
        Need(classes.count(category) == 1 && classified.insert(path).second && overlay_rows.count(path) == 1 &&
            overlay_rows.at(path).sha == row.at("sha256").str(), "overlay-classification");
        seen_classes.insert(category);
    }
    Need(seen_classes == classes && classified.size() == overlay_rows.size(), "overlay-class-closure");
    Rows payload = BaseRows(Read(base_manifest.leaf().handle.get(), kMaximumText));
    Rows base_rows = payload;
    const std::map<std::string, std::string> evidence = {
        {"evidence/payload-manifest.json", kBaseManifest},
        {"evidence/prepublication-record.json","0281893dce01d1aa54a1ad16cd621786615340844fcec35940095768e7dda9ca"},
        {"evidence/runtime-record.json","5d6b61194b5a7f0e53aeb78ac0bdee40f6edea294adecb0f8a7462751f6e6a84"},
        {"evidence/status.json","c8878e9df9d8c5979517efa3a9495b8e65c640b6f2c195fff029def6c262bbc6"}};
    for (const auto& row : evidence) {
        base_rows.emplace(row.first, Entry{row.first, row.second, UINT64_MAX});
        std::string sidecar = row.second + "  " + row.first.substr(row.first.rfind('/') + 1) + "\n";
        base_rows.emplace(row.first + ".sha256", Entry{row.first + ".sha256", Hash(sidecar), sidecar.size()});
    }
    Tree base_tree(base.leaf()); base_tree.scan(base_rows); base_rows = base_tree.rows;
    Need(SameId(base_manifest.leaf().before.identity, base_tree.node("evidence/payload-manifest.json").before.identity), "base-manifest-object");
    Tree overlay_tree(overlay.leaf()); overlay_tree.scan(overlay_rows); overlay_rows = overlay_tree.rows;
    uint64_t overlay_bytes = 0; Rows final_rows = payload; std::set<std::string> final_folded;
    for (const auto& row : payload) final_folded.insert(Fold(row.first));
    for (const auto& row : overlay_rows) {
        Need(final_folded.insert(Fold(row.first)).second && final_rows.emplace(row).second, "overlay-overwrite-or-alias");
        Need(row.second.size <= kMaximumBytes - overlay_bytes, "overlay-byte-bound"); overlay_bytes += row.second.size;
    }
    Need(overlay_bytes == contract.at("overlay_total_bytes").num() && final_rows.size() <= kMaximumFiles, "overlay-total");
    std::wstring leaf;
    Path output_parent = BindParent(args.at("--output-root"), leaf);
    Exclude(output_parent, base, repository, overlay);
    Need(args.at("--final-manifest") == args.at("--output-root") + L"\\evidence\\runtime-files.sha256", "final-manifest-retained-root-policy");
    for (Path* input : {&base, &repository, &overlay, &base_manifest, &overlay_manifest, &contract_file, &producer, &trace}) Check(*input);
    Check(output_parent);
    Node output(Open(output_parent.leaf().handle.get(), leaf, true, true), true);
    for (const Path* denied : {&base, &repository, &overlay})
        for (const auto& ancestor : denied->chain)
            Need(!SameId(output.before.identity, ancestor->before.identity), "output-physical-alias");
    HANDLE duplicate_raw = nullptr;
    Win(DuplicateHandle(reinterpret_cast<HANDLE>(static_cast<INT_PTR>(-1)), output.handle.get(),
        reinterpret_cast<HANDLE>(static_cast<INT_PTR>(-1)), &duplicate_raw, kDirectoryAccess, FALSE, 0) != FALSE, "retained-root-duplicate");
    Node duplicate(Handle(duplicate_raw), true);
    Need(SameId(output.before.identity, duplicate.before.identity), "retained-root-duplicate-identity");
    Tree output_tree(output);
    output_tree.create("runtime", true); output_tree.create("evidence", true);
    for (const auto& row : final_rows) {
        Tree& input = payload.count(row.first) ? base_tree : overlay_tree;
        output_tree.copy("runtime/" + row.first, input.node(row.first), row.second);
    }
    std::string manifest;
    for (const auto& row : final_rows) manifest += row.second.sha + "  " + row.first + "\n";
    output_tree.bytes("evidence/runtime-files.sha256", manifest);
    output_tree.bytes("evidence/runtime-files.sha256.sha256", Hash(manifest) + "  runtime-files.sha256\n");
    base_tree.check(base_rows); overlay_tree.check(overlay_rows); output_tree.check(output_tree.rows);
    for (Path* input : {&base, &repository, &overlay, &base_manifest, &overlay_manifest, &contract_file, &producer, &trace, &output_parent}) Check(*input);
    output.check(); duplicate.check();
    Json record;
    record.object = {
        {"base_manifest_sha256", Json(std::string(kBaseManifest))},
        {"base_root_identity", Json(Id(base.leaf().before.identity))},
        {"build_trace_sha256", Json(Narrow(args.at("--build-trace-sha256")))},
        {"effective_interface_map_sha256", Json(std::string(kMap))},
        {"effective_schema_sha256", Json(std::string(kSchema))},
        {"external_pin_digest", Json(Narrow(args.at("--external-pin-digest")))},
        {"final_file_count", Json(static_cast<uint64_t>(final_rows.size()))},
        {"final_manifest_sha256", Json(Hash(manifest))},
        {"final_total_bytes", Json(overlay_bytes + 24138847)},
        {"output_root_identity", Json(Id(output.before.identity))},
        {"overlay_contract_sha256", Json(Narrow(args.at("--contract-sha256")))},
        {"overlay_manifest_sha256", Json(Narrow(args.at("--overlay-sha256")))},
        {"platform_evidence_state", Json(std::string("explicitly-pinned-unverified-until-stage70"))},
        {"producer_file_sha256", Json(Narrow(args.at("--producer-sha256")))},
        {"producer_loaded_identity", Json(std::string("external-launcher-prerequisite-unverified-by-materializer"))},
        {"repository_root_identity", Json(Id(repository.leaf().before.identity))},
        {"run_nonce", Json(Narrow(args.at("--run-nonce")))},
        {"schema_id", Json(std::string("S0-RUNTIME-PRELOADER-V0.5-MATERIALIZATION-RESULT-1"))},
        {"terminal_state", Json(std::string("COMPLETE-RETAINED-HANDLES-PENDING-CLOSE"))}
    };
    Json measurements; measurements.kind = Json::Array;
    auto measure_row = [&](const std::string& name, const Node& node) {
        Json row; row.object = {{"path", Json(name)}, {"file_identity", Json(Id(node.before.identity))},
            {"security_descriptor_sha256", Json(node.before.security)}, {"effective_token_sha256", Json(node.before.token)}};
        measurements.array.push_back(std::move(row));
    };
    measure_row("output-root", output);
    measure_row("retained-output-duplicate", duplicate);
    size_t authority_index = 0;
    for (const Path* retained : {&base, &repository, &overlay, &base_manifest, &overlay_manifest, &contract_file, &producer, &trace, &output_parent}) {
        size_t ancestor_index = 0;
        for (const auto& node : retained->chain) {
            measure_row("authority-" + std::to_string(authority_index) + "-ancestor-" + std::to_string(ancestor_index), *node);
            ++ancestor_index;
        }
        ++authority_index;
    }
    for (const auto& item : output_tree.children) {
        Json row; row.object = {{"path", Json(item.first)}, {"file_identity", Json(Id(item.second->before.identity))},
            {"security_descriptor_sha256", Json(item.second->before.security)}, {"effective_token_sha256", Json(item.second->before.token)}};
        measurements.array.push_back(std::move(row));
    }
    record.object.emplace("pre_post_equal_measurements", std::move(measurements));
    std::string record_raw = Encode(record) + "\n";
    output_tree.bytes("evidence/materialization-record.json", record_raw);
    output_tree.bytes("evidence/materialization-record.json.sha256", Hash(record_raw) + "  materialization-record.json\n");
    std::string terminal_inventory;
    for (const auto& row : output_tree.rows) terminal_inventory += row.second.sha + "  " + row.first + "\n";
    output_tree.bytes("evidence/terminal-files.sha256", terminal_inventory);
    output_tree.bytes("evidence/terminal-files.sha256.sha256", Hash(terminal_inventory) + "  terminal-files.sha256\n");
    output_tree.check(output_tree.rows); base_tree.check(base_rows); overlay_tree.check(overlay_rows);
    for (Path* input : {&base, &repository, &overlay, &base_manifest, &overlay_manifest, &contract_file, &producer, &trace, &output_parent}) Check(*input);
    output.check(); duplicate.check();
    std::printf("S0_MATERIALIZATION_V05_COMPLETE %s %zu %llu\n", Hash(manifest).c_str(),
        final_rows.size(), static_cast<unsigned long long>(overlay_bytes + 24138847));
    return 0;
}
}
int wmain(int argc, wchar_t** argv) {
    try { return Run(argc, argv); }
    catch (const Failure& failure) {
        std::fprintf(stderr, "S0_MATERIALIZATION_V05_REJECT stage=%s code=%lu partial_output_non_authoritative_do_not_retry\n",
            failure.stage, failure.code); return 70;
    } catch (...) {
        std::fprintf(stderr, "S0_MATERIALIZATION_V05_REJECT stage=unclassified partial_output_non_authoritative_do_not_retry\n"); return 70;
    }
}
