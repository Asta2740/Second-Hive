# Full Disclosure and Ratings - TryHackMe Progress

## Exercises finished
- Pickle Rick

## Needs review
- Windows logs reading and troubleshooting
- Shell operators in Linux
- Search for files in Linux
- Permissions in Linux
- Vim usage basics

## Fundamentals - Windows
### Windows Fundamentals 1
- OS overview and core components
- GUI navigation and common system folders
- Accounts and permissions (local users vs admins)
- UAC settings and why prompts appear
- Task Manager and Control Panel quick map

### Windows Fundamentals 2
- Troubleshooting tools: `msconfig`, `compmgmt.msc`, Event Viewer
- Shared folders and access controls
- Device Manager and drivers
- Services and applications (startup vs running)
- `msinfo32` and `resmon.exe` for system details
- Command Prompt basics
- Registry Editor overview
  - User profile locations
  - Installed applications
  - Folder property settings
  - Hardware inventory
  - Open ports and services

### Windows Fundamentals 3
- Defender and threat protection workflow
- Firewall and network protection
- App and browser control
- Device security features
- BitLocker basics and when to use it
- Volume Shadow Copy Service (VSS) for backup and recovery

## Fundamentals - Linux
### Linux Fundamentals 1
- First interaction with a Linux host
- Basic commands and shell navigation
- Shell operators overview

### Linux Fundamentals 2
- Accessing hosts with SSH
- Commands and arguments
- Filesystem operations: `touch`, `mkdir`, `cp`, `mv`, `rm`, `file`
- Permissions overview and `ls -l` interpretation
- Common directories
  - `/etc` system configuration
  - `/var` variable data and logs
  - `/root` root home
  - `/tmp` temporary files (cleared on reboot)

### Linux Fundamentals 3
- Editors: nano and vim (vim for minimal environments)
- Download and transfer tools: `wget`, `scp`
- Quick web servers: `python -m http.server`, `updog`
- Processes and monitoring: `ps`, `ps aux`, `top`
- Process control: `kill` and signals (SIGTERM, SIGKILL, SIGSTOP)
- `systemd` as PID 1 and service parent
- `systemctl` basics: start/stop/enable/disable/status
- Foreground and background: `&`, `fg`
- Automation with crontab
  - Format: `MIN HOUR DOM MON DOW COMMAND`
  - `crontab -e` and generators
- Package management
  - APT repos in `/etc/apt`
  - `add-apt-repository`, `apt remove`
- Logs in `/var/log`

## Web Fundamentals
- How web content is assembled and delivered
- HTTP vs HTTPS and the request/response flow
- URLs, headers, and common request methods
  - GET, POST, PUT, PATCH, DELETE
- Status code families and common codes
- Request/response headers to know (Host, User-Agent, Content-Type, Set-Cookie, Cache-Control)
- Cookies and session behavior
- Common issues: commented HTML data, HTML injection
- Defense fundamentals (input validation, auth checks, least privilege)

## Digital Forensics
- NIST process: collection, examination, analysis, reporting
- Collection types: computer, mobile, network, database, cloud, email
- Evidence acquisition
  - Legal authorization (search warrant)
  - Chain of custody and accountability
  - Write blockers to prevent tampering
- Windows forensics
  - Disk image (bit-for-bit)
  - Memory image
  - Tools: FTK Imager, Autopsy, DumpIt, Volatility
- Metadata checks
  - `pdfinfo`, `exiftool`

## Incident Response Fundamentals
- Incidents and alert types
  - Malware, breaches, data leaks, insider, DoS
- SANS process: preparation, identification, containment, eradication, recovery, lessons learned
- NIST process: preparation, detection/analysis, containment/eradication/recovery, post-incident
- Key components
  - Roles and responsibilities
  - Communication and escalation paths
- Tools and techniques
  - SIEM for log collection and correlation
  - AV for commodity malware
  - EDR for advanced threats
  - Playbooks and runbooks

## Logs Fundamentals
- Use cases: monitoring, investigation, troubleshooting, performance, compliance
- Log types
  - System, security, application, audit, network
- Windows Event Viewer
  - Application, System, Security logs
  - Common Event IDs: 4624, 4625, 4634, 4720, 4724, 4722, 4725, 4726

## SIEM Overview
- Why SIEM: centralized visibility and correlation
- Capabilities: parsing, detection, visualization, early warning, 24/7 monitoring
- Log sources
  - Host-centric: user auth, process execution, file access
  - Network-centric: HTTP, SSH, firewall logs
- Common log locations
  - Windows: Event Viewer, Sysmon
  - Linux: `/var/log`, `/var/log/auth.log`, `/var/log/secure`, `/var/log/kern`, web server logs
- Ingestion methods: agents/forwarders, syslog, manual upload, port forwarding

## IDS Fundamentals
- Purpose: detect malicious activity when defenses are bypassed
- Types
  - HIDS: host-based, detailed but heavy to manage
  - NIDS: network-wide visibility
- Detection modes
  - Signature-based (good for known attacks)
  - Anomaly-based (can detect zero days, but noisy)
  - Hybrid (combines both)
- Snort overview
  - Modes: sniffer, packet logger, IDS mode
  - Rule location: `/etc/snort/rules`
  - Example rule components (action, protocol, source, destination, metadata)
  - Testing: live (`-i`) and pcap (`-r`) modes

## Networking Recap
- OSI and TCP/IP layers
- Packets vs frames, handshakes, UDP vs TCP
- Core protocols: ARP, DHCP, DNS, ICMP
- Devices and topologies
- VPN basics: PPP, IPsec, PPTP
- DNS hierarchy: root, TLD, second level, subdomain
- Record types: A, AAAA, CNAME, MX

## Firewall Fundamentals
- Purpose: control traffic and reduce attack surface
- Types
  - Stateless (L3/L4, fast, no connection tracking)
  - Stateful (tracks connections, richer rules)
  - Proxy (L7 inspection, content filtering)
  - Next-gen (L3-L7, DPI, IPS, threat protection)
- Rule components: src/dst, port, protocol, action, direction
- Linux firewalls (Netfilter)
  - `iptables`, `nftables`, `firewalld`
