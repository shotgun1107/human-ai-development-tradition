#define PY_SSIZE_T_CLEAN
#ifndef _WIN32_WINNT
#define _WIN32_WINNT 0x0A00
#endif
#include <Python.h>

#include "s0_runtime_v0_5.h"

#include <algorithm>
#include <array>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <map>
#include <string>
#include <vector>

#pragma comment(lib, "ntdll.lib")

extern "C" NTSYSAPI NTSTATUS NTAPI NtQueryObject(
    HANDLE,
    OBJECT_INFORMATION_CLASS,
    PVOID,
    ULONG,
    PULONG
);
namespace {

volatile LONG g_bind_latch = 0;

constexpr std::array<const char*, 28> kAdmissionKeys = {
    "actual_verifier_pid",
    "application_path",
    "application_sha256",
    "application_virtual_path",
    "bootstrap_sha256",
    "bootstrap_virtual_path",
    "effective_runtime_package_sha256",
    "external_pin_digest",
    "guard_observation_policy_id",
    "kernel_semantics_policy_id",
    "launch_control_sha256",
    "launch_handle_set_evidence_sha256",
    "preloader_image_path",
    "preloader_image_sha256",
    "preloader_pid",
    "preloader_responsibility_id",
    "root_file_id",
    "root_volume_serial",
    "run_nonce",
    "runtime_profile_v0_1_sha256",
    "runtime_profile_v0_2_sha256",
    "runtime_profile_v0_3_sha256",
    "runtime_profile_v0_4_sha256",
    "schema_id",
    "success_policy_id",
    "verifier_sha256",
    "verifier_virtual_path",
    "workspace_root"
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

struct Sha256 {
    uint32_t state[8];
    uint64_t bit_count;
    uint8_t block[64];
    size_t used;
};

constexpr uint32_t kSha256[64] = {
    0x428a2f98u,0x71374491u,0xb5c0fbcfu,0xe9b5dba5u,0x3956c25bu,0x59f111f1u,0x923f82a4u,0xab1c5ed5u,
    0xd807aa98u,0x12835b01u,0x243185beu,0x550c7dc3u,0x72be5d74u,0x80deb1feu,0x9bdc06a7u,0xc19bf174u,
    0xe49b69c1u,0xefbe4786u,0x0fc19dc6u,0x240ca1ccu,0x2de92c6fu,0x4a7484aau,0x5cb0a9dcu,0x76f988dau,
    0x983e5152u,0xa831c66du,0xb00327c8u,0xbf597fc7u,0xc6e00bf3u,0xd5a79147u,0x06ca6351u,0x14292967u,
    0x27b70a85u,0x2e1b2138u,0x4d2c6dfcu,0x53380d13u,0x650a7354u,0x766a0abbu,0x81c2c92eu,0x92722c85u,
    0xa2bfe8a1u,0xa81a664bu,0xc24b8b70u,0xc76c51a3u,0xd192e819u,0xd6990624u,0xf40e3585u,0x106aa070u,
    0x19a4c116u,0x1e376c08u,0x2748774cu,0x34b0bcb5u,0x391c0cb3u,0x4ed8aa4au,0x5b9cca4fu,0x682e6ff3u,
    0x748f82eeu,0x78a5636fu,0x84c87814u,0x8cc70208u,0x90befffau,0xa4506cebu,0xbef9a3f7u,0xc67178f2u
};

uint32_t Rotate(uint32_t value, unsigned bits) {
    return (value >> bits) | (value << (32u - bits));
}

void ShaTransform(Sha256& hash, const uint8_t* block) {
    uint32_t w[64]{};
    for (size_t i = 0; i < 16; ++i) {
        w[i] = (static_cast<uint32_t>(block[i * 4]) << 24) |
               (static_cast<uint32_t>(block[i * 4 + 1]) << 16) |
               (static_cast<uint32_t>(block[i * 4 + 2]) << 8) |
               static_cast<uint32_t>(block[i * 4 + 3]);
    }
    for (size_t i = 16; i < 64; ++i) {
        uint32_t s0 = Rotate(w[i - 15], 7) ^ Rotate(w[i - 15], 18) ^ (w[i - 15] >> 3);
        uint32_t s1 = Rotate(w[i - 2], 17) ^ Rotate(w[i - 2], 19) ^ (w[i - 2] >> 10);
        w[i] = w[i - 16] + s0 + w[i - 7] + s1;
    }
    uint32_t a=hash.state[0], b=hash.state[1], c=hash.state[2], d=hash.state[3];
    uint32_t e=hash.state[4], f=hash.state[5], g=hash.state[6], h=hash.state[7];
    for (size_t i = 0; i < 64; ++i) {
        uint32_t s1 = Rotate(e, 6) ^ Rotate(e, 11) ^ Rotate(e, 25);
        uint32_t choice = (e & f) ^ (~e & g);
        uint32_t t1 = h + s1 + choice + kSha256[i] + w[i];
        uint32_t s0 = Rotate(a, 2) ^ Rotate(a, 13) ^ Rotate(a, 22);
        uint32_t majority = (a & b) ^ (a & c) ^ (b & c);
        uint32_t t2 = s0 + majority;
        h=g; g=f; f=e; e=d+t1; d=c; c=b; b=a; a=t1+t2;
    }
    hash.state[0]+=a; hash.state[1]+=b; hash.state[2]+=c; hash.state[3]+=d;
    hash.state[4]+=e; hash.state[5]+=f; hash.state[6]+=g; hash.state[7]+=h;
}

void ShaInit(Sha256& hash) {
    const uint32_t initial[8] = {0x6a09e667u,0xbb67ae85u,0x3c6ef372u,0xa54ff53au,
                                 0x510e527fu,0x9b05688cu,0x1f83d9abu,0x5be0cd19u};
    memcpy(hash.state, initial, sizeof(initial));
    hash.bit_count = 0;
    hash.used = 0;
}

void ShaUpdate(Sha256& hash, const uint8_t* data, size_t count) {
    hash.bit_count += static_cast<uint64_t>(count) * 8u;
    while (count) {
        size_t take = (std::min)(count, sizeof(hash.block) - hash.used);
        memcpy(hash.block + hash.used, data, take);
        hash.used += take;
        data += take;
        count -= take;
        if (hash.used == sizeof(hash.block)) {
            ShaTransform(hash, hash.block);
            hash.used = 0;
        }
    }
}

std::array<uint8_t, 32> ShaFinish(Sha256& hash) {
    uint64_t bits = hash.bit_count;
    uint8_t one = 0x80;
    ShaUpdate(hash, &one, 1);
    uint8_t zero = 0;
    while (hash.used != 56) ShaUpdate(hash, &zero, 1);
    uint8_t length[8]{};
    for (size_t i = 0; i < 8; ++i) length[7 - i] = static_cast<uint8_t>(bits >> (i * 8));
    ShaUpdate(hash, length, sizeof(length));
    std::array<uint8_t, 32> output{};
    for (size_t i = 0; i < 8; ++i) {
        output[i * 4] = static_cast<uint8_t>(hash.state[i] >> 24);
        output[i * 4 + 1] = static_cast<uint8_t>(hash.state[i] >> 16);
        output[i * 4 + 2] = static_cast<uint8_t>(hash.state[i] >> 8);
        output[i * 4 + 3] = static_cast<uint8_t>(hash.state[i]);
    }
    SecureZeroMemory(&hash, sizeof(hash));
    return output;
}

std::string Hash(const std::string& raw) {
    Sha256 state{};
    ShaInit(state);
    ShaUpdate(state, reinterpret_cast<const uint8_t*>(raw.data()), raw.size());
    auto digest = ShaFinish(state);
    static constexpr char digits[] = "0123456789abcdef";
    std::string result(64, '0');
    for (size_t i = 0; i < digest.size(); ++i) {
        result[i * 2] = digits[digest[i] >> 4];
        result[i * 2 + 1] = digits[digest[i] & 15];
    }
    return result;
}

bool LowerSha(const std::string& value) {
    if (value.size() != 64) return false;
    for (char ch : value) if (!((ch >= '0' && ch <= '9') || (ch >= 'a' && ch <= 'f'))) return false;
    return true;
}

void SetFailure(const char* message) {
    PyErr_SetString(PyExc_RuntimeError, message);
}

std::string ParseJsonString(const std::string& raw, size_t& cursor) {
    if (cursor >= raw.size() || raw[cursor++] != '"') throw 1;
    std::string value;
    while (cursor < raw.size()) {
        unsigned char ch = static_cast<unsigned char>(raw[cursor++]);
        if (ch == '"') return value;
        if (ch < 0x20 || ch > 0x7e) throw 1;
        if (ch == '\\') {
            if (cursor >= raw.size()) throw 1;
            char escaped = raw[cursor++];
            if (escaped != '\\' && escaped != '"') throw 1;
            value.push_back(escaped);
        } else value.push_back(static_cast<char>(ch));
    }
    throw 1;
}

std::string EncodeJsonString(const std::string& value) {
    std::string result = "\"";
    for (unsigned char ch : value) {
        if (ch < 0x20 || ch > 0x7e) throw 1;
        if (ch == '\\' || ch == '"') result.push_back('\\');
        result.push_back(static_cast<char>(ch));
    }
    result.push_back('"');
    return result;
}

std::map<std::string, std::string> ParseCanonicalJson(const std::string& raw) {
    if (raw.size() < 3 || raw.back() != '\n') throw 1;
    size_t cursor = 0;
    if (raw[cursor++] != '{') throw 1;
    std::map<std::string, std::string> result;
    std::string previous;
    bool first = true;
    while (cursor < raw.size() && raw[cursor] != '}') {
        if (!first && raw[cursor++] != ',') throw 1;
        std::string key = ParseJsonString(raw, cursor);
        if ((!previous.empty() && key <= previous) || cursor >= raw.size() || raw[cursor++] != ':') throw 1;
        std::string value = ParseJsonString(raw, cursor);
        result.emplace(key, value);
        previous = key;
        first = false;
    }
    if (cursor + 2 != raw.size() || raw[cursor] != '}' || raw[cursor + 1] != '\n') throw 1;
    std::string rebuilt = "{";
    first = true;
    for (const auto& field : result) {
        if (!first) rebuilt.push_back(',');
        rebuilt += EncodeJsonString(field.first) + ":" + EncodeJsonString(field.second);
        first = false;
    }
    rebuilt += "}\n";
    if (rebuilt != raw) throw 1;
    return result;
}

const std::string& Field(const std::map<std::string, std::string>& value, const char* name) {
    auto it = value.find(name);
    if (it == value.end() || it->second.empty()) throw 1;
    return it->second;
}

void RequireExactAdmissionKeys(const std::map<std::string, std::string>& admission) {
    if (admission.size() != kAdmissionKeys.size()) throw 1;
    size_t index = 0;
    for (const auto& field : admission) {
        if (field.first != kAdmissionKeys[index]) throw 1;
        ++index;
    }
}

void RequireWorkspaceRoot(const std::string& value) {
    S0CanonicalWorkspace(value);
}

uint64_t Decimal(const std::string& value) {
    if (value.empty() || (value.size() > 1 && value[0] == '0')) throw 1;
    uint64_t result = 0;
    for (char ch : value) {
        if (ch < '0' || ch > '9' || result > (UINT64_MAX - static_cast<uint64_t>(ch - '0')) / 10) throw 1;
        result = result * 10 + static_cast<uint64_t>(ch - '0');
    }
    return result;
}

std::string ReadAdmission(HANDLE handle) {
    std::string raw;
    std::array<char, 1024> buffer{};
    for (;;) {
        DWORD got = 0;
        if (!ReadFile(handle, buffer.data(), static_cast<DWORD>(buffer.size()), &got, nullptr)) {
            if (GetLastError() == ERROR_BROKEN_PIPE) break;
            throw 1;
        }
        if (!got) break;
        if (raw.size() + got > S0_MAX_ADMISSION_FRAME) throw 1;
        raw.append(buffer.data(), got);
    }
    if (raw.empty() || raw.back() != '\n' || raw.find('\r') != std::string::npos || raw.find('\0') != std::string::npos) throw 1;
    return raw;
}

ACCESS_MASK GrantedAccess(HANDLE handle) {
    S0ObjectBasicInformation info{};
    ULONG returned = 0;
    NTSTATUS status = NtQueryObject(handle, ObjectBasicInformation,
                                    &info, sizeof(info), &returned);
    if (status < 0 || returned < offsetof(S0ObjectBasicInformation, creation_time)) throw 1;
    return info.granted_access;
}

void RequireHandleBase(HANDLE handle) {
    DWORD flags = 0;
    if (!handle || handle == INVALID_HANDLE_VALUE ||
        !GetHandleInformation(handle, &flags) || !(flags & HANDLE_FLAG_INHERIT)) throw 1;
}

void RequirePipe(HANDLE handle, bool read_end) {
    if (GetFileType(handle) != FILE_TYPE_PIPE) throw 1;
    DWORD flags = 0, output_size = 0, input_size = 0, maximum = 0;
    if (!GetNamedPipeInfo(handle, &flags, &output_size, &input_size, &maximum) ||
        (flags & PIPE_TYPE_MESSAGE)) throw 1;
    ACCESS_MASK access = GrantedAccess(handle);
    bool can_read = (access & FILE_READ_DATA) != 0;
    bool can_write = (access & FILE_WRITE_DATA) != 0;
    if (can_read != read_end || can_write == read_end) throw 1;
}

std::string HexBytes(const uint8_t* bytes, size_t count) {
    static constexpr char digits[] = "0123456789abcdef";
    std::string result(count * 2, '0');
    for (size_t i = 0; i < count; ++i) {
        result[i * 2] = digits[bytes[i] >> 4];
        result[i * 2 + 1] = digits[bytes[i] & 15];
    }
    return result;
}

std::wstring Utf8ToWide(const std::string& value) {
    int count = MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, value.data(),
                                    static_cast<int>(value.size()), nullptr, 0);
    if (count <= 0) throw 1;
    std::wstring result(static_cast<size_t>(count), L'\0');
    if (MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, value.data(),
                            static_cast<int>(value.size()), result.data(), count) != count) throw 1;
    return result;
}

std::wstring ProcessImage(HANDLE process) {
    std::wstring path(S0_MAX_PATH_CHARS, L'\0');
    DWORD count = static_cast<DWORD>(path.size());
    if (!QueryFullProcessImageNameW(process, 0, path.data(), &count) || !count) throw 1;
    path.resize(count);
    return path;
}

bool EqualPath(const std::wstring& left, const std::wstring& right) {
    return left.size() == right.size() && CompareStringOrdinal(left.c_str(), static_cast<int>(left.size()),
        right.c_str(), static_cast<int>(right.size()), FALSE) == CSTR_EQUAL;
}

std::string HandleLocator(HANDLE handle) {
    char text[19]{};
    if (sprintf_s(text, "0x%016llx",
                  static_cast<unsigned long long>(reinterpret_cast<uintptr_t>(handle))) != 18) throw 1;
    return text;
}

std::string RebuildEvidence(const std::map<std::string, std::string>& admission,
                            const std::array<HANDLE, S0_HANDLE_COUNT>& handles) {
    auto fields = admission;
    fields["runtime_package_sha256"] = Field(admission, "effective_runtime_package_sha256");
    std::array<std::string, S0_HANDLE_COUNT> locators{};
    for (size_t i = 0; i < S0_HANDLE_COUNT; ++i) locators[i] = HandleLocator(handles[i]);
    return S0EvidenceV2(fields, locators);

}

struct HandleBindingsV4 {
    PyObject_HEAD
    HANDLE commit_request_write;
    HANDLE commit_reply_read;
    HANDLE output_root;
    HANDLE preloader_process;
    volatile LONG state;
};

void CloseOwned(HandleBindingsV4* self) {
    HANDLE* handles[] = {&self->commit_request_write, &self->commit_reply_read,
                         &self->output_root, &self->preloader_process};
    for (HANDLE* item : handles) {
        if (*item && *item != INVALID_HANDLE_VALUE) CloseHandle(*item);
        *item = nullptr;
    }
}

void BindingsDealloc(PyObject* object) {
    auto* self = reinterpret_cast<HandleBindingsV4*>(object);
    CloseOwned(self);
    Py_TYPE(object)->tp_free(object);
}

PyObject* CommitOnce(PyObject* object, PyObject* arguments) {
    auto* self = reinterpret_cast<HandleBindingsV4*>(object);
    if (!PyArg_ParseTuple(arguments, ":commit_once")) return nullptr;
    if (InterlockedCompareExchange(&self->state, 1, 0) != 0) {
        SetFailure("runtime admission is terminal or already committing");
        return nullptr;
    }
    const char request[] = "RUNTIME_ADMISSION_COMMIT\n";
    DWORD wrote = 0;
    if (!WriteFile(self->commit_request_write, request, sizeof(request) - 1, &wrote, nullptr) ||
        wrote != sizeof(request) - 1) {
        InterlockedExchange(&self->state, -1);
        CloseOwned(self);
        SetFailure("runtime commit request failed");
        return nullptr;
    }
    CloseHandle(self->commit_request_write);
    self->commit_request_write = nullptr;
    char reply[4]{};
    DWORD got = 0;
    if (!ReadFile(self->commit_reply_read, reply, 3, &got, nullptr) || got != 3 ||
        memcmp(reply, "OK\n", 3) != 0) {
        InterlockedExchange(&self->state, -1);
        CloseOwned(self);
        SetFailure("runtime commit reply failed");
        return nullptr;
    }
    char extra = 0;
    DWORD extra_count = 0;
    BOOL extra_result = ReadFile(self->commit_reply_read, &extra, 1, &extra_count, nullptr);
    DWORD extra_error = GetLastError();
    if ((extra_result && extra_count != 0) || (!extra_result && extra_error != ERROR_BROKEN_PIPE)) {
        InterlockedExchange(&self->state, -1);
        CloseOwned(self);
        SetFailure("runtime commit reply EOF differs");
        return nullptr;
    }
    CloseHandle(self->commit_reply_read);
    self->commit_reply_read = nullptr;
    InterlockedExchange(&self->state, 2);
    Py_RETURN_NONE;
}

PyObject* BindingsRepr(PyObject*) {
    return PyUnicode_FromString("<HandleBindingsV4 private-process-local>");
}

PyMethodDef binding_methods[] = {
    {"commit_once", CommitOnce, METH_VARARGS, nullptr},
    {nullptr, nullptr, 0, nullptr}
};

PyTypeObject binding_type = {PyVarObject_HEAD_INIT(nullptr, 0)};

void CloseFive(std::array<HANDLE, S0_HANDLE_COUNT>& handles) {
    std::set<HANDLE> closed;
    for (HANDLE& handle : handles) {
        if (handle && handle != INVALID_HANDLE_VALUE && closed.insert(handle).second) CloseHandle(handle);
        handle = nullptr;
    }
}

PyObject* BindOnce(PyObject*, PyObject* args) {
    if (InterlockedCompareExchange(&g_bind_latch, 1, 0) != 0) {
        SetFailure("native runtime handle bind latch is already consumed");
        return nullptr;
    }
    PyObject* tuple = nullptr;
    if (!PyArg_ParseTuple(args, "O:bind_once_v4", &tuple) || !PyTuple_CheckExact(tuple) ||
        PyTuple_GET_SIZE(tuple) != S0_HANDLE_COUNT) {
        SetFailure("native runtime handle tuple differs");
        return nullptr;
    }
    std::array<HANDLE, S0_HANDLE_COUNT> handles{};
    try {
        for (Py_ssize_t index = 0; index < static_cast<Py_ssize_t>(S0_HANDLE_COUNT); ++index) {
            PyObject* item = PyTuple_GET_ITEM(tuple, index);
            if (!PyLong_CheckExact(item)) throw 1;
            unsigned long long value = PyLong_AsUnsignedLongLong(item);
            if (PyErr_Occurred() || !value || value == UINT64_MAX || value > UINTPTR_MAX) throw 1;
            handles[static_cast<size_t>(index)] = reinterpret_cast<HANDLE>(static_cast<uintptr_t>(value));
            RequireHandleBase(handles[static_cast<size_t>(index)]);
        }
        for (size_t left = 0; left < handles.size(); ++left)
            for (size_t right = left + 1; right < handles.size(); ++right)
                if (handles[left] == handles[right]) throw 1;

        RequirePipe(handles[S0_ADMISSION_READ], true);
        RequirePipe(handles[S0_COMMIT_REQUEST_WRITE], false);
        RequirePipe(handles[S0_COMMIT_REPLY_READ], true);
        DWORD reply_available = 0;
        if (!PeekNamedPipe(handles[S0_COMMIT_REPLY_READ], nullptr, 0, nullptr,
                           &reply_available, nullptr) || reply_available != 0) throw 1;

        if (GetFileType(handles[S0_OUTPUT_ROOT]) != FILE_TYPE_DISK ||
            GrantedAccess(handles[S0_OUTPUT_ROOT]) != S0_ROOT_ACCESS) throw 1;
        FILE_ATTRIBUTE_TAG_INFO root_tag{};
        FILE_STANDARD_INFO root_standard{};
        FILE_ID_INFO root_id{};
        FILE_ID_INFO root_id_second{};
        if (!GetFileInformationByHandleEx(handles[S0_OUTPUT_ROOT], FileAttributeTagInfo,
                                          &root_tag, sizeof(root_tag)) ||
            !GetFileInformationByHandleEx(handles[S0_OUTPUT_ROOT], FileStandardInfo,
                                          &root_standard, sizeof(root_standard)) ||
            !GetFileInformationByHandleEx(handles[S0_OUTPUT_ROOT], FileIdInfo,
                                          &root_id, sizeof(root_id)) ||
            !GetFileInformationByHandleEx(handles[S0_OUTPUT_ROOT], FileIdInfo,
                                          &root_id_second, sizeof(root_id_second)) ||
            !(root_tag.FileAttributes & FILE_ATTRIBUTE_DIRECTORY) ||
            (root_tag.FileAttributes & FILE_ATTRIBUTE_REPARSE_POINT) ||
            root_standard.NumberOfLinks != 1 || root_standard.DeletePending ||
            memcmp(&root_id, &root_id_second, sizeof(root_id)) != 0) throw 1;

        if (GrantedAccess(handles[S0_PRELOADER_PROCESS]) !=
                (PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE)) throw 1;
        DWORD preloader_pid = GetProcessId(handles[S0_PRELOADER_PROCESS]);
        if (!preloader_pid) throw 1;

        std::string raw = ReadAdmission(handles[S0_ADMISSION_READ]);
        auto admission = ParseCanonicalJson(raw);
        RequireExactAdmissionKeys(admission);
        RequireWorkspaceRoot(Field(admission, "workspace_root"));
        if (Field(admission, "schema_id") != S0_ADMISSION_SCHEMA ||
            Field(admission, "success_policy_id") != S0_SUCCESS_POLICY ||
            Field(admission, "preloader_responsibility_id") != S0_PRELOADER_POLICY ||
            Field(admission, "kernel_semantics_policy_id") != S0_KERNEL_POLICY ||
            Field(admission, "guard_observation_policy_id") != S0_GUARD_POLICY ||
            Decimal(Field(admission, "actual_verifier_pid")) != GetCurrentProcessId() ||
            Decimal(Field(admission, "preloader_pid")) != preloader_pid) throw 1;
        for (const char* name : {"application_sha256", "bootstrap_sha256",
                                 "effective_runtime_package_sha256", "external_pin_digest",
                                 "launch_control_sha256", "launch_handle_set_evidence_sha256",
                                 "preloader_image_sha256", "run_nonce",
                                 "runtime_profile_v0_1_sha256", "runtime_profile_v0_2_sha256",
                                 "runtime_profile_v0_3_sha256", "runtime_profile_v0_4_sha256",
                                 "verifier_sha256"}) {
            if (!LowerSha(Field(admission, name))) throw 1;
        }
        for (const auto& field : admission) {
            if (field.first.find("locator") != std::string::npos ||
                field.first.find("handle_value") != std::string::npos) throw 1;
        }
        if (Field(admission, "root_file_id") != HexBytes(root_id.FileId.Identifier, 16) ||
            Field(admission, "root_volume_serial") !=
                HexBytes(reinterpret_cast<const uint8_t*>(&root_id.VolumeSerialNumber), 8)) throw 1;

        S0_NT_PROCESS_BASIC_INFORMATION basic{};
        ULONG returned = 0;
        if (NtQueryInformationProcess(GetCurrentProcess(), ProcessBasicInformation,
                                      &basic, sizeof(basic), &returned) < 0 ||
            returned < sizeof(basic) || basic.InheritedFromUniqueProcessId != preloader_pid) throw 1;
        BOOL current_in_job = FALSE, preloader_in_job = FALSE;
        if (!IsProcessInJob(GetCurrentProcess(), nullptr, &current_in_job) || !current_in_job ||
            !IsProcessInJob(handles[S0_PRELOADER_PROCESS], nullptr, &preloader_in_job) ||
            preloader_in_job) throw 1;
        if (!EqualPath(ProcessImage(handles[S0_PRELOADER_PROCESS]),
                       Utf8ToWide(Field(admission, "preloader_image_path")))) throw 1;
        if (!EqualPath(ProcessImage(GetCurrentProcess()),
                       Utf8ToWide(Field(admission, "application_path")))) throw 1;
        std::string evidence = RebuildEvidence(admission, handles);
        if (Hash(evidence) != Field(admission, "launch_handle_set_evidence_sha256")) throw 1;
        if (WaitForSingleObject(handles[S0_PRELOADER_PROCESS], 0) != WAIT_TIMEOUT) throw 1;
        CloseHandle(handles[S0_ADMISSION_READ]);
        handles[S0_ADMISSION_READ] = nullptr;

        auto* binding = reinterpret_cast<HandleBindingsV4*>(binding_type.tp_alloc(&binding_type, 0));
        if (!binding) throw 1;
        binding->commit_request_write = handles[S0_COMMIT_REQUEST_WRITE];
        binding->commit_reply_read = handles[S0_COMMIT_REPLY_READ];
        binding->output_root = handles[S0_OUTPUT_ROOT];
        binding->preloader_process = handles[S0_PRELOADER_PROCESS];
        binding->state = 0;
        handles[S0_COMMIT_REQUEST_WRITE] = nullptr;
        handles[S0_COMMIT_REPLY_READ] = nullptr;
        handles[S0_OUTPUT_ROOT] = nullptr;
        handles[S0_PRELOADER_PROCESS] = nullptr;
        return reinterpret_cast<PyObject*>(binding);
    } catch (...) {
        PyErr_Clear();
        CloseFive(handles);
        SetFailure("native runtime handle admission rejected");
        return nullptr;
    }
}

PyMethodDef module_methods[] = {
    {"bind_once_v4", BindOnce, METH_VARARGS, nullptr},
    {nullptr, nullptr, 0, nullptr}
};

PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "s0_runtime_handle_guard_v0_4",
    nullptr,
    -1,
    module_methods,
    nullptr,
    nullptr,
    nullptr,
    nullptr
};

}  // namespace

PyMODINIT_FUNC PyInit_s0_runtime_handle_guard_v0_4(void) {
    binding_type.tp_name = "s0_runtime_handle_guard_v0_4.HandleBindingsV4";
    binding_type.tp_basicsize = sizeof(HandleBindingsV4);
    binding_type.tp_dealloc = BindingsDealloc;
    binding_type.tp_repr = BindingsRepr;
    binding_type.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_DISALLOW_INSTANTIATION;
    binding_type.tp_methods = binding_methods;
    binding_type.tp_new = nullptr;
    if (PyType_Ready(&binding_type) < 0) return nullptr;
    return PyModule_Create(&module);
}
