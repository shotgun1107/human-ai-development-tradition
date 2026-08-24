"""Windows ctypes collector for one retained, already-downloaded file handle.

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

from .canonical import VerificationError, canonical_json_lf, sha256_hex
from .contract import (
    CHAIN_ENGINE,
    CHAIN_FLAGS,
    CODE_SIGNING_EKU,
    EVENT_SEQUENCE,
    FIXED_BOOTSTRAPPER_URL,
    MAX_REVOCATION_FRESHNESS_SECONDS,
    OBSERVATION_SCHEMA_ID,
    SUPPLIER_CRITERION_COMPONENTS,
    SUPPLIER_CRITERION_ID,
    TIME_STAMPING_EKU,
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
FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
FILE_ATTRIBUTE_TAG_INFO_CLASS = 9
FILE_ID_INFO_CLASS = 18
DUPLICATE_SAME_ACCESS = 0x00000002
FILE_BEGIN = 0
FILE_CURRENT = 1
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
        self.kernel32.DuplicateHandle.argtypes = [HANDLE, HANDLE, HANDLE, ctypes.POINTER(HANDLE), DWORD, BOOL, DWORD]
        self.kernel32.DuplicateHandle.restype = BOOL
        self.kernel32.GetCurrentProcess.restype = HANDLE

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
    if not api.kernel32.GetFileSizeEx(native, ctypes.byref(size)) or size.value <= 0:
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


def _hash_handle(api: _Apis, handle: int) -> str:
    import msvcrt

    native = HANDLE(handle)
    position = ctypes.c_longlong()
    if not api.kernel32.SetFilePointerEx(native, 0, ctypes.byref(position), FILE_CURRENT):
        raise NativeVerificationError("file pointer query failed")
    duplicate = HANDLE()
    process = api.kernel32.GetCurrentProcess()
    if not api.kernel32.DuplicateHandle(process, native, process, ctypes.byref(duplicate), 0, False, DUPLICATE_SAME_ACCESS):
        raise NativeVerificationError("file handle duplication failed")
    try:
        if not api.kernel32.SetFilePointerEx(native, 0, None, FILE_BEGIN):
            raise NativeVerificationError("file rewind failed")
        fd = msvcrt.open_osfhandle(int(duplicate.value), os.O_RDONLY | os.O_BINARY)
        duplicate = HANDLE()
        digest = hashlib.sha256()
        with os.fdopen(fd, "rb", closefd=True) as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    finally:
        api.kernel32.SetFilePointerEx(native, position.value, None, FILE_BEGIN)
        if duplicate.value:
            api.kernel32.CloseHandle(duplicate)


def _store_snapshot(api: _Apis) -> str:
    entries: list[str] = []
    for store_name in ("ROOT", "CA", "Disallowed"):
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
                cert = api.crypt32.CertEnumCertificatesInStore(store, cert)
                if not cert:
                    break
                entries.append(f"{store_name}:CERT:{_cert_sha256(cert)}")
            ctl = PCCTL_CONTEXT()
            while True:
                ctl = api.crypt32.CertEnumCTLsInStore(store, ctl)
                if not ctl:
                    break
                if not ctl.contents.pbCtlEncoded or ctl.contents.cbCtlEncoded == 0:
                    raise NativeVerificationError("CTL encoding is absent")
                digest = hashlib.sha256(
                    ctypes.string_at(ctl.contents.pbCtlEncoded, ctl.contents.cbCtlEncoded)
                ).hexdigest()
                entries.append(f"{store_name}:CTL:{digest}")
        finally:
            api.crypt32.CertCloseStore(store, 0)
    return sha256_hex(canonical_json_lf(sorted(entries)))


def _provider_chain(signer: PCRYPT_PROVIDER_SGNR) -> list[str]:
    if not signer or signer.contents.csCertChain < 2 or not signer.contents.pasCertChain:
        raise NativeVerificationError("provider signer chain is absent")
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


def _chain_rows(chain: PCERT_CHAIN_CONTEXT, reference_time: int) -> list[dict[str, object]]:
    if not chain or chain.contents.cChain != 1 or not chain.contents.rgpChain:
        raise NativeVerificationError("chain context is not one simple chain")
    simple = chain.contents.rgpChain[0]
    if not simple or simple.contents.cElement < 2 or not simple.contents.rgpElement:
        raise NativeVerificationError("simple chain is incomplete")
    rows: list[dict[str, object]] = []
    count = int(simple.contents.cElement)
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
            freshness_reference = None
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
            freshness_reference = reference_time
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
                "freshness_reference_filetime": freshness_reference,
                "disallowed": bool(int(element.TrustStatus.dwErrorStatus) & CERT_TRUST_IS_EXPLICIT_DISTRUST),
            }
        )
    return rows


def _build_chain(
    api: _Apis,
    cert: PCERT_CONTEXT,
    verification_time: int,
    reference_time: int,
    eku: str,
) -> tuple[PCERT_CHAIN_CONTEXT, list[dict[str, object]], dict[str, object]]:
    usage_values = (ctypes.c_char_p * 1)(eku.encode("ascii"))
    usage = CTL_USAGE(1, usage_values)
    match = CERT_USAGE_MATCH(0, usage)
    empty = CERT_USAGE_MATCH(0, CTL_USAGE(0, None))
    cutoff = _int_filetime(reference_time - MAX_REVOCATION_FRESHNESS_SECONDS * 10_000_000)
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
    if not succeeded or not context:
        raise NativeVerificationError("certificate chain build failed")
    rows = _chain_rows(context, reference_time)
    output_sha256 = sha256_hex(canonical_json_lf(rows))
    call: dict[str, object] = {
        "api": "CertGetCertificateChain",
        "chain_engine": CHAIN_ENGINE,
        "flags": list(CHAIN_FLAGS),
        "url_retrieval_timeout_ms": URL_RETRIEVAL_TIMEOUT_MS,
        "leaf_certificate_der_sha256": _cert_sha256(cert),
        "verification_time_filetime": verification_time,
        "reference_time_filetime": reference_time,
        "requested_eku": eku,
        "additional_candidate_store_used": False,
        "api_return": True,
        "output_chain_sha256": output_sha256,
        "input_sha256": "",
    }
    call["input_sha256"] = chain_call_input_sha256(call)
    return context, rows, call


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
        "verification_time_filetime": verification_time,
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
    requested_uri: str,
    final_uri: str,
    redirect_count: int,
    process_count_before_decision: int = 0,
) -> bytes:
    """Collect one complete observation without executing the candidate file."""

    if os.name != "nt" or type(file_handle) is not int or file_handle <= 0:
        raise NativeVerificationError("one valid Windows file handle is required")
    path = Path(full_path)
    if not path.is_absolute() or requested_uri != FIXED_BOOTSTRAPPER_URL:
        raise NativeVerificationError("fixed path or URI precondition differs")
    if type(redirect_count) is not int or type(redirect_count) is bool or redirect_count < 0:
        raise NativeVerificationError("redirect count differs")
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
    reference_time = _now_filetime(api)
    download_identity = _file_identity(api, file_handle)
    download_hash = _hash_handle(api, file_handle)
    events = [_event(0, None)]
    trust_pre = _store_snapshot(api)
    events.append(_event(1, None))

    action = _guid(WINTRUST_ACTION_GUID)
    file_info = WINTRUST_FILE_INFO(ctypes.sizeof(WINTRUST_FILE_INFO), str(path), HANDLE(file_handle), None)
    data = WINTRUST_DATA()
    data.cbStruct = ctypes.sizeof(WINTRUST_DATA)
    data.dwUIChoice = WTD_UI_NONE
    data.fdwRevocationChecks = WTD_REVOKE_NONE
    data.dwUnionChoice = WTD_CHOICE_FILE
    data.pFile = ctypes.pointer(file_info)
    data.dwStateAction = WTD_STATEACTION_VERIFY
    data.dwProvFlags = WTD_DISABLE_MD2_MD4 | WTD_MOTW
    data.dwUIContext = WTD_UICONTEXT_INSTALL
    verify_return = int(api.wintrust.WinVerifyTrust(HANDLE(-1), ctypes.byref(action), ctypes.byref(data)))
    if not data.hWVTStateData:
        raise NativeVerificationError("WinVerifyTrust did not return provider state")
    state_id = sha256_hex(
        f"pid={os.getpid()}\nstate={int(data.hWVTStateData):016x}\n".encode("ascii")
    )
    events.append(_event(2, state_id))
    events.append(_event(3, state_id))
    close_return: int | None = None
    signer_chain_context = PCERT_CHAIN_CONTEXT()
    timestamp_chain_context = PCERT_CHAIN_CONTEXT()
    try:
        provider_data = api.wintrust.WTHelperProvDataFromStateData(data.hWVTStateData)
        if not provider_data:
            raise NativeVerificationError("provider data extraction failed")
        signer = api.wintrust.WTHelperGetProvSignerFromChain(provider_data, 0, False, 0)
        if not signer:
            raise NativeVerificationError("signer is absent")
        events.append(_event(4, state_id))
        countersigner = api.wintrust.WTHelperGetProvSignerFromChain(provider_data, 0, True, 0)
        if not countersigner:
            raise NativeVerificationError("mandatory countersigner is absent")
        if int(countersigner.contents.dwSignerType) != SGNR_TYPE_TIMESTAMP:
            raise NativeVerificationError("provider countersigner is not a timestamp signer")
        events.append(_event(5, state_id))
        signer_provider_chain = _provider_chain(signer)
        timestamp_provider_chain = _provider_chain(countersigner)
        signing_time = _filetime_int(countersigner.contents.sftVerifyAsOf)
        if signing_time <= 0:
            raise NativeVerificationError("timestamp signing time is absent")
        signer_cert = signer.contents.pasCertChain[0].pCert
        timestamp_cert = countersigner.contents.pasCertChain[0].pCert
        signer_chain_context, signer_rows, signer_call = _build_chain(
            api, signer_cert, signing_time, reference_time, CODE_SIGNING_EKU
        )
        events.append(_event(6, state_id))
        signer_auth = _policy(
            api, POLICY_AUTHENTICODE, "CERT_CHAIN_POLICY_AUTHENTICODE",
            signer_chain_context, signer_call["output_chain_sha256"], signing_time,
            {"pv_extra_policy_para": "NULL"},
        )
        signer_ms = _policy(
            api, POLICY_MICROSOFT_ROOT, "CERT_CHAIN_POLICY_MICROSOFT_ROOT",
            signer_chain_context, signer_call["output_chain_sha256"], signing_time,
            {"test_root_enabled": False},
        )
        events.append(_event(7, state_id))
        timestamp_chain_context, timestamp_rows, timestamp_call = _build_chain(
            api, timestamp_cert, signing_time, reference_time, TIME_STAMPING_EKU
        )
        events.append(_event(8, state_id))
        timestamp_auth = _policy(
            api, POLICY_AUTHENTICODE_TS, "CERT_CHAIN_POLICY_AUTHENTICODE_TS",
            timestamp_chain_context, timestamp_call["output_chain_sha256"], signing_time,
            {"pv_extra_policy_para": "NULL"},
        )
        events.append(_event(9, state_id))
        post_identity = _file_identity(api, file_handle)
        post_hash = _hash_handle(api, file_handle)
        trust_post = _store_snapshot(api)
        events.append(_event(10, state_id))
    finally:
        if signer_chain_context:
            api.crypt32.CertFreeCertificateChain(signer_chain_context)
        if timestamp_chain_context:
            api.crypt32.CertFreeCertificateChain(timestamp_chain_context)
        data.dwStateAction = WTD_STATEACTION_CLOSE
        close_return = int(api.wintrust.WinVerifyTrust(HANDLE(-1), ctypes.byref(action), ctypes.byref(data)))
        events.append(_event(11, state_id))

    preexecution_identity = _file_identity(api, file_handle)
    preexecution_hash = _hash_handle(api, file_handle)
    events.append(_event(12, None))
    if tuple(event["kind"] for event in events) != EVENT_SEQUENCE:
        raise NativeVerificationError("native event sequence differs")
    observation = {
        "schema_id": OBSERVATION_SCHEMA_ID,
        "native_collection_status": "COMPLETED-NONAUTHORITATIVE-OBSERVATION",
        "implementation_manifest_sha256": authority.implementation_manifest_sha256,
        "policy_manifest_sha256": authority.policy_manifest_sha256,
        "native_verifier_manifest_sha256": authority.native_verifier_manifest_sha256,
        "semantic_validator_manifest_sha256": authority.semantic_validator_manifest_sha256,
        "supplier": {
            "criterion_id": SUPPLIER_CRITERION_ID,
            "components": list(SUPPLIER_CRITERION_COMPONENTS),
            "official_leaf_guarantee_claimed": False,
            "project_reauthorization_acknowledged": True,
        },
        "requested_uri": requested_uri,
        "final_uri": final_uri,
        "redirect_count": redirect_count,
        "original_file_handle_retained": True,
        "file_identities": {
            "download_close": download_identity,
            "post_signature": post_identity,
            "preexecution": preexecution_identity,
        },
        "byte_sha256": {
            "download_close": download_hash,
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
            "signing_time_filetime": signing_time,
            "leaf_certificate_der_sha256": timestamp_provider_chain[0],
            "provider_chain": timestamp_provider_chain,
            "rebuilt_chain": timestamp_rows,
            "chain_call": timestamp_call,
            "timestamp_policy": timestamp_auth,
        },
        "trust_authority": {
            "pre_snapshot_sha256": trust_pre,
            "post_snapshot_sha256": trust_post,
            "snapshot_scope": list(_TRUST_SCOPE),
            "store_mutation_count": 0 if trust_pre == trust_post else 1,
        },
        "process_count_before_decision": process_count_before_decision,
    }
    return canonical_json_lf(observation)


_TRUST_SCOPE = (
    "LOCAL-MACHINE-ROOT",
    "LOCAL-MACHINE-CA",
    "LOCAL-MACHINE-DISALLOWED",
    "EFFECTIVE-WINDOWS-DISALLOWED-CTL",
)
