#ifndef S0_RUNTIME_V0_5_H
#define S0_RUNTIME_V0_5_H

#if !defined(_WIN64)
#error "runtime/preloader v0.4 is defined only for the Windows x64 ABI"
#endif

#ifndef _WIN32_WINNT
#define _WIN32_WINNT 0x0A00
#endif
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <winternl.h>

#include <stdint.h>

/* Frozen public ABI constants from the authenticated v0.4 interface map. */
#define S0_HANDLE_COUNT 5u
#define S0_HANDLE_ARRAY_BYTES_X64 40u
#define S0_ATTRIBUTE_COUNT 1u
#define S0_CREATION_FLAGS ((DWORD)0x08080404u)
#define S0_HANDLE_LIST_ATTRIBUTE ((DWORD_PTR)0x00020002u)
#define S0_ROOT_ACCESS ((ACCESS_MASK)0x00100081u)
#define S0_ROOT_SHARE ((ULONG)0x00000001u)
#define S0_ROOT_DISPOSITION ((ULONG)0x00000002u)
#define S0_ROOT_OPTIONS ((ULONG)0x00200021u)
#define S0_ROOT_ATTRIBUTES ((ULONG)0x00000010u)
#define S0_OBJECT_ATTRIBUTES_FLAGS ((ULONG)0x00001040u)
#define S0_FILE_CREATED ((ULONG_PTR)0x0000000000000002ull)
#define S0_MAX_CONTROL_FRAME (64u * 1024u)
#define S0_MAX_ADMISSION_FRAME 8192u
#define S0_MAX_COMMIT_FRAME 64u
#define S0_MAX_RUNTIME_FILES 512u
#define S0_MAX_RUNTIME_BYTES (512ull * 1024ull * 1024ull)
#define S0_MAX_PATH_CHARS 32767u

#define S0_ADMISSION_SCHEMA "S0-PUBLIC-ASSEMBLY-RUNTIME-ADMISSION-FRAME-4"
#define S0_EVIDENCE_SCHEMA "S0-LAUNCH-HANDLE-SET-EVIDENCE-2"
#define S0_SUCCESS_POLICY "createprocess-success-bound-v0.4"
#define S0_PRELOADER_POLICY "authenticated-preloader-exact-handle-list-v0.4"
#define S0_KERNEL_POLICY "pinned-windows-handle-list-semantics-v0.4"
#define S0_GUARD_POLICY "known-five-handles-only-v0.4"

enum S0_HANDLE_POSITION {
    S0_ADMISSION_READ = 0,
    S0_COMMIT_REQUEST_WRITE = 1,
    S0_COMMIT_REPLY_READ = 2,
    S0_OUTPUT_ROOT = 3,
    S0_PRELOADER_PROCESS = 4
};

static const char* const S0_HANDLE_ROLE[S0_HANDLE_COUNT] = {
    "admission-read",
    "commit-request-write",
    "commit-reply-read",
    "output-root",
    "preloader-process"
};

static const char* const S0_HANDLE_KIND[S0_HANDLE_COUNT] = {
    "byte-stream-pipe-endpoint",
    "byte-stream-pipe-endpoint",
    "byte-stream-pipe-endpoint",
    "directory",
    "process"
};

static const char* const S0_HANDLE_ACCESS[S0_HANDLE_COUNT] = {
    "read-not-write-data",
    "write-not-read-data",
    "read-not-write-data",
    "file-list-directory-read-attributes-synchronize-only",
    "process-query-limited-information-synchronize-only"
};

typedef struct S0_FILE_IDENTITY {
    uint64_t volume_serial;
    uint8_t file_id[16];
} S0_FILE_IDENTITY;

typedef struct S0_SHA256 {
    uint8_t bytes[32];
} S0_SHA256;

typedef struct S0_NT_PROCESS_BASIC_INFORMATION {
    NTSTATUS ExitStatus;
    PPEB PebBaseAddress;
    ULONG_PTR AffinityMask;
    LONG BasePriority;
    ULONG_PTR UniqueProcessId;
    ULONG_PTR InheritedFromUniqueProcessId;
} S0_NT_PROCESS_BASIC_INFORMATION;

typedef NTSTATUS (NTAPI *S0_NT_CREATE_FILE)(
    PHANDLE,
    ACCESS_MASK,
    POBJECT_ATTRIBUTES,
    PIO_STATUS_BLOCK,
    PLARGE_INTEGER,
    ULONG,
    ULONG,
    ULONG,
    ULONG,
    PVOID,
    ULONG
);

typedef NTSTATUS (NTAPI *S0_NT_QUERY_OBJECT)(
    HANDLE,
    OBJECT_INFORMATION_CLASS,
    PVOID,
    ULONG,
    PULONG
);

typedef NTSTATUS (NTAPI *S0_NT_QUERY_INFORMATION_PROCESS)(
    HANDLE,
    PROCESSINFOCLASS,
    PVOID,
    ULONG,
    PULONG
);


/* Pure byte grammar shared by the producer and consumer. No OS calls. */
#include <array>
#include <map>
#include <set>
#include <stdexcept>
#include <string>

inline bool S0LowerHex(const std::string& text, size_t width) {
    if (text.size() != width) return false;
    for (char c : text)
        if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f'))) return false;
    return true;
}

inline void S0CanonicalWorkspace(const std::string& value) {
    if (value.size() < 3 || value.size() > 32766 ||
        value[0] < 'A' || value[0] > 'Z' || value[1] != ':' || value[2] != '\\' ||
        (value.size() > 3 && value.back() == '\\')) throw std::runtime_error("workspace grammar");
    for (unsigned char c : value)
        if (c < 32 || c > 126 || c == '/' || c == '=' || c == '"' || c == '<' ||
            c == '>' || c == '|' || c == '?' || c == '*') throw std::runtime_error("workspace character");
    size_t start = 3;
    while (start < value.size()) {
        size_t end = value.find('\\', start);
        if (end == std::string::npos) end = value.size();
        std::string part = value.substr(start, end - start);
        if (part.empty() || part == "." || part == ".." || part.size() > 255 ||
            part.back() == '.' || part.back() == ' ' || part.find(':') != std::string::npos)
            throw std::runtime_error("workspace component");
        start = end + 1;
    }
}

inline void S0CanonicalVirtual(const std::string& value) {
    if (value.empty() || value.size() > 1024 || value.front() == '/' || value.back() == '/')
        throw std::runtime_error("virtual path size");
    size_t start = 0;
    while (start < value.size()) {
        size_t end = value.find('/', start);
        if (end == std::string::npos) end = value.size();
        std::string part = value.substr(start, end - start);
        if (part.empty() || part == "." || part == ".." || part.size() > 255 || part.back() == '.')
            throw std::runtime_error("virtual path component");
        for (char c : part)
            if (!((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') ||
                  (c >= '0' && c <= '9') || c == '.' || c == '_' || c == '-'))
                throw std::runtime_error("virtual path character");
        start = end + 1;
    }
}

inline std::string S0EvidenceV2(
    const std::map<std::string, std::string>& fields,
    const std::array<std::string, S0_HANDLE_COUNT>& locators) {
    std::string raw;
    auto emit = [&](const std::string& name, const std::string& value) {
        if (value.empty()) throw std::runtime_error("empty evidence value");
        for (unsigned char c : value)
            if (c < 32 || c > 126 || c == '=') throw std::runtime_error("evidence encoding");
        raw += name + "=" + value + "\n";
        if (raw.size() > 65536) throw std::runtime_error("evidence bound");
    };
    auto field = [&](const char* key) -> const std::string& {
        auto found = fields.find(key);
        if (found == fields.end()) throw std::runtime_error("missing evidence field");
        return found->second;
    };
    auto hash = [&](const char* key) {
        const std::string& value = field(key);
        if (!S0LowerHex(value, 64)) throw std::runtime_error("evidence hash");
        emit(key, value);
    };
    emit("schema_id", S0_EVIDENCE_SCHEMA);
    hash("run_nonce");
    hash("external_pin_digest");
    S0CanonicalWorkspace(field("workspace_root"));
    emit("workspace_root", field("workspace_root"));
    for (const char* key : {"preloader_image_sha256", "runtime_package_sha256", "launch_control_sha256",
        "runtime_profile_v0_1_sha256", "runtime_profile_v0_2_sha256",
        "runtime_profile_v0_3_sha256", "runtime_profile_v0_4_sha256"}) hash(key);
    for (const char* role : {"application", "bootstrap", "verifier"}) {
        std::string path_key = std::string(role) + "_virtual_path";
        const std::string& path = field(path_key.c_str());
        S0CanonicalVirtual(path);
        emit(path_key, path);
        hash((std::string(role) + "_sha256").c_str());
    }
    emit("creation_flags_numeric", "0x08080404");
    emit("startupinfoex_dwflags", "0");
    emit("b_inherit_handles", "true");
    emit("attribute_count", "1");
    emit("attribute_id_numeric", "0x00020002");
    emit("handle_array_bytes_x64", "40");
    emit("handle_count", "5");
    std::set<std::string> unique;
    for (size_t i = 0; i < S0_HANDLE_COUNT; ++i) {
        const std::string& locator = locators[i];
        if (locator.size() != 18 || locator.substr(0, 2) != "0x" ||
            !S0LowerHex(locator.substr(2), 16) || locator == "0x0000000000000000" ||
            locator >= "0xfffffffffffffffa" || !unique.insert(locator).second)
            throw std::runtime_error("evidence locator");
        std::string prefix = "handle_" + std::to_string(i) + "_";
        emit(prefix + "role", S0_HANDLE_ROLE[i]);
        emit(prefix + "kind", S0_HANDLE_KIND[i]);
        emit(prefix + "access", S0_HANDLE_ACCESS[i]);
        emit(prefix + "locator", locator);
    }
    emit("precreation_verifier_pid", "0");
    return raw;
}

#endif
