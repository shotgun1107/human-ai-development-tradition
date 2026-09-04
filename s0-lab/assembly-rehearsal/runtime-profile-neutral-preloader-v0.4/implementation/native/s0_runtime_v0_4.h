#ifndef S0_RUNTIME_V0_4_H
#define S0_RUNTIME_V0_4_H

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
#define S0_EVIDENCE_SCHEMA "S0-LAUNCH-HANDLE-SET-EVIDENCE-1"
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

#endif
