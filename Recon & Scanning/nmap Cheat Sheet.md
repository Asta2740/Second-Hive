# Nmap Cheat Sheet

## Basic scanning
- `nmap -sV [host]` version detection
- `nmap -sS [host]` SYN stealth scan
- `nmap -sU [host]` UDP scan
- `nmap -sT [host]` TCP connect scan
- `nmap -sN [host]` TCP null scan
- `nmap -sF [host]` TCP FIN scan

## Host discovery
- `nmap -sL [host/network]` list targets (DNS query)
- `nmap -sn [host/network]` ping scan (no port scan)
- `nmap -Pn [host/network]` skip host discovery

## Port scanning
- `nmap -sC [host]` default scripts
- `nmap -p [ports] [host]` scan specific ports
- `nmap -F [host]` fast scan (top ports)
- `nmap -p- [host]` scan all ports (1-65535)

## Version and OS detection
- `nmap -sV [host]` service versions
- `nmap -O [host]` OS detection
- `nmap -A [host]` aggressive (OS, version, scripts, traceroute)
- `nmap --script [name] [host]` run specific script

## Output options
- `nmap -oN [file] [host]` normal output
- `nmap -oX [file] [host]` XML output
- `nmap -oG [file] [host]` grepable output
- `nmap -oA [base] [host]` all major formats

## Timing options
- `nmap -T0..5 [host]` paranoid to insane
- Use slower timings to reduce detection and packet loss

## Firewall or IDS evasion
- `nmap --spoof-mac [address]` change source MAC
- `nmap -D RND:10 [host]` decoy scan
- `nmap -f [host]` fragment packets
- `nmap --data-length [len] [host]` append random data

## Notes
- SYN scans typically require admin or root privileges
- UDP scans are slower and may need retries
