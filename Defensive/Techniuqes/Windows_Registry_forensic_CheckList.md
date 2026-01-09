# Malware Persistence – Registry Checklist

## Purpose
This checklist is designed to identify **registry-based persistence mechanisms** used by malware to:
- Execute at boot or logon
- Maintain access after reboot
- Hijack legitimate Windows components
- Evade detection via obscure registry locations

Use this during:
- Incident response
- Malware analysis
- Threat hunting
- Post-compromise forensics

---

## 1. Run & RunOnce Keys (Classic Persistence)

### User-Level

HKCU\Software\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce


### System-Level

HKLM\Software\Microsoft\Windows\CurrentVersion\Run
HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce


### What to Look For
- Unsigned executables
- Scripts (`.ps1`, `.vbs`, `.js`)
- LOLBins (powershell.exe, rundll32.exe, mshta.exe)
- Suspicious paths (Temp, AppData, ProgramData)

---

## 2. Winlogon Persistence (High-Impact)

HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon

### Critical Values
Shell
Userinit
Notify


### Indicators
- Additional executables appended to `explorer.exe`
- Non-standard DLLs in `Notify`
- Paths outside `System32`

---

## 3. Services & Drivers (Boot Persistence)

HKLM\SYSTEM\CurrentControlSet\Services


### Indicators
- Unknown service names
- `Start` = 0 (Boot) or 2 (Auto)
- `ImagePath` pointing to user-writable directories
- Kernel drivers (`Type = 1`) not signed

---

## 4. Scheduled Task Registry Artifacts



HKLM\Software\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree


### Indicators
- Tasks executing scripts or LOLBins
- Obfuscated task names
- Tasks triggered at logon/startup

---

## 5. Startup Folder via Registry Redirection



HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders
HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders


### Indicators
- Startup folder redirected to attacker-controlled location

---

## 6. AppInit DLLs (Legacy but Still Abused)



HKLM\Software\Microsoft\Windows NT\CurrentVersion\Windows


### Values


AppInit_DLLs
LoadAppInit_DLLs


### Indicators
- DLLs loaded into every GUI process
- Persistence + injection combo

---

## 7. Image File Execution Options (IFEO)



HKLM\Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options


### Indicators
- `Debugger` value set
- Hijacking legitimate executables (e.g., `cmd.exe`, `taskmgr.exe`)

---

## 8. COM Hijacking (Stealth Persistence)

### User-Level


HKCU\Software\Classes\CLSID


### System-Level


HKLM\Software\Classes\CLSID


### Indicators
- InProcServer32 pointing to suspicious DLLs
- CLSIDs tied to auto-elevated COM objects

---

## 9. Explorer Shell Extensions



HKLM\Software\Microsoft\Windows\CurrentVersion\Shell Extensions
HKCU\Software\Microsoft\Windows\CurrentVersion\Shell Extensions


### Indicators
- DLLs loading on Explorer start
- Unrecognized CLSIDs

---

## 10. Active Setup (User Profile Re-Execution)



HKLM\Software\Microsoft\Active Setup\Installed Components


### Indicators
- Malware re-executes for every new user
- `StubPath` launching executables or scripts

---

## 11. Logon Scripts



HKCU\Environment
HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System


### Indicators
- Custom logon scripts
- Powershell or batch files

---

## 12. Policies Abuse (Defense Evasion + Persistence)



HKCU\Software\Microsoft\Windows\CurrentVersion\Policies
HKLM\Software\Microsoft\Windows\CurrentVersion\Policies


### Indicators
- Disabled security tools
- Forced execution via policy settings

---

## 13. LSA & Authentication Packages (Advanced)



HKLM\SYSTEM\CurrentControlSet\Control\Lsa


### Values


Authentication Packages
Security Packages


### Indicators
- Custom DLLs loaded at authentication time
- Credential harvesting malware

---

## 14. Boot Execution (Rare but Severe)



HKLM\SYSTEM\CurrentControlSet\Control\Session Manager


### Values


BootExecute


### Indicators
- Additional executables beyond `autocheck autochk *`

---

## 15. File Association Hijacking



HKCU\Software\Classes
HKLM\Software\Classes


### Indicators
- Executables tied to file open actions
- Hijacked `.exe`, `.bat`, `.ps1` handlers

---

## 16. WMI Persistence Registry Artifacts



HKLM\Software\Microsoft\WBEM


### Indicators
- WMI event consumers linked to scripts/executables

---

## 17. Common Malware Red Flags

- Executables in:
  - `%AppData%`
  - `%LocalAppData%`
  - `%ProgramData%`
  - `%Temp%`
- Randomized names
- Base64-encoded PowerShell
- LOLBins used as launchers
- Registry keys with recent LastWrite timestamps

---

## 18. Correlation Recommendations

Always correlate registry findings with:
- Scheduled Tasks XML
- Event Logs (4688, 7045)
- Prefetch
- Amcache
- ShimCache
- File system timestamps

---

## 19. Tools for Validation

- RegRipper
- Registry Explorer
- Autoruns
- KAPE
- Velociraptor

---

## Disclaimer
Use this checklist **only on systems you are authorized to analyze**.  
Unauthorized access may violate local and international laws.

---
