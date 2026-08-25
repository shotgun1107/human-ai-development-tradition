"""Windows ctypes collector for one pinned acquisition and private read lease.

Importing this module calls no native API. ``collect_observation`` is the only
live entry and is intentionally not exercised by the PUBLIC synthetic suite.
"""

from __future__ import annotations

import ctypes
from ctypes import wintypes
import hashlib
import os
import uuid
from pathlib import Path

from .acquisition import AcquisitionEvidence
from .canonical import VerificationError, canonical_json_lf, sha256_hex
from .contract import (
    CHAIN_ENGINE,
    CHAIN_FLAGS,
    CODE_SIGNING_EKU,
    EVENT_SEQUENCE,
    FILETIME_TICKS_PER_SECOND,
    IMMUTABLE_LEASE_CONTRACT,
    MAX_CANDIDATE_BYTES,
    MAX_CERTIFICATE_BYTES,
    MAX_CHAIN_CALL_DURATION_SECONDS,
    MAX_CTL_BYTES,
    MAX_OBSERVATION_BYTES,
    MAX_PROVIDER_CHAIN_CERTIFICATES,
    MAX_REBUILT_CHAIN_CERTIFICATES,
    MAX_REVOCATION_FRESHNESS_SECONDS,
    MAX_STORE_ENTRIES,
    OBSERVATION_SCHEMA_ID,
    RUNTIME_AUTHORITY_SCOPE,
    SUPPLIER_CRITERION_COMPONENTS,
    SUPPLIER_CRITERION_ID,
    TIME_STAMPING_EKU,
    TRUST_SNAPSHOT_SCOPE,
    URL_RETRIEVAL_TIMEOUT_MS,
    WINTRUST_ACTION_GUID,
    WINTRUST_PROV_FLAGS,
)
from .model import VerificationAuthority
from .semantic import chain_call_input_sha256, policy_input_sha256


class NativeVerificationError(VerificationError):
    """A native observation could not be completed without ambiguity."""


DWORD = wintypes.DWORD
BOOL = wintypes.BOOL
HANDLE = wintypes.HANDLE
LPVOID = wintypes.LPVOID


class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", ctypes.c_ubyte * 8),
    ]


class FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", DWORD), ("dwHighDateTime", DWORD)]


class CERT_TRUST_STATUS(ctypes.Structure):
    _fields_ = [("dwErrorStatus", DWORD), ("dwInfoStatus", DWORD)]


class CERT_CONTEXT(ctypes.Structure):
    _fields_ = [
        ("dwCertEncodingType", DWORD),
        ("pbCertEncoded", ctypes.POINTER(ctypes.c_ubyte)),
        ("cbCertEncoded", DWORD),
        ("pCertInfo", LPVOID),
        ("hCertStore", HANDLE),
    ]


PCERT_CONTEXT = ctypes.POINTER(CERT_CONTEXT)


class CERT_REVOCATION_INFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("dwRevocationResult", DWORD),
        ("pszRevocationOid", ctypes.c_char_p),
        ("pvOidSpecificInfo", LPVOID),
        ("fHasFreshnessTime", BOOL),
        ("dwFreshnessTime", DWORD),
        ("pCrlInfo", LPVOID),
    ]


class CERT_CHAIN_ELEMENT(ctypes.Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("pCertContext", PCERT_CONTEXT),
        ("TrustStatus", CERT_TRUST_STATUS),
        ("pRevocationInfo", ctypes.POINTER(CERT_REVOCATION_INFO)),
        ("pIssuanceUsage", LPVOID),
        ("pApplicationUsage", LPVOID),
        ("pwszExtendedErrorInfo", wintypes.LPWSTR),
    ]


PCERT_CHAIN_ELEMENT = ctypes.POINTER(CERT_CHAIN_ELEMENT)


class CERT_SIMPLE_CHAIN(ctypes.Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("TrustStatus", CERT_TRUST_STATUS),
        ("cElement", DWORD),
        ("rgpElement", ctypes.POINTER(PCERT_CHAIN_ELEMENT)),
        ("pTrustListInfo", LPVOID),
        ("fHasRevocationFreshnessTime", BOOL),
        ("dwRevocationFreshnessTime", DWORD),
    ]


PCERT_SIMPLE_CHAIN = ctypes.POINTER(CERT_SIMPLE_CHAIN)


class CERT_CHAIN_CONTEXT(ctypes.Structure):
    pass


PCERT_CHAIN_CONTEXT = ctypes.POINTER(CERT_CHAIN_CONTEXT)
CERT_CHAIN_CONTEXT._fields_ = [
    ("cbSize", DWORD),
    ("TrustStatus", CERT_TRUST_STATUS),
    ("cChain", DWORD),
    ("rgpChain", ctypes.POINTER(PCERT_SIMPLE_CHAIN)),
    ("cLowerQualityChainContext", DWORD),
    ("rgpLowerQualityChainContext", ctypes.POINTER(PCERT_CHAIN_CONTEXT)),
    ("fHasRevocationFreshnessTime", BOOL),
    ("dwRevocationFreshnessTime", DWORD),
    ("dwCreateFlags", DWORD),
    ("ChainId", GUID),
]


class CTL_USAGE(ctypes.Structure):
    _fields_ = [("cUsageIdentifier", DWORD), ("rgpszUsageIdentifier", ctypes.POINTER(ctypes.c_char_p))]


class CERT_USAGE_MATCH(ctypes.Structure):
    _fields_ = [("dwType", DWORD), ("Usage", CTL_USAGE)]


class CERT_CHAIN_PARA(ctypes.Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("RequestedUsage", CERT_USAGE_MATCH),
        ("RequestedIssuancePolicy", CERT_USAGE_MATCH),
        ("dwUrlRetrievalTimeout", DWORD),
        ("fCheckRevocationFreshnessTime", BOOL),
        ("dwRevocationFreshnessTime", DWORD),
        ("pftCacheResync", ctypes.POINTER(FILETIME)),
        ("pStrongSignPara", LPVOID),
        ("dwStrongSignFlags", DWORD),
    ]


class CERT_CHAIN_POLICY_PARA(ctypes.Structure):
    _fields_ = [("cbSize", DWORD), ("dwFlags", DWORD), ("pvExtraPolicyPara", LPVOID)]


class CERT_CHAIN_POLICY_STATUS(ctypes.Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("dwError", DWORD),
        ("lChainIndex", wintypes.LONG),
        ("lElementIndex", wintypes.LONG),
        ("pvExtraPolicyStatus", LPVOID),
    ]


class CRYPT_PROVIDER_CERT(ctypes.Structure):
    _fields_ = [
        ("cbStruct", DWORD),
        ("pCert", PCERT_CONTEXT),
        ("fCommercial", BOOL),
        ("fTrustedRoot", BOOL),
        ("fSelfSigned", BOOL),
        ("fTestCert", BOOL),
        ("dwRevokedReason", DWORD),
        ("dwConfidence", DWORD),
        ("dwError", DWORD),
        ("pTrustListContext", LPVOID),
        ("fTrustListSignerCert", BOOL),
        ("pCtlContext", LPVOID),
        ("dwCtlError", DWORD),
        ("fIsCyclic", BOOL),
        ("pChainElement", PCERT_CHAIN_ELEMENT),
    ]


class CRYPT_PROVIDER_SGNR(ctypes.Structure):
    pass


PCRYPT_PROVIDER_SGNR = ctypes.POINTER(CRYPT_PROVIDER_SGNR)
CRYPT_PROVIDER_SGNR._fields_ = [
    ("cbStruct", DWORD),
    ("sftVerifyAsOf", FILETIME),
    ("csCertChain", DWORD),
    ("pasCertChain", ctypes.POINTER(CRYPT_PROVIDER_CERT)),
    ("dwSignerType", DWORD),
    ("psSigner", LPVOID),
    ("dwError", DWORD),
    ("csCounterSigners", DWORD),
    ("pasCounterSigners", PCRYPT_PROVIDER_SGNR),
    ("pChainContext", PCERT_CHAIN_CONTEXT),
]


class WINTRUST_FILE_INFO(ctypes.Structure):
    _fields_ = [
        ("cbStruct", DWORD),
        ("pcwszFilePath", wintypes.LPCWSTR),
        ("hFile", HANDLE),
        ("pgKnownSubject", ctypes.POINTER(GUID)),
    ]


class WINTRUST_DATA_UNION(ctypes.Union):
    _fields_ = [("pFile", ctypes.POINTER(WINTRUST_FILE_INFO)), ("pointer", LPVOID)]


class WINTRUST_DATA(ctypes.Structure):
    _anonymous_ = ("choice",)
    _fields_ = [
        ("cbStruct", DWORD),
        ("pPolicyCallbackData", LPVOID),
        ("pSIPClientData", LPVOID),
        ("dwUIChoice", DWORD),
        ("fdwRevocationChecks", DWORD),
        ("dwUnionChoice", DWORD),
        ("choice", WINTRUST_DATA_UNION),
        ("dwStateAction", DWORD),
        ("hWVTStateData", HANDLE),
        ("pwszURLReference", wintypes.LPWSTR),
        ("dwProvFlags", DWORD),
        ("dwUIContext", DWORD),
        ("pSignatureSettings", LPVOID),
    ]


class FILE_ID_128(ctypes.Structure):
    _fields_ = [("Identifier", ctypes.c_ubyte * 16)]


class FILE_ID_INFO(ctypes.Structure):
    _fields_ = [("VolumeSerialNumber", ctypes.c_ulonglong), ("FileId", FILE_ID_128)]


class FILE_ATTRIBUTE_TAG_INFO(ctypes.Structure):
    _fields_ = [("FileAttributes", DWORD), ("ReparseTag", DWORD)]


class CTL_CONTEXT(ctypes.Structure):
    _fields_ = [
        ("dwMsgAndCertEncodingType", DWORD),
        ("pbCtlEncoded", ctypes.POINTER(ctypes.c_ubyte)),
        ("cbCtlEncoded", DWORD),
        ("pCtlInfo", LPVOID),
        ("hCertStore", HANDLE),
        ("hCryptMsg", HANDLE),
        ("pbCtlContent", ctypes.POINTER(ctypes.c_ubyte)),
        ("cbCtlContent", DWORD),
    ]


PCCTL_CONTEXT = ctypes.POINTER(CTL_CONTEXT)


WTD_UI_NONE = 2
WTD_REVOKE_NONE = 0
WTD_CHOICE_FILE = 1
WTD_STATEACTION_VERIFY = 1
WTD_STATEACTION_CLOSE = 2
WTD_DISABLE_MD2_MD4 = 0x2000
WTD_MOTW = 0x4000
WTD_UICONTEXT_INSTALL = 1
CERT_CHAIN_REVOCATION_ACCUMULATIVE_TIMEOUT = 0x08000000
CERT_CHAIN_TIMESTAMP_TIME = 0x00000200
CERT_CHAIN_REVOCATION_CHECK_CHAIN_EXCLUDE_ROOT = 0x40000000
CERT_SYSTEM_STORE_LOCAL_MACHINE = 0x00020000
CERT_STORE_OPEN_EXISTING_FLAG = 0x00004000
CERT_STORE_READONLY_FLAG = 0x00008000
CERT_STORE_PROV_SYSTEM_W = 10
CRYPT_E_NOT_FOUND = 0x80092004
FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
FILE_ATTRIBUTE_NORMAL = 0x00000080
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
FILE_FLAG_SEQUENTIAL_SCAN = 0x08000000
FILE_ATTRIBUTE_TAG_INFO_CLASS = 9
FILE_ID_INFO_CLASS = 18
GENERIC_READ = 0x80000000
FILE_SHARE_READ = 0x00000001
OPEN_EXISTING = 3
FILE_BEGIN = 0
CERT_TRUST_IS_EXPLICIT_DISTRUST = 0x04000000
POLICY_AUTHENTICODE = 2
POLICY_AUTHENTICODE_TS = 3
POLICY_MICROSOFT_ROOT = 7
HCCE_LOCAL_MACHINE = 1
SGNR_TYPE_TIMESTAMP = 0x00000010


def _guid(value: str) -> GUID:
    parsed = uuid.UUID(value.strip("{}"))
    fields = parsed.fields
    data4 = (ctypes.c_ubyte * 8)(fields[3], fields[4], *fields[5].to_bytes(6, "big"))
    return GUID(fields[0], fields[1], fields[2], data4)


def _filetime_int(value: FILETIME) -> int:
    return (int(value.dwHighDateTime) << 32) | int(value.dwLowDateTime)


def _int_filetime(value: int) -> FILETIME:
    return FILETIME(value & 0xFFFFFFFF, (value >> 32) & 0xFFFFFFFF)


def _cert_sha256(context: PCERT_CONTEXT) -> str:
    if not context or not context.contents.pbCertEncoded or context.contents.cbCertEncoded == 0:
        raise NativeVerificationError("certificate context is absent")
    if int(context.contents.cbCertEncoded) > MAX_CERTIFICATE_BYTES:
        raise NativeVerificationError("certificate encoding exceeds the public bound")
    return hashlib.sha256(
        ctypes.string_at(context.contents.pbCertEncoded, context.contents.cbCertEncoded)
    ).hexdigest()


class _Apis:
    def __init__(self) -> None:
        if os.name != "nt":
            raise NativeVerificationError("Windows native APIs are unavailable")
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.wintrust = ctypes.WinDLL("wintrust", use_last_error=True)
        self.crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)

        self.kernel32.GetSystemTimeAsFileTime.argtypes = [ctypes.POINTER(FILETIME)]
        self.kernel32.GetFileInformationByHandleEx.argtypes = [HANDLE, ctypes.c_int, LPVOID, DWORD]
        self.kernel32.GetFileInformationByHandleEx.restype = BOOL
        self.kernel32.GetFileSizeEx.argtypes = [HANDLE, ctypes.POINTER(ctypes.c_longlong)]
        self.kernel32.GetFileSizeEx.restype = BOOL
        self.kernel32.GetFinalPathNameByHandleW.argtypes = [HANDLE, wintypes.LPWSTR, DWORD, DWORD]
        self.kernel32.GetFinalPathNameByHandleW.restype = DWORD
        self.kernel32.SetFilePointerEx.argtypes = [HANDLE, ctypes.c_longlong, ctypes.POINTER(ctypes.c_longlong), DWORD]
        self.kernel32.SetFilePointerEx.restype = BOOL
        self.kernel32.ReadFile.argtypes = [HANDLE, LPVOID, DWORD, ctypes.POINTER(DWORD), LPVOID]
        self.kernel32.ReadFile.restype = BOOL
        self.kernel32.CreateFileW.argtypes = [
            wintypes.LPCWSTR, DWORD, DWORD, LPVOID, DWORD, DWORD, HANDLE,
        ]
        self.kernel32.CreateFileW.restype = HANDLE
        self.kernel32.CloseHandle.argtypes = [HANDLE]
        self.kernel32.CloseHandle.restype = BOOL

        self.wintrust.WinVerifyTrust.argtypes = [HANDLE, ctypes.POINTER(GUID), ctypes.POINTER(WINTRUST_DATA)]
        self.wintrust.WinVerifyTrust.restype = wintypes.LONG
        self.wintrust.WTHelperProvDataFromStateData.argtypes = [HANDLE]
        self.wintrust.WTHelperProvDataFromStateData.restype = LPVOID
        self.wintrust.WTHelperGetProvSignerFromChain.argtypes = [LPVOID, DWORD, BOOL, DWORD]
        self.wintrust.WTHelperGetProvSignerFromChain.restype = PCRYPT_PROVIDER_SGNR

        self.crypt32.CertGetCertificateChain.argtypes = [
            HANDLE, PCERT_CONTEXT, ctypes.POINTER(FILETIME), HANDLE,
            ctypes.POINTER(CERT_CHAIN_PARA), DWORD, LPVOID,
            ctypes.POINTER(PCERT_CHAIN_CONTEXT),
        ]
        self.crypt32.CertGetCertificateChain.restype = BOOL
        self.crypt32.CertFreeCertificateChain.argtypes = [PCERT_CHAIN_CONTEXT]
        self.crypt32.CertVerifyCertificateChainPolicy.argtypes = [
            LPVOID, PCERT_CHAIN_CONTEXT, ctypes.POINTER(CERT_CHAIN_POLICY_PARA),
            ctypes.POINTER(CERT_CHAIN_POLICY_STATUS),
        ]
        self.crypt32.CertVerifyCertificateChainPolicy.restype = BOOL
        self.crypt32.CertOpenStore.argtypes = [LPVOID, DWORD, HANDLE, DWORD, LPVOID]
        self.crypt32.CertOpenStore.restype = HANDLE
        self.crypt32.CertCloseStore.argtypes = [HANDLE, DWORD]
        self.crypt32.CertCloseStore.restype = BOOL
        self.crypt32.CertEnumCertificatesInStore.argtypes = [HANDLE, PCERT_CONTEXT]
        self.crypt32.CertEnumCertificatesInStore.restype = PCERT_CONTEXT
        self.crypt32.CertEnumCTLsInStore.argtypes = [HANDLE, PCCTL_CONTEXT]
        self.crypt32.CertEnumCTLsInStore.restype = PCCTL_CONTEXT


def _now_filetime(api: _Apis) -> int:
    value = FILETIME()
    api.kernel32.GetSystemTimeAsFileTime(ctypes.byref(value))
    return _filetime_int(value)


def _file_identity(api: _Apis, handle: int) -> dict[str, object]:
    file_id = FILE_ID_INFO()
    attributes = FILE_ATTRIBUTE_TAG_INFO()
    size = ctypes.c_longlong()
    native = HANDLE(handle)
    if not api.kernel32.GetFileInformationByHandleEx(native, FILE_ID_INFO_CLASS, ctypes.byref(file_id), ctypes.sizeof(file_id)):
        raise NativeVerificationError("file ID query failed")
    if not api.kernel32.GetFileInformationByHandleEx(native, FILE_ATTRIBUTE_TAG_INFO_CLASS, ctypes.byref(attributes), ctypes.sizeof(attributes)):
        raise NativeVerificationError("file attribute query failed")
    if (
        not api.kernel32.GetFileSizeEx(native, ctypes.byref(size))
        or size.value <= 0
        or size.value > MAX_CANDIDATE_BYTES
    ):
        raise NativeVerificationError("file size query failed")
    return {
        "volume_serial_hex": f"{int(file_id.VolumeSerialNumber):016x}",
        "file_id_hex": bytes(file_id.FileId.Identifier).hex(),
        "reparse_point": bool(attributes.FileAttributes & FILE_ATTRIBUTE_REPARSE_POINT),
        "byte_length": int(size.value),
    }


def _handle_path(api: _Apis, handle: int) -> str:
    capacity = 512
    while capacity <= 32768:
        buffer = ctypes.create_unicode_buffer(capacity)
        length = int(api.kernel32.GetFinalPathNameByHandleW(HANDLE(handle), buffer, capacity, 0))
        if length == 0:
            raise NativeVerificationError("final handle path query failed")
        if length < capacity:
            value = buffer.value
            if value.startswith("\\\\?\\UNC\\"):
                return "\\\\" + value[8:]
            if value.startswith("\\\\?\\"):
                return value[4:]
            return value
        capacity = length + 1
    raise NativeVerificationError("final handle path is unbounded")


def _workspace_root() -> Path:
    source = Path(__file__).resolve()
    for parent in source.parents:
        if (parent / "AGENTS.md").is_file():
            return parent
    raise NativeVerificationError("workspace root is unavailable")


def _open_immutable_read_lease(api: _Apis, path: Path) -> int:
    value = api.kernel32.CreateFileW(
        str(path),
        GENERIC_READ,
        FILE_SHARE_READ,
        None,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OPEN_REPARSE_POINT | FILE_FLAG_SEQUENTIAL_SCAN,
        None,
    )
    invalid = ctypes.c_void_p(-1).value
    if value is None or int(value) == int(invalid):
        raise NativeVerificationError(
            "private read lease failed; write/delete access or writable mapping may exist"
        )
    return int(value)


def _close_owned_handle(api: _Apis, handle: int) -> None:
    if not api.kernel32.CloseHandle(HANDLE(handle)):
        raise NativeVerificationError("owned file handle close failed")


def _hash_owned_handle(api: _Apis, handle: int) -> str:
    """Hash one verifier-owned handle without sharing a file pointer."""

    identity = _file_identity(api, handle)
    expected_length = int(identity["byte_length"])
    native = HANDLE(handle)
    if not api.kernel32.SetFilePointerEx(native, 0, None, FILE_BEGIN):
        raise NativeVerificationError("owned file rewind failed")
    digest = hashlib.sha256()
    remaining = expected_length
    buffer = ctypes.create_string_buffer(1024 * 1024)
    while remaining:
        requested = min(remaining, len(buffer))
        consumed = DWORD()
        if not api.kernel32.ReadFile(
            native,
            buffer,
            requested,
            ctypes.byref(consumed),
            None,
        ):
            raise NativeVerificationError("owned file read failed")
        count = int(consumed.value)
        if count <= 0 or count > requested:
            raise NativeVerificationError("owned file ended before its bound length")
        digest.update(buffer.raw[:count])
        remaining -= count
    extra = DWORD()
    if not api.kernel32.ReadFile(native, buffer, 1, ctypes.byref(extra), None):
        raise NativeVerificationError("owned file terminal read failed")
    if int(extra.value) != 0:
        raise NativeVerificationError("owned file exceeded its bound length")
    if not api.kernel32.SetFilePointerEx(native, 0, None, FILE_BEGIN):
        raise NativeVerificationError("owned file final rewind failed")
    return digest.hexdigest()


def _store_snapshot(api: _Apis) -> dict[str, object]:
    entries: list[str] = []
    stores = (
        "ROOT",
        "CA",
        "MY",
        "TRUST",
        "AuthRoot",
        "Disallowed",
    )
    for store_name in stores:
        name = ctypes.c_wchar_p(store_name)
        store = api.crypt32.CertOpenStore(
            LPVOID(CERT_STORE_PROV_SYSTEM_W),
            0,
            None,
            CERT_SYSTEM_STORE_LOCAL_MACHINE | CERT_STORE_OPEN_EXISTING_FLAG | CERT_STORE_READONLY_FLAG,
            ctypes.cast(name, LPVOID),
        )
        if not store:
            raise NativeVerificationError("system certificate store open failed")
        try:
            cert = PCERT_CONTEXT()
            while True:
                ctypes.set_last_error(0)
                cert = api.crypt32.CertEnumCertificatesInStore(store, cert)
                if not cert:
                    if ctypes.get_last_error() & 0xFFFFFFFF != CRYPT_E_NOT_FOUND:
                        raise NativeVerificationError("certificate enumeration failed")
                    break
                entries.append(f"{store_name}:CERT:{_cert_sha256(cert)}")
                if len(entries) > MAX_STORE_ENTRIES:
                    raise NativeVerificationError("store snapshot exceeds the public bound")
            ctl = PCCTL_CONTEXT()
            while True:
                ctypes.set_last_error(0)
                ctl = api.crypt32.CertEnumCTLsInStore(store, ctl)
                if not ctl:
                    if ctypes.get_last_error() & 0xFFFFFFFF != CRYPT_E_NOT_FOUND:
                        raise NativeVerificationError("CTL enumeration failed")
                    break
                if not ctl.contents.pbCtlEncoded or ctl.contents.cbCtlEncoded == 0:
                    raise NativeVerificationError("CTL encoding is absent")
                if int(ctl.contents.cbCtlEncoded) > MAX_CTL_BYTES:
                    raise NativeVerificationError("CTL encoding exceeds the public bound")
                digest = hashlib.sha256(
                    ctypes.string_at(ctl.contents.pbCtlEncoded, ctl.contents.cbCtlEncoded)
                ).hexdigest()
                entries.append(f"{store_name}:CTL:{digest}")
                if len(entries) > MAX_STORE_ENTRIES:
                    raise NativeVerificationError("store snapshot exceeds the public bound")
        finally:
            if not api.crypt32.CertCloseStore(store, 0):
                raise NativeVerificationError("certificate store close failed")
    return {
        "sha256": sha256_hex(canonical_json_lf(sorted(entries))),
        "entry_count": len(entries),
    }


def _provider_chain(signer: PCRYPT_PROVIDER_SGNR) -> list[str]:
    if not signer or signer.contents.csCertChain < 2 or not signer.contents.pasCertChain:
        raise NativeVerificationError("provider signer chain is absent")
    if int(signer.contents.csCertChain) > MAX_PROVIDER_CHAIN_CERTIFICATES:
        raise NativeVerificationError("provider signer chain exceeds the public bound")
    if int(signer.contents.dwError) != 0:
        raise NativeVerificationError("provider signer error is nonzero")
    for index in range(signer.contents.csCertChain):
        provider_cert = signer.contents.pasCertChain[index]
        if int(provider_cert.dwError) != 0 or bool(provider_cert.fTestCert):
            raise NativeVerificationError("provider certificate error or test certificate observed")
    return [
        _cert_sha256(signer.contents.pasCertChain[index].pCert)
        for index in range(signer.contents.csCertChain)
    ]


def _chain_rows(chain: PCERT_CHAIN_CONTEXT) -> list[dict[str, object]]:
    if not chain or chain.contents.cChain != 1 or not chain.contents.rgpChain:
        raise NativeVerificationError("chain context is not one simple chain")
    simple = chain.contents.rgpChain[0]
    if not simple or simple.contents.cElement < 2 or not simple.contents.rgpElement:
        raise NativeVerificationError("simple chain is incomplete")
    rows: list[dict[str, object]] = []
    count = int(simple.contents.cElement)
    if count > MAX_REBUILT_CHAIN_CERTIFICATES:
        raise NativeVerificationError("rebuilt chain exceeds the public bound")
    for index in range(count):
        pointer = simple.contents.rgpElement[index]
        if not pointer:
            raise NativeVerificationError("chain element is absent")
        element = pointer.contents
        root = index == count - 1
        revocation = element.pRevocationInfo
        if root:
            result = "ROOT-NOT-CHECKED"
            has_freshness = False
            age = None
        else:
            if not revocation:
                result = "UNCHECKED"
                has_freshness = False
                age = None
            else:
                result_code = int(revocation.contents.dwRevocationResult)
                result = "GOOD" if result_code == 0 else f"ERROR-0x{result_code:08x}"
                has_freshness = bool(revocation.contents.fHasFreshnessTime)
                age = int(revocation.contents.dwFreshnessTime) if has_freshness else None
        rows.append(
            {
                "position": index,
                "role": "LEAF" if index == 0 else "ROOT" if root else "INTERMEDIATE",
                "certificate_der_sha256": _cert_sha256(element.pCertContext),
                "trust_error_status": int(element.TrustStatus.dwErrorStatus),
                "trust_info_status": int(element.TrustStatus.dwInfoStatus),
                "revocation_result": result,
                "has_freshness_time": has_freshness,
                "freshness_age_seconds": age,
                "disallowed": bool(int(element.TrustStatus.dwErrorStatus) & CERT_TRUST_IS_EXPLICIT_DISTRUST),
            }
        )
    return rows


def _build_chain(
    api: _Apis,
    cert: PCERT_CONTEXT,
    verification_time: int,
    eku: str,
) -> tuple[PCERT_CHAIN_CONTEXT, list[dict[str, object]], dict[str, object]]:
    usage_values = (ctypes.c_char_p * 1)(eku.encode("ascii"))
    usage = CTL_USAGE(1, usage_values)
    match = CERT_USAGE_MATCH(0, usage)
    empty = CERT_USAGE_MATCH(0, CTL_USAGE(0, None))
    call_started = _now_filetime(api)
    cache_resync_time = (
        call_started - MAX_REVOCATION_FRESHNESS_SECONDS * FILETIME_TICKS_PER_SECOND
    )
    if cache_resync_time <= 0:
        raise NativeVerificationError("cache resync time is outside the exact range")
    cutoff = _int_filetime(cache_resync_time)
    params = CERT_CHAIN_PARA(
        ctypes.sizeof(CERT_CHAIN_PARA),
        match,
        empty,
        URL_RETRIEVAL_TIMEOUT_MS,
        True,
        MAX_REVOCATION_FRESHNESS_SECONDS,
        ctypes.pointer(cutoff),
        None,
        0,
    )
    ptime = _int_filetime(verification_time)
    flags = CERT_CHAIN_REVOCATION_CHECK_CHAIN_EXCLUDE_ROOT | CERT_CHAIN_REVOCATION_ACCUMULATIVE_TIMEOUT | CERT_CHAIN_TIMESTAMP_TIME
    context = PCERT_CHAIN_CONTEXT()
    succeeded = bool(
        api.crypt32.CertGetCertificateChain(
            HANDLE(HCCE_LOCAL_MACHINE),
            cert,
            ctypes.byref(ptime),
            None,
            ctypes.byref(params),
            flags,
            None,
            ctypes.byref(context),
        )
    )
    call_returned = _now_filetime(api)
    if not succeeded or not context:
        if context:
            api.crypt32.CertFreeCertificateChain(context)
        raise NativeVerificationError("certificate chain build failed")
    try:
        duration = call_returned - call_started
        if (
            duration < 0
            or duration
            > MAX_CHAIN_CALL_DURATION_SECONDS * FILETIME_TICKS_PER_SECOND
        ):
            raise NativeVerificationError("chain call clock interval differs")
        rows = _chain_rows(context)
        output_sha256 = sha256_hex(canonical_json_lf(rows))
        call: dict[str, object] = {
            "api": "CertGetCertificateChain",
            "chain_engine": CHAIN_ENGINE,
            "flags": list(CHAIN_FLAGS),
            "url_retrieval_timeout_ms": URL_RETRIEVAL_TIMEOUT_MS,
            "leaf_certificate_der_sha256": _cert_sha256(cert),
            "verification_time_filetime_hex": f"{verification_time:016x}",
            "cache_resync_filetime_hex": f"{cache_resync_time:016x}",
            "call_started_filetime_hex": f"{call_started:016x}",
            "call_returned_filetime_hex": f"{call_returned:016x}",
            "requested_eku": eku,
            "additional_candidate_store_used": False,
            "api_return": True,
            "output_chain_sha256": output_sha256,
            "input_sha256": "",
        }
        call["input_sha256"] = chain_call_input_sha256(call)
        return context, rows, call
    except Exception:
        api.crypt32.CertFreeCertificateChain(context)
        raise


def _policy(
    api: _Apis,
    policy_id: int,
    policy_name: str,
    chain: PCERT_CHAIN_CONTEXT,
    chain_sha256: str,
    verification_time: int,
    extra_policy: dict[str, object],
) -> dict[str, object]:
    params = CERT_CHAIN_POLICY_PARA(ctypes.sizeof(CERT_CHAIN_POLICY_PARA), 0, None)
    status = CERT_CHAIN_POLICY_STATUS(ctypes.sizeof(CERT_CHAIN_POLICY_STATUS), 0, -1, -1, None)
    succeeded = bool(
        api.crypt32.CertVerifyCertificateChainPolicy(
            LPVOID(policy_id), chain, ctypes.byref(params), ctypes.byref(status)
        )
    )
    result: dict[str, object] = {
        "policy_id": policy_name,
        "chain_context_sha256": chain_sha256,
        "verification_time_filetime_hex": f"{verification_time:016x}",
        "flags": 0,
        "extra_policy": extra_policy,
        "api_return": succeeded,
        "policy_error": int(status.dwError),
        "input_sha256": "",
    }
    result["input_sha256"] = policy_input_sha256(result)
    return result


def _event(index: int, state_id: str | None) -> dict[str, object]:
    return {"sequence": index, "kind": EVENT_SEQUENCE[index], "provider_state_id": state_id}


def collect_observation(
    *,
    full_path: str,
    file_handle: int,
    authority: VerificationAuthority,
    acquisition: AcquisitionEvidence,
    process_count_before_decision: int = 0,
) -> bytes:
    """Collect one complete bounded observation without executing the file."""

    if os.name != "nt" or type(file_handle) is not int or file_handle <= 0:
        raise NativeVerificationError("one valid Windows file handle is required")
    if type(acquisition) is not AcquisitionEvidence:
        raise NativeVerificationError("authenticated acquisition evidence is required")
    if (
        acquisition.record_sha256 != authority.acquisition_record_sha256
        or acquisition.authority_manifest_sha256
        != authority.acquisition_authority_manifest_sha256
    ):
        raise NativeVerificationError("acquisition authority copy differs")
    path = Path(full_path)
    if not path.is_absolute():
        raise NativeVerificationError("candidate path is not absolute")
    api = _Apis()
    actual_path = Path(_handle_path(api, file_handle)).resolve()
    requested_path = path.resolve()
    if os.path.normcase(str(actual_path)) != os.path.normcase(str(requested_path)):
        raise NativeVerificationError("file handle and requested path differ")
    workspace = _workspace_root()
    try:
        actual_path.relative_to(workspace)
    except ValueError:
        pass
    else:
        raise NativeVerificationError("candidate file is inside the repository")

    lease_handle = _open_immutable_read_lease(api, actual_path)
    try:
        lease_path = Path(_handle_path(api, lease_handle)).resolve()
        if os.path.normcase(str(lease_path)) != os.path.normcase(str(actual_path)):
            raise NativeVerificationError("private lease resolved to another path")
        supplied_identity = _file_identity(api, file_handle)
        lease_identity = _file_identity(api, lease_handle)
        acquisition_record = acquisition.record()
        if (
            supplied_identity != lease_identity
            or acquisition_record["file_identity"] != lease_identity
        ):
            raise NativeVerificationError("acquisition and lease file identities differ")
        lease_hash = _hash_owned_handle(api, lease_handle)
        if acquisition_record["byte_sha256"] != lease_hash:
            raise NativeVerificationError("acquisition and lease byte hashes differ")

        events = [_event(0, None), _event(1, None)]
        trust_pre = _store_snapshot(api)
        events.append(_event(2, None))

        action = _guid(WINTRUST_ACTION_GUID)
        file_info = WINTRUST_FILE_INFO(
            ctypes.sizeof(WINTRUST_FILE_INFO),
            str(lease_path),
            HANDLE(lease_handle),
            None,
        )
        data = WINTRUST_DATA()
        data.cbStruct = ctypes.sizeof(WINTRUST_DATA)
        data.dwUIChoice = WTD_UI_NONE
        data.fdwRevocationChecks = WTD_REVOKE_NONE
        data.dwUnionChoice = WTD_CHOICE_FILE
        data.pFile = ctypes.pointer(file_info)
        data.dwStateAction = WTD_STATEACTION_VERIFY
        data.dwProvFlags = WTD_DISABLE_MD2_MD4 | WTD_MOTW
        data.dwUIContext = WTD_UICONTEXT_INSTALL

        verify_called = False
        verify_return: int | None = None
        close_return: int | None = None
        state_id: str | None = None
        signer_chain_context = PCERT_CHAIN_CONTEXT()
        timestamp_chain_context = PCERT_CHAIN_CONTEXT()
        try:
            verify_called = True
            verify_return = int(
                api.wintrust.WinVerifyTrust(
                    HANDLE(-1),
                    ctypes.byref(action),
                    ctypes.byref(data),
                )
            )
            if not data.hWVTStateData:
                raise NativeVerificationError("WinVerifyTrust did not return provider state")
            state_id = sha256_hex(
                f"pid={os.getpid()}\nstate={int(data.hWVTStateData):016x}\n".encode(
                    "ascii"
                )
            )
            events.append(_event(3, state_id))
            events.append(_event(4, state_id))
            if verify_return != 0:
                raise NativeVerificationError("WinVerifyTrust returned nonzero")
            provider_data = api.wintrust.WTHelperProvDataFromStateData(
                data.hWVTStateData
            )
            if not provider_data:
                raise NativeVerificationError("provider data extraction failed")
            signer = api.wintrust.WTHelperGetProvSignerFromChain(
                provider_data, 0, False, 0
            )
            if not signer:
                raise NativeVerificationError("signer is absent")
            events.append(_event(5, state_id))
            countersigner = api.wintrust.WTHelperGetProvSignerFromChain(
                provider_data, 0, True, 0
            )
            if not countersigner:
                raise NativeVerificationError("mandatory countersigner is absent")
            if int(countersigner.contents.dwSignerType) != SGNR_TYPE_TIMESTAMP:
                raise NativeVerificationError(
                    "provider countersigner is not a timestamp signer"
                )
            events.append(_event(6, state_id))
            signer_provider_chain = _provider_chain(signer)
            timestamp_provider_chain = _provider_chain(countersigner)
            signing_time = _filetime_int(countersigner.contents.sftVerifyAsOf)
            if signing_time <= 0:
                raise NativeVerificationError("timestamp signing time is absent")
            signer_cert = signer.contents.pasCertChain[0].pCert
            timestamp_cert = countersigner.contents.pasCertChain[0].pCert
            signer_chain_context, signer_rows, signer_call = _build_chain(
                api,
                signer_cert,
                signing_time,
                CODE_SIGNING_EKU,
            )
            events.append(_event(7, state_id))
            signer_auth = _policy(
                api,
                POLICY_AUTHENTICODE,
                "CERT_CHAIN_POLICY_AUTHENTICODE",
                signer_chain_context,
                signer_call["output_chain_sha256"],
                signing_time,
                {"pv_extra_policy_para": "NULL"},
            )
            signer_ms = _policy(
                api,
                POLICY_MICROSOFT_ROOT,
                "CERT_CHAIN_POLICY_MICROSOFT_ROOT",
                signer_chain_context,
                signer_call["output_chain_sha256"],
                signing_time,
                {"test_root_enabled": False},
            )
            events.append(_event(8, state_id))
            timestamp_chain_context, timestamp_rows, timestamp_call = _build_chain(
                api,
                timestamp_cert,
                signing_time,
                TIME_STAMPING_EKU,
            )
            events.append(_event(9, state_id))
            timestamp_auth = _policy(
                api,
                POLICY_AUTHENTICODE_TS,
                "CERT_CHAIN_POLICY_AUTHENTICODE_TS",
                timestamp_chain_context,
                timestamp_call["output_chain_sha256"],
                signing_time,
                {"pv_extra_policy_para": "NULL"},
            )
            events.append(_event(10, state_id))
            post_identity = _file_identity(api, lease_handle)
            post_hash = _hash_owned_handle(api, lease_handle)
            trust_post = _store_snapshot(api)
            events.append(_event(11, state_id))
        finally:
            if signer_chain_context:
                api.crypt32.CertFreeCertificateChain(signer_chain_context)
            if timestamp_chain_context:
                api.crypt32.CertFreeCertificateChain(timestamp_chain_context)
            if verify_called:
                data.dwStateAction = WTD_STATEACTION_CLOSE
                close_return = int(
                    api.wintrust.WinVerifyTrust(
                        HANDLE(-1),
                        ctypes.byref(action),
                        ctypes.byref(data),
                    )
                )
                if state_id is not None:
                    events.append(_event(12, state_id))

        if close_return != 0:
            raise NativeVerificationError("WinVerifyTrust CLOSE returned nonzero")
        preexecution_identity = _file_identity(api, lease_handle)
        preexecution_hash = _hash_owned_handle(api, lease_handle)
        events.append(_event(13, None))
        if tuple(event["kind"] for event in events) != EVENT_SEQUENCE:
            raise NativeVerificationError("native event sequence differs")
        observation = {
            "schema_id": OBSERVATION_SCHEMA_ID,
            "native_collection_status": "COMPLETED-NONAUTHORITATIVE-OBSERVATION",
            "implementation_manifest_sha256": authority.implementation_manifest_sha256,
            "policy_manifest_sha256": authority.policy_manifest_sha256,
            "acquisition_validator_manifest_sha256": (
                authority.acquisition_validator_manifest_sha256
            ),
            "native_verifier_manifest_sha256": (
                authority.native_verifier_manifest_sha256
            ),
            "semantic_validator_manifest_sha256": (
                authority.semantic_validator_manifest_sha256
            ),
            "runtime_authority": {
                "scope": RUNTIME_AUTHORITY_SCOPE,
                "executed_code_authority_established": False,
            },
            "acquisition_record": acquisition_record,
            "acquisition_record_sha256": acquisition.record_sha256,
            "runtime_binding": {
                "consumer_process_id": os.getpid(),
                "supplied_handle_hex": f"{file_handle:016x}",
                "immutable_lease_contract": dict(IMMUTABLE_LEASE_CONTRACT),
            },
            "supplier": {
                "criterion_id": SUPPLIER_CRITERION_ID,
                "components": list(SUPPLIER_CRITERION_COMPONENTS),
                "official_leaf_guarantee_claimed": False,
                "project_reauthorization_acknowledged": True,
            },
            "file_identities": {
                "lease_open": lease_identity,
                "post_signature": post_identity,
                "preexecution": preexecution_identity,
            },
            "byte_sha256": {
                "lease_open": lease_hash,
                "post_signature": post_hash,
                "preexecution": preexecution_hash,
            },
            "wintrust": {
                "action_guid": WINTRUST_ACTION_GUID,
                "window_handle": "INVALID_HANDLE_VALUE",
                "ui_choice": "WTD_UI_NONE",
                "ui_context": "WTD_UICONTEXT_INSTALL",
                "union_choice": "WTD_CHOICE_FILE",
                "revocation_checks": "WTD_REVOKE_NONE",
                "prov_flags": list(WINTRUST_PROV_FLAGS),
                "state_action_verify": "WTD_STATEACTION_VERIFY",
                "verify_return": verify_return,
                "state_action_close": "WTD_STATEACTION_CLOSE",
                "close_return": close_return,
                "provider_state_id": state_id,
                "candidate_callback_used": False,
                "candidate_store_used": False,
                "custom_parser_used": False,
            },
            "events": events,
            "signer": {
                "leaf_certificate_der_sha256": signer_provider_chain[0],
                "provider_chain": signer_provider_chain,
                "rebuilt_chain": signer_rows,
                "chain_call": signer_call,
                "code_signing_eku_present": signer_call["api_return"],
                "authenticode_policy": signer_auth,
                "microsoft_root_policy": signer_ms,
            },
            "timestamp": {
                "present": True,
                "kind": "WINDOWS-PROVIDER-TIMESTAMP-SIGNER",
                "signer_index": 0,
                "countersigner_index": 0,
                "provider_state_id": state_id,
                "signing_time_filetime_hex": f"{signing_time:016x}",
                "leaf_certificate_der_sha256": timestamp_provider_chain[0],
                "provider_chain": timestamp_provider_chain,
                "rebuilt_chain": timestamp_rows,
                "chain_call": timestamp_call,
                "timestamp_policy": timestamp_auth,
            },
            "trust_authority": {
                "pre_snapshot": trust_pre,
                "post_snapshot": trust_post,
                "snapshot_scope": list(TRUST_SNAPSHOT_SCOPE),
                "enumeration_complete": True,
                "store_close_success": True,
                "effective_trust_authority_claimed": False,
                "store_mutation_count": 0 if trust_pre == trust_post else 1,
            },
            "process_count_before_decision": process_count_before_decision,
        }
        raw = canonical_json_lf(observation)
        if len(raw) > MAX_OBSERVATION_BYTES:
            raise NativeVerificationError("observation exceeds the public byte bound")
        return raw
    finally:
        _close_owned_handle(api, lease_handle)
