# Windows Registry Forensics Guide

## Overview
It's the brain of the windows and it stores how the winodws functions and all the configurations withing

It's stored in serveral files each file contain a different configuration settings , they're known as the Hives

The Windows Registry is a hierarchical database that stores configuration settings and operational data for:
- The operating system
- Installed applications
- User profiles
- Hardware
- Security policies

In forensic investigations, registry artifacts are critical for:
- User activity reconstruction
- Malware persistence analysis
- Timeline creation
- Account and system configuration analysis

---

## 1. Registry Hive Summary

| Hive Name    | Loaded Key            | Description |
|--------------|-----------------------|------------|
| SYSTEM       | HKLM\SYSTEM           | System configuration, services, hardware, boot info |
| SOFTWARE     | HKLM\SOFTWARE         | Installed applications, OS configuration |
| SAM          | HKLM\SAM              | Local user and group account info |
| SECURITY     | HKLM\SECURITY         | Security policies, audit data |
| DEFAULT      | HKU\.DEFAULT          | Default user profile (login screen) |
| NTUSER.DAT   | HKCU                  | Per-user configuration |
| USRCLASS.DAT | HKCU\Software\Classes | User COM objects, shell extensions |

---

## 2. Registry Hive Locations on Disk

### System-Wide Hives

C:\Windows\System32\config\


| File Name| Registry Key |
|----------|------------|
| SYSTEM   | HKLM\SYSTEM |
| SOFTWARE | HKLM\SOFTWARE |
| SAM      | HKLM\SAM |
| SECURITY | HKLM\SECURITY |
| DEFAULT  | HKU\.DEFAULT |

---

### User-Specific Hives

C:\Users<username>\


| File Name | Registry Key |
|--------|------------|
| NTUSER.DAT | HKCU |
| USRCLASS.DAT | HKCU\Software\Classes |

Location of `USRCLASS.DAT`:

C:\Users<username>\AppData\Local\Microsoft\Windows\


---

## 3. Detailed Hive Contents (Forensic Relevance)

### 3.1 SYSTEM Hive
**Path:** `HKLM\SYSTEM`

Contains:
- Control Sets
- Services and drivers
- Hardware configuration
- System boot info

Key Areas:

HKLM\SYSTEM\CurrentControlSet\Services
HKLM\SYSTEM\MountedDevices
HKLM\SYSTEM\Select


Forensic Value:
- USB device history
- Driver load order
- System startup configuration
- Time zone settings

---

### 3.2 SOFTWARE Hive
**Path:** `HKLM\SOFTWARE`

Contains:
- Installed software
- OS configuration
- Application paths
- Auto-start programs

Key Areas:

HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion


Forensic Value:
- Installed applications
- OS version and build
- Persistence mechanisms

---

### 3.3 SAM Hive
**Path:** `HKLM\SAM`

Contains:
- Local user accounts
- Group membership
- Password hashes (NTLM)

Forensic Value:
- User enumeration
- Account creation timestamps
- Password hash extraction (offline only)

---

### 3.4 SECURITY Hive
**Path:** `HKLM\SECURITY`

Contains:
- Local security policy
- Audit policy
- Cached credentials

Forensic Value:
- Logon policies
- Audit settings
- Credential artifacts

---

### 3.5 DEFAULT Hive
**Path:** `HKU\.DEFAULT`

Contains:
- Default user settings
- Login screen configuration

Forensic Value:
- System-wide default behavior
- Pre-login settings

---

### 3.6 NTUSER.DAT (Per User)
**Path:** `HKCU`

Contains:
- User preferences
- Application usage
- Shell and Explorer settings

Forensic Value:
- User activity tracking
- Recently opened files
- Application execution history

---

### 3.7 USRCLASS.DAT
**Path:** `HKCU\Software\Classes`

Contains:
- COM registrations
- Shell extensions
- File associations

Forensic Value:
- Malware persistence
- Hijacked file handlers
- COM abuse artifacts

---

## 4. High-Value Registry Locations (Forensics)

### 4.1 Program Execution Evidence

| Artifact | Registry Path |
|------|--------------|
| UserAssist | HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist |
| ShimCache (AppCompatCache) | HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache |
| Amcache | HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Amcache |
| MUICache | HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache |

---

### 4.2 Persistence Mechanisms

| Method | Registry Path |
|-----|-------------|
| Run Keys | HKCU\Software\Microsoft\Windows\CurrentVersion\Run |
| RunOnce | HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce |
| Services | HKLM\SYSTEM\CurrentControlSet\Services |
| Winlogon | HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon |

---

### 4.3 USB & External Devices

| Artifact | Registry Path |
|------|-------------|
| USB Devices | HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR |
| Mounted Volumes | HKLM\SYSTEM\MountedDevices |
| Device Classes | HKLM\SYSTEM\CurrentControlSet\Control\DeviceClasses |

---

### 4.4 User Activity & File Access

| Artifact | Registry Path |
|------|-------------|
| Recent Docs | HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs |
| Typed Paths | HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths |
| Search History | HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery |

---

### 4.5 Network & Connectivity

| Artifact | Registry Path |
|------|-------------|
| Network Profiles | HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles |
| Wi-Fi Profiles | HKLM\SOFTWARE\Microsoft\WlanSvc\Interfaces |

---

## 5. Timeline-Critical Registry Keys

| Artifact | Purpose |
|------|--------|
| LastWrite Time | Key modification tracking |
| InstallDate | OS install time |
| ProfileLoadTime | User logon times |
| ShutdownTime | Last system shutdown |

---

## 6. Registry Forensics Tips

- Registry timestamps use **LastWrite Time**
- Offline analysis recommended (avoid live contamination)
- Combine registry artifacts with:
  - Event Logs
  - Prefetch
  - Amcache
  - ShimCache

---

## 7. Common Registry Forensic Tools

- RegRipper
- Registry Explorer
- Autopsy
- KAPE
- FTK / EnCase

---

## Disclaimer
All analysis should be conducted on systems you are **authorized to investigate**. Improper access may violate local laws.

---
