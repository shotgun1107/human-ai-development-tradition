"""F-04 enumeration API doubles only: no backend construction or DLL call."""

from __future__ import annotations

import ctypes
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest import mock

from s0_public_assembly_verifier import win32
from s0_public_assembly_verifier.errors import AssemblyFailure


CANDIDATE = Path(__file__).resolve().parents[1]
BASELINE = CANDIDATE.parents[2] / "s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation"
OBSERVATIONS = []


class StreamApiDouble:
    """Deterministic Win32 call sequence with controllable last-error clobber."""

    def __init__(self, names=("::$DATA",), terminal=38, first_error=None,
                 close_ok=True, close_error=0):
        self.names = list(names)
        self.terminal = terminal
        self.first_error = first_error
        self.close_ok = close_ok
        self.close_error = close_error
        self.index = 0
        self.handle = 1234
        self.calls = []

    def FindFirstStreamW(self, path, level, pointer, flags):
        self.calls.append("first")
        if self.first_error is not None:
            ctypes.set_last_error(self.first_error)
            return win32._INVALID_HANDLE_VALUE
        pointer._obj.cStreamName = self.names[0]
        return self.handle

    def FindNextStreamW(self, handle, pointer):
        assert handle == self.handle
        self.index += 1
        if self.index < len(self.names):
            self.calls.append("next:entry")
            pointer._obj.cStreamName = self.names[self.index]
            return True
        self.calls.append("next:error:" + str(self.terminal))
        ctypes.set_last_error(self.terminal)
        return False

    def FindClose(self, handle):
        assert handle == self.handle
        self.calls.append("close:" + str(self.close_ok))
        ctypes.set_last_error(self.close_error)
        return self.close_ok


class StreamInventoryTests(unittest.TestCase):
    def inspect(self, api, *, preflight=False, module=win32):
        # Never run Win32PublicationBackend.__init__, which loads native APIs.
        backend = object.__new__(module.Win32PublicationBackend)
        object.__setattr__(backend, "_kernel32", api)
        outcome = {"preflight": preflight, "module": module.__name__,
                   "input": {"names": api.names, "terminal": api.terminal,
                             "first_error": api.first_error, "close_ok": api.close_ok,
                             "close_error": api.close_error}}
        with mock.patch.object(ctypes, "WinDLL", side_effect=AssertionError("native DLL construction forbidden")):
            try:
                backend._require_no_alternate_streams(CANDIDATE / "verification/tmp/no-native-object",
                                                     preflight=preflight)
            except AssemblyFailure as exc:
                outcome.update(status="rejected", failure_class=exc.failure_class,
                               observed_transport_calls=exc.observed_transport_calls,
                               diagnostic=exc.diagnostic)
                if isinstance(exc.__context__, AssemblyFailure):
                    outcome["primary_context"] = str(exc.__context__)
            else:
                outcome["status"] = "accepted"
        outcome["calls"] = api.calls[:]
        OBSERVATIONS.append(outcome)
        return outcome

    def assert_failure(self, outcome, preflight, diagnostic):
        self.assertEqual(outcome["status"], "rejected")
        self.assertEqual(outcome["failure_class"], "AR-AUTH" if preflight else "AR-RECORD")
        self.assertEqual(outcome["observed_transport_calls"], 0 if preflight else 1)
        self.assertIn(diagnostic, outcome["diagnostic"])

    def test_first_eof_accepts_without_close(self):
        for preflight in (False, True):
            with self.subTest(preflight=preflight):
                outcome = self.inspect(StreamApiDouble(first_error=38), preflight=preflight)
                self.assertEqual(outcome["status"], "accepted")
                self.assertEqual(outcome["calls"], ["first"])

    def test_first_non_eof_rejects_without_close(self):
        for preflight in (False, True):
            for error in (0, 2, 5, 87):
                with self.subTest(preflight=preflight, error=error):
                    outcome = self.inspect(StreamApiDouble(first_error=error), preflight=preflight)
                    self.assert_failure(outcome, preflight, "could not be authenticated")
                    self.assertEqual(outcome["calls"], ["first"])

    def test_normal_eof_accepts_and_closes_exactly_once(self):
        for preflight in (False, True):
            with self.subTest(preflight=preflight):
                outcome = self.inspect(StreamApiDouble(), preflight=preflight)
                self.assertEqual(outcome["status"], "accepted")
                self.assertEqual(outcome["calls"], ["first", "next:error:38", "close:True"])

    def test_next_non_eof_rejects_and_closes_exactly_once(self):
        for preflight in (False, True):
            for error in (0, 5, 87):
                with self.subTest(preflight=preflight, error=error):
                    outcome = self.inspect(StreamApiDouble(terminal=error), preflight=preflight)
                    self.assert_failure(outcome, preflight, "could not be authenticated")
                    self.assertEqual(outcome["calls"], ["first", "next:error:" + str(error), "close:True"])

    def test_last_error_captured_before_close_clobber(self):
        for terminal, close_error, expected in ((5, 38, "rejected"), (38, 5, "accepted")):
            for preflight in (False, True):
                with self.subTest(terminal=terminal, close_error=close_error, preflight=preflight):
                    outcome = self.inspect(StreamApiDouble(terminal=terminal, close_error=close_error),
                                           preflight=preflight)
                    self.assertEqual(outcome["status"], expected)
                    if expected == "rejected":
                        self.assert_failure(outcome, preflight, "could not be authenticated")

    def test_alternate_and_multiple_entries_reject(self):
        for names in ((":extra:$DATA",), ("::$DATA", ":extra:$DATA"), ("::$DATA", "::$DATA"),
                      ("::$DATA", ":one:$DATA", ":two:$DATA")):
            for preflight in (False, True):
                with self.subTest(names=names, preflight=preflight):
                    outcome = self.inspect(StreamApiDouble(names=names), preflight=preflight)
                    self.assert_failure(outcome, preflight, "alternate data stream")
                    self.assertEqual(outcome["calls"].count("close:True"), 1)
                    self.assertEqual(outcome["calls"].count("next:entry"), len(names) - 1)

    def test_close_failure_after_normal_eof_rejects(self):
        for preflight in (False, True):
            with self.subTest(preflight=preflight):
                outcome = self.inspect(StreamApiDouble(close_ok=False, close_error=6), preflight=preflight)
                self.assert_failure(outcome, preflight, "could not be closed")
                self.assertEqual(outcome["calls"], ["first", "next:error:38", "close:False"])

    def test_enumeration_and_close_failure_preserve_rejection_and_context(self):
        for preflight in (False, True):
            with self.subTest(preflight=preflight):
                outcome = self.inspect(StreamApiDouble(terminal=5, close_ok=False, close_error=6),
                                       preflight=preflight)
                self.assert_failure(outcome, preflight, "could not be closed")
                self.assertIn("could not be authenticated", outcome["primary_context"])
                self.assertEqual(outcome["calls"], ["first", "next:error:5", "close:False"])

    def test_baseline_discriminates_unchecked_next_and_close(self):
        path = BASELINE / "s0_public_assembly_verifier/win32.py"
        name = "s0_public_assembly_verifier._baseline_win32"
        spec = importlib.util.spec_from_file_location(name, path)
        baseline = importlib.util.module_from_spec(spec)
        sys.modules[name] = baseline
        spec.loader.exec_module(baseline)
        self.assertEqual(Path(baseline.__file__).resolve(), path.resolve())
        for api in (StreamApiDouble(terminal=5), StreamApiDouble(close_ok=False, close_error=6)):
            with self.subTest(terminal=api.terminal, close_ok=api.close_ok):
                self.assertEqual(self.inspect(api, module=baseline)["status"], "accepted")
