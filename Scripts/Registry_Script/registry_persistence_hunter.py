#!/usr/bin/env python3
"""
registry_persistence_hunter.py (with Time Range filtering)

Adds:
- --start "YYYY-MM-DD" or ISO datetime (e.g., "2025-12-01T00:00:00Z")
- --end   "YYYY-MM-DD" or ISO datetime (e.g., "2025-12-23T23:59:59Z")
- Filters results by the **registry key LastWrite time** (best available timestamp in offline registry).

Notes:
- Registry artifacts primarily expose **Key LastWrite** timestamps (not per-value write times).
- If a result has no timestamp (rare), it will be excluded when time filtering is enabled,
  unless you set --include_undated.

Dependencies:
- regipy (recommended): pip install regipy
  OR
- python-registry: pip install python-registry
"""

import argparse
import csv
import json
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------
# Persistence locations
# ---------------------------
PERSISTENCE_QUERIES = [
    # Run keys
    ("Run", "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", "values"),
    ("RunOnce", "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce", "values"),
    ("Run", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "values"),
    ("RunOnce", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce", "values"),

    # Winlogon
    ("Winlogon", "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon", "named_values:Shell,Userinit,Notify"),

    # Services / Drivers
    ("Services", "HKLM\\SYSTEM\\CurrentControlSet\\Services", "subkeys_services"),

    # Scheduled Tasks cache
    ("ScheduledTasks", "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tree", "subkeys"),
    ("ScheduledTasks", "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tasks", "subkeys"),

    # AppInit DLLs
    ("AppInit", "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Windows", "named_values:AppInit_DLLs,LoadAppInit_DLLs"),

    # IFEO Debugger
    ("IFEO", "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options", "subkeys_debugger"),

    # Active Setup
    ("ActiveSetup", "HKLM\\SOFTWARE\\Microsoft\\Active Setup\\Installed Components", "subkeys_stubpath"),

    # Startup folder redirection
    ("ShellFolders", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders", "values"),
    ("UserShellFolders", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders", "values"),

    # COM Hijacking (common)
    ("COM_Hijack", "HKCU\\Software\\Classes\\CLSID", "subkeys_inprocserver32"),
    ("COM_Hijack", "HKLM\\SOFTWARE\\Classes\\CLSID", "subkeys_inprocserver32"),

    # LSA packages
    ("LSA", "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Lsa", "named_values:Authentication Packages,Security Packages"),

    # BootExecute
    ("BootExecute", "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager", "named_values:BootExecute"),

    # File association hijack (high signal examples)
    ("FileAssoc", "HKCU\\Software\\Classes\\exefile\\shell\\open\\command", "default"),
    ("FileAssoc", "HKLM\\SOFTWARE\\Classes\\exefile\\shell\\open\\command", "default"),
]

SUSPICIOUS_LAUNCHERS = re.compile(
    r"\b(powershell|pwsh|cmd|wscript|cscript|mshta|rundll32|regsvr32|wmic|schtasks)\b",
    re.IGNORECASE
)
SUSPICIOUS_PATHS = re.compile(
    r"\\(AppData\\Local\\Temp|AppData\\Roaming|ProgramData|Temp)\\",
    re.IGNORECASE
)

# ---------------------------
# Time parsing + filtering
# ---------------------------

def _parse_dt(s: str) -> datetime:
    """
    Accepts:
      - YYYY-MM-DD  (assumes 00:00:00Z)
      - ISO8601 datetime:
          2025-12-01T12:34:56Z
          2025-12-01T12:34:56+02:00
          2025-12-01T12:34:56
    Returns timezone-aware datetime (UTC if missing tzinfo).
    """
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        dt = datetime.fromisoformat(s)
        return dt.replace(tzinfo=timezone.utc)

    # Normalize trailing Z
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"

    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

def parse_time_range(start: Optional[str], end: Optional[str]) -> Tuple[Optional[datetime], Optional[datetime]]:
    start_dt = _parse_dt(start) if start else None
    end_dt = _parse_dt(end) if end else None
    if start_dt and end_dt and end_dt < start_dt:
        raise ValueError("--end must be >= --start")
    return start_dt, end_dt

def iso_to_dt(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    try:
        # handle "Z"
        t = s
        if t.endswith("Z"):
            t = t[:-1] + "+00:00"
        dt = datetime.fromisoformat(t)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None

def in_range(ts_iso: Optional[str], start: Optional[datetime], end: Optional[datetime]) -> bool:
    """
    Inclusive range: start <= ts <= end
    If start/end is None, that side is unbounded.
    """
    if start is None and end is None:
        return True
    dt = iso_to_dt(ts_iso)
    if dt is None:
        return False
    if start and dt < start:
        return False
    if end and dt > end:
        return False
    return True

# ---------------------------
# Registry backend abstraction
# ---------------------------

class RegistryBackend:
    def open_hive(self, hive_path: str) -> Any:
        raise NotImplementedError

    def get_key(self, hive_obj: Any, key_path: str) -> Optional[Any]:
        raise NotImplementedError

    def key_lastwrite(self, key_obj: Any) -> Optional[str]:
        raise NotImplementedError

    def enum_values(self, key_obj: Any) -> List[Tuple[str, Any]]:
        raise NotImplementedError

    def get_value(self, key_obj: Any, value_name: str) -> Optional[Any]:
        raise NotImplementedError

    def enum_subkeys(self, key_obj: Any) -> List[Any]:
        raise NotImplementedError

    def subkey_name(self, key_obj: Any) -> str:
        raise NotImplementedError


def detect_backend() -> RegistryBackend:
    try:
        from regipy.registry import RegistryHive  # type: ignore
        class RegipyBackend(RegistryBackend):
            def open_hive(self, hive_path: str) -> Any:
                return RegistryHive(hive_path)

            def get_key(self, hive_obj: Any, key_path: str) -> Optional[Any]:
                try:
                    return hive_obj.get_key(key_path)
                except Exception:
                    return None

            def key_lastwrite(self, key_obj: Any) -> Optional[str]:
                try:
                    dt = key_obj.header.last_modified
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    return dt.isoformat()
                except Exception:
                    return None

            def enum_values(self, key_obj: Any) -> List[Tuple[str, Any]]:
                out = []
                try:
                    for v in key_obj.values:
                        out.append((v.name if v.name else "(Default)", v.value))
                except Exception:
                    pass
                return out

            def get_value(self, key_obj: Any, value_name: str) -> Optional[Any]:
                try:
                    for v in key_obj.values:
                        n = v.name if v.name else "(Default)"
                        if n == value_name or (value_name in ("(Default)", "") and n == "(Default)"):
                            return v.value
                except Exception:
                    return None
                return None

            def enum_subkeys(self, key_obj: Any) -> List[Any]:
                try:
                    return list(key_obj.iter_subkeys(as_json=False))
                except Exception:
                    return []

            def subkey_name(self, key_obj: Any) -> str:
                try:
                    return key_obj.name
                except Exception:
                    return ""
        return RegipyBackend()
    except Exception:
        pass

    try:
        from Registry import Registry  # type: ignore
        class PythonRegistryBackend(RegistryBackend):
            def open_hive(self, hive_path: str) -> Any:
                return Registry.Registry(hive_path)

            def get_key(self, hive_obj: Any, key_path: str) -> Optional[Any]:
                try:
                    return hive_obj.open(key_path)
                except Exception:
                    return None

            def key_lastwrite(self, key_obj: Any) -> Optional[str]:
                try:
                    dt = key_obj.timestamp()
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    return dt.isoformat()
                except Exception:
                    return None

            def enum_values(self, key_obj: Any) -> List[Tuple[str, Any]]:
                out = []
                try:
                    for v in key_obj.values():
                        name = v.name() if v.name() else "(Default)"
                        try:
                            data = v.value()
                        except Exception:
                            data = repr(v.value())
                        out.append((name, data))
                except Exception:
                    pass
                return out

            def get_value(self, key_obj: Any, value_name: str) -> Optional[Any]:
                try:
                    for v in key_obj.values():
                        name = v.name() if v.name() else "(Default)"
                        if name == value_name or (value_name in ("(Default)", "") and name == "(Default)"):
                            try:
                                return v.value()
                            except Exception:
                                return repr(v.value())
                except Exception:
                    return None
                return None

            def enum_subkeys(self, key_obj: Any) -> List[Any]:
                try:
                    return key_obj.subkeys()
                except Exception:
                    return []

            def subkey_name(self, key_obj: Any) -> str:
                try:
                    return key_obj.name()
                except Exception:
                    return ""
        return PythonRegistryBackend()
    except Exception as e:
        raise RuntimeError(
            "No supported registry library found. Install one:\n"
            "  pip install regipy\n"
            "or\n"
            "  pip install python-registry\n"
        ) from e


# ---------------------------
# Hive mapping
# ---------------------------

def translate_rooted_path(rooted: str) -> Tuple[str, str]:
    p = rooted.strip("\\")
    parts = p.split("\\", 1)
    root = parts[0].upper()
    rest = parts[1] if len(parts) > 1 else ""

    if root == "HKLM":
        top = rest.split("\\", 1)[0].upper() if rest else ""
        if top == "SOFTWARE":
            return ("HKLM_SOFTWARE", rest[len("SOFTWARE\\"):] if rest.startswith("SOFTWARE\\") else "")
        if top == "SYSTEM":
            return ("HKLM_SYSTEM", rest[len("SYSTEM\\"):] if rest.startswith("SYSTEM\\") else "")
        if top == "SAM":
            return ("HKLM_SAM", rest[len("SAM\\"):] if rest.startswith("SAM\\") else "")
        if top == "SECURITY":
            return ("HKLM_SECURITY", rest[len("SECURITY\\"):] if rest.startswith("SECURITY\\") else "")
        return ("HKLM_SOFTWARE", rest)
    elif root == "HKCU":
        if rest.lower().startswith("software\\classes") or rest.lower().startswith("software\\classes\\"):
            tail = rest[len("Software\\Classes\\"):] if rest.lower().startswith("software\\classes\\") else ""
            return ("HKCU_USRCLASS", tail)
        return ("HKCU_NTUSER", rest)
    else:
        return ("UNKNOWN", rest)


# ---------------------------
# Detection heuristics
# ---------------------------

def score_suspicion(value_data: Any) -> List[str]:
    reasons = []
    if value_data is None:
        return reasons

    s = str(value_data)

    if SUSPICIOUS_LAUNCHERS.search(s):
        reasons.append("uses_LOLBin_launcher")
    if SUSPICIOUS_PATHS.search(s):
        reasons.append("exec_from_user_writable_path")
    if any(x in s.lower() for x in ["base64", "frombase64string", "iex", "downloadstring", "invoke-webrequest"]):
        reasons.append("powershell_obfuscation_or_download")
    if s.strip().startswith(("http://", "https://")):
        reasons.append("exec_or_ref_remote_url")
    if s.lower().endswith((".vbs", ".js", ".jse", ".wsf", ".ps1", ".hta")):
        reasons.append("script_based_persistence")
    return reasons


# ---------------------------
# Scanning logic (time-aware)
# ---------------------------

SCAN_RESULTS: List[Dict[str, Any]] = []

def add_result_time_filtered(
    *,
    category: str,
    hive: str,
    key: str,
    value_name: str,
    value_data: Any,
    key_lastwrite: Optional[str],
    suspicion: List[str],
    start_dt: Optional[datetime],
    end_dt: Optional[datetime],
    include_undated: bool
):
    if (start_dt or end_dt):
        if key_lastwrite is None:
            if not include_undated:
                return
        else:
            if not in_range(key_lastwrite, start_dt, end_dt):
                return

    SCAN_RESULTS.append({
        "category": category,
        "hive": hive,
        "key": key,
        "value_name": value_name,
        "value_data": value_data,
        "key_lastwrite": key_lastwrite,
        "suspicion": suspicion,
    })

def scan_key_values(backend: RegistryBackend, hive_obj: Any, hive_label: str, key_path: str, category: str,
                    start_dt: Optional[datetime], end_dt: Optional[datetime], include_undated: bool):
    key = backend.get_key(hive_obj, key_path)
    if not key:
        return
    lw = backend.key_lastwrite(key)
    for name, data in backend.enum_values(key):
        add_result_time_filtered(
            category=category, hive=hive_label, key=key_path,
            value_name=name, value_data=data, key_lastwrite=lw,
            suspicion=score_suspicion(data),
            start_dt=start_dt, end_dt=end_dt, include_undated=include_undated
        )

def scan_named_values(backend: RegistryBackend, hive_obj: Any, hive_label: str, key_path: str, category: str, names: List[str],
                      start_dt: Optional[datetime], end_dt: Optional[datetime], include_undated: bool):
    key = backend.get_key(hive_obj, key_path)
    if not key:
        return
    lw = backend.key_lastwrite(key)
    for n in names:
        data = backend.get_value(key, n)
        if data is None:
            continue
        add_result_time_filtered(
            category=category, hive=hive_label, key=key_path,
            value_name=n, value_data=data, key_lastwrite=lw,
            suspicion=score_suspicion(data),
            start_dt=start_dt, end_dt=end_dt, include_undated=include_undated
        )

def scan_default_value(backend: RegistryBackend, hive_obj: Any, hive_label: str, key_path: str, category: str,
                       start_dt: Optional[datetime], end_dt: Optional[datetime], include_undated: bool):
    key = backend.get_key(hive_obj, key_path)
    if not key:
        return
    lw = backend.key_lastwrite(key)
    data = backend.get_value(key, "(Default)") or backend.get_value(key, "")
    if data is None:
        return
    add_result_time_filtered(
        category=category, hive=hive_label, key=key_path,
        value_name="(Default)", value_data=data, key_lastwrite=lw,
        suspicion=score_suspicion(data),
        start_dt=start_dt, end_dt=end_dt, include_undated=include_undated
    )

def scan_subkeys_presence(backend: RegistryBackend, hive_obj: Any, hive_label: str, key_path: str, category: str,
                          start_dt: Optional[datetime], end_dt: Optional[datetime], include_undated: bool):
    key = backend.get_key(hive_obj, key_path)
    if not key:
        return
    for sk in backend.enum_subkeys(key):
        sk_name = backend.subkey_name(sk)
        lw = backend.key_lastwrite(sk)
        add_result_time_filtered(
            category=category, hive=hive_label, key=f"{key_path}\\{sk_name}",
            value_name="(subkey)", value_data="(present)",
            key_lastwrite=lw, suspicion=[],
            start_dt=start_dt, end_dt=end_dt, include_undated=include_undated
        )

def scan_subkeys_services(backend: RegistryBackend, hive_obj: Any, hive_label: str, services_root: str, category: str,
                          start_dt: Optional[datetime], end_dt: Optional[datetime], include_undated: bool):
    root = backend.get_key(hive_obj, services_root)
    if not root:
        return
    for sk in backend.enum_subkeys(root):
        name = backend.subkey_name(sk)
        lw = backend.key_lastwrite(sk)
        img = backend.get_value(sk, "ImagePath")
        start = backend.get_value(sk, "Start")
        typ = backend.get_value(sk, "Type")
        if img is None and start is None and typ is None:
            continue

        reasons = score_suspicion(img)
        if isinstance(start, int) and start in (0, 2):
            reasons.append(f"service_start={start}_boot_or_auto")
        if isinstance(typ, int) and typ == 1:
            reasons.append("kernel_driver_type=1")

        add_result_time_filtered(
            category=category, hive=hive_label, key=f"{services_root}\\{name}",
            value_name="ImagePath/Start/Type",
            value_data={"ImagePath": img, "Start": start, "Type": typ},
            key_lastwrite=lw, suspicion=reasons,
            start_dt=start_dt, end_dt=end_dt, include_undated=include_undated
        )

def scan_ifeo_debugger(backend: RegistryBackend, hive_obj: Any, hive_label: str, ifeo_root: str, category: str,
                       start_dt: Optional[datetime], end_dt: Optional[datetime], include_undated: bool):
    root = backend.get_key(hive_obj, ifeo_root)
    if not root:
        return
    for sk in backend.enum_subkeys(root):
        exe = backend.subkey_name(sk)
        dbg = backend.get_value(sk, "Debugger")
        if dbg is None:
            continue
        lw = backend.key_lastwrite(sk)
        reasons = score_suspicion(dbg) + ["ifeo_debugger_set"]
        add_result_time_filtered(
            category=category, hive=hive_label, key=f"{ifeo_root}\\{exe}",
            value_name="Debugger", value_data=dbg, key_lastwrite=lw, suspicion=reasons,
            start_dt=start_dt, end_dt=end_dt, include_undated=include_undated
        )

def scan_activesetup_stubpath(backend: RegistryBackend, hive_obj: Any, hive_label: str, as_root: str, category: str,
                              start_dt: Optional[datetime], end_dt: Optional[datetime], include_undated: bool):
    root = backend.get_key(hive_obj, as_root)
    if not root:
        return
    for sk in backend.enum_subkeys(root):
        comp = backend.subkey_name(sk)
        stub = backend.get_value(sk, "StubPath")
        if stub is None:
            continue
        lw = backend.key_lastwrite(sk)
        reasons = score_suspicion(stub) + ["active_setup_stubpath"]
        add_result_time_filtered(
            category=category, hive=hive_label, key=f"{as_root}\\{comp}",
            value_name="StubPath", value_data=stub, key_lastwrite=lw, suspicion=reasons,
            start_dt=start_dt, end_dt=end_dt, include_undated=include_undated
        )

def scan_com_inprocserver32(backend: RegistryBackend, hive_obj: Any, hive_label: str, clsid_root: str, category: str,
                            start_dt: Optional[datetime], end_dt: Optional[datetime], include_undated: bool):
    root = backend.get_key(hive_obj, clsid_root)
    if not root:
        return
    for clsid_key in backend.enum_subkeys(root):
        clsid = backend.subkey_name(clsid_key)
        inproc = backend.get_key(hive_obj, f"{clsid_root}\\{clsid}\\InprocServer32")
        if not inproc:
            continue
        dflt = backend.get_value(inproc, "(Default)") or backend.get_value(inproc, "")
        if dflt is None:
            continue
        lw = backend.key_lastwrite(inproc)
        reasons = score_suspicion(dflt)
        if reasons:
            reasons.append("com_inprocserver32_hijack_candidate")
        add_result_time_filtered(
            category=category, hive=hive_label, key=f"{clsid_root}\\{clsid}\\InprocServer32",
            value_name="(Default)", value_data=dflt, key_lastwrite=lw, suspicion=reasons,
            start_dt=start_dt, end_dt=end_dt, include_undated=include_undated
        )

def scan_all(hives: Dict[str, str], backend: RegistryBackend,
             start_dt: Optional[datetime], end_dt: Optional[datetime], include_undated: bool):
    opened: Dict[str, Any] = {}
    for label, path in hives.items():
        if path and os.path.exists(path):
            opened[label] = backend.open_hive(path)

    for category, rooted_path, mode in PERSISTENCE_QUERIES:
        logical, subpath = translate_rooted_path(rooted_path)
        if logical not in opened:
            continue

        hive_obj = opened[logical]
        hive_label = logical
        key_path = subpath

        if mode == "values":
            scan_key_values(backend, hive_obj, hive_label, key_path, category, start_dt, end_dt, include_undated)
        elif mode.startswith("named_values:"):
            names = [x.strip() for x in mode.split(":", 1)[1].split(",")]
            scan_named_values(backend, hive_obj, hive_label, key_path, category, names, start_dt, end_dt, include_undated)
        elif mode == "subkeys":
            scan_subkeys_presence(backend, hive_obj, hive_label, key_path, category, start_dt, end_dt, include_undated)
        elif mode == "subkeys_debugger":
            scan_ifeo_debugger(backend, hive_obj, hive_label, key_path, category, start_dt, end_dt, include_undated)
        elif mode == "subkeys_stubpath":
            scan_activesetup_stubpath(backend, hive_obj, hive_label, key_path, category, start_dt, end_dt, include_undated)
        elif mode == "subkeys_inprocserver32":
            scan_com_inprocserver32(backend, hive_obj, hive_label, key_path, category, start_dt, end_dt, include_undated)
        elif mode == "subkeys_services":
            scan_subkeys_services(backend, hive_obj, hive_label, key_path, category, start_dt, end_dt, include_undated)
        elif mode == "default":
            scan_default_value(backend, hive_obj, hive_label, key_path, category, start_dt, end_dt, include_undated)


def write_json(out_path: str, results: List[Dict[str, Any]]):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)

def write_csv(out_path: str, results: List[Dict[str, Any]]):
    fields = ["category", "hive", "key", "value_name", "value_data", "key_lastwrite", "suspicion"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in results:
            row = dict(r)
            row["suspicion"] = ",".join(row.get("suspicion") or [])
            row["value_data"] = json.dumps(row.get("value_data"), ensure_ascii=False, default=str)
            w.writerow({k: row.get(k, "") for k in fields})




def main():
    ap = argparse.ArgumentParser(description="Offline Registry Persistence Hunter (Time Range Aware)")
    ap.add_argument("--system", help="Path to SYSTEM hive")
    ap.add_argument("--software", help="Path to SOFTWARE hive")
    ap.add_argument("--sam", help="Path to SAM hive (optional)")
    ap.add_argument("--security", help="Path to SECURITY hive (optional)")
    ap.add_argument("--ntuser", help="Path to NTUSER.DAT (optional)")
    ap.add_argument("--usrclass", help="Path to USRCLASS.DAT (optional)")

    ap.add_argument("--start", help='Start time (inclusive). Example: "2025-12-01" or "2025-12-01T00:00:00Z"')
    ap.add_argument("--end", help='End time (inclusive). Example: "2025-12-23" or "2025-12-23T23:59:59Z"')
    ap.add_argument("--include_undated", action="store_true",
                    help="Include entries without a key_lastwrite timestamp even when --start/--end filtering is enabled")

    ap.add_argument("--out", help="Output JSON path", default="persistence_results.json")
    ap.add_argument("--csv", help="Optional output CSV path")
    ap.add_argument("--only_suspicious", action="store_true", help="Only emit entries with suspicion reasons")
    args = ap.parse_args()

    backend = detect_backend()

    start_dt, end_dt = parse_time_range(args.start, args.end)

    hives = {
        "HKLM_SYSTEM": args.system or "",
        "HKLM_SOFTWARE": args.software or "",
        "HKLM_SAM": args.sam or "",
        "HKLM_SECURITY": args.security or "",
        "HKCU_NTUSER": args.ntuser or "",
        "HKCU_USRCLASS": args.usrclass or "",
    }

    # Require at least SYSTEM or SOFTWARE
    if not (hives["HKLM_SYSTEM"] and os.path.exists(hives["HKLM_SYSTEM"])) and not (
        hives["HKLM_SOFTWARE"] and os.path.exists(hives["HKLM_SOFTWARE"])
    ):
        raise SystemExit("Provide at least --system and/or --software hive path(s).")

    scan_all(hives, backend, start_dt, end_dt, args.include_undated)

    results = SCAN_RESULTS
    if args.only_suspicious:
        results = [r for r in results if r.get("suspicion")]

    write_json(args.out, results)
    if args.csv:
        write_csv(args.csv, results)

    print(f"[+] Results: {len(results)}")
    if start_dt or end_dt:
        print(f"[+] Time filter: start={start_dt.isoformat() if start_dt else 'None'}  end={end_dt.isoformat() if end_dt else 'None'}")
        if args.include_undated:
            print("[+] Including undated entries.")
    print(f"[+] JSON written to: {args.out}")
    if args.csv:
        print(f"[+] CSV written to: {args.csv}")

if __name__ == "__main__":
    main()
