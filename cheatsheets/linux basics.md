# Studies Documentation

## Shell operators (Linux)
- `&` run command in background
- `&&` run second command only if first succeeds
- `>` redirect output and overwrite file
- `>>` append output to file

## File system basics
- `touch` create file
- `mkdir` create directory
- `cp` copy
- `mv` move or rename
- `rm` remove (use `-r` for directories)
- `file` detect file type

## Permissions 101
- Use `ls -l` to view permissions
- Format: type + `rwx` for user/group/others
- `ls -l` also shows owner, group, size, and timestamps
- Octal values: read 4, write 2, execute 1
- Execute on a directory means you can access entries inside it
- Change permissions with `chmod`
  - Numeric: `chmod 755 file`
  - Symbolic: `chmod ug+rwx file`, `chmod o+r file`
- Classes: `u` (user), `g` (group), `o` (other)
- Special permissions
  - SUID: run as file owner
  - SGID: run as group owner; new files inherit group
### Extended attributes (quick note)
- Add: `setfattr -n user.comment -v "note" file.txt`
- Read: `getfattr -n user.comment file.txt`

## Common directories
- `/etc` system configuration (e.g., `sudoers`, `passwd`, `shadow`)
- `/var` variable data and logs (`/var/log`)
- `/root` home for root
- `/tmp` temporary files, world-writable

## Terminal editors
- `nano` basic editor, shortcuts with Ctrl key
- `vim` powerful, available on minimal systems, supports syntax highlighting

## General utilities
- `wget` download files
- `scp` copy files over SSH (format: source destination)
- `python3 -m http.server` quick HTTP server (no indexing)
- `updog` lightweight server with indexing support
- `curl` for HTTP requests and testing

## Processes 101
- Processes have PIDs; managed by the kernel
- View processes: `ps`, `ps aux`, `top`
- Stop a process: `kill PID` (default SIGTERM)

## Automation with cron
- Cron format: `MIN HOUR DOM MON DOW COMMAND`
- Edit with `crontab -e`
- `*` is a wildcard for any value
- Example (every 12 hours)
  - `0 */12 * * * cp -R /home/cmnatic/Documents /var/backups/`
- Use online helpers: Crontab Generator, Cron Guru

## Redirection: `>/dev/null 2>&1`
- `/dev/null` discards output
- `>` redirects stdout
- `2>&1` redirects stderr to stdout
- Combined: discard all output

## Package management (APT)
- APT pulls from repositories defined in `/etc/apt`
- `apt update` refreshes package lists
- Add repos: `add-apt-repository`
- Remove repos: `add-apt-repository --remove ...`
- Install packages: `apt install name`
- Remove packages: `apt remove name`
- GPG keys validate package integrity
- Third-party repos are trusted by adding their GPG keys

## Logs
- Linux logs live in `/var/log`
- Examples: web server access/error logs, auth logs
- Log rotation is used to manage size

## Windows file permissions
- Full control, Modify, Read and execute, List folder contents, Read, Write

## Windows Event Viewer
- Three panes: tree, event list, actions
- Standard logs under Windows Logs
  - Application, System, Security, Setup, Forwarded Events
- Useful for troubleshooting and security investigations

## Active Directory basics
- Centralized identity and policy management
- Objects: users, groups, computers, printers, shares
- Users can be people or service accounts
- Machine accounts end with `$` and rotate passwords
- Delegation allows scoped admin rights
- Accidental deletion protection can be enabled

## Tcpdump essentials
- Capture and save packets: `tcpdump -i eth0 -w file.pcap`
- Filter by host: `host example.com`, `src host`, `dst host`
- Filter by port: `port 53`, `src port`, `dst port`
- Filter by protocol: `tcp`, `udp`, `icmp`
- Use logical operators: `and`, `or`, `not`
- Example filters
  - `tcpdump -i any tcp port 22`
  - `tcpdump -i wlo1 udp port 123`
  - `tcpdump -i eth0 host example.com and tcp port 443 -w https.pcap`
- Size filters: `greater LENGTH`, `less LENGTH`
- TCP flag filtering
  - `tcpdump "tcp[tcpflags] == tcp-syn"`
  - `tcpdump "tcp[tcpflags] & tcp-syn != 0"`

## Nmap basics
- Host discovery: `-sn`, `-PS`, `-PA`, `-PU`
- TCP scans: `-sT` (connect), `-sS` (SYN)
- UDP scan: `-sU`
- Port ranges: `-F`, `-p10-1024`, `-p-`
- Version detection: `-sV`, OS detection `-O`, aggressive `-A`
- Skip discovery when needed: `-Pn`
- Timing templates: `-T0` to `-T5`
- Output formats: `-oN`, `-oX`, `-oG`, `-oA`

## Asymmetric cryptography (quick note)
- Uses public and private keys
- Public key encrypts, private key decrypts (or vice versa for signatures)
- One-way math makes deriving the private key infeasible
- Often used to exchange a symmetric session key securely
