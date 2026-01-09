# Networking Core Notes

## DNS basics
- Ports: UDP 53 for most queries, TCP 53 for zone transfers and large replies
- Record types
  - A: hostname to IPv4
  - AAAA: hostname to IPv6
  - CNAME: alias to another name
  - MX: mail exchanger for a domain
- Tools: `nslookup` for querying records
- Authority and ownership
  - Domain registrant controls DNS records
  - WHOIS data is public unless privacy service is used
  - `whois` CLI can query registrant, creation date, updates

## Telnet overview
- Telnet is a plain-text remote terminal protocol
- Useful for testing raw TCP services
- Examples of servers/ports
  - Echo: TCP 7
  - Daytime: TCP 13
  - HTTP: TCP 80
- Note: Telnet is insecure; prefer SSH for administration

## FTP essentials
- Purpose: file transfer, separate control and data channels
- Default port: TCP 21 (control)
- Common commands
  - `USER`, `PASS` for login
  - `RETR` download
  - `STOR` upload
- Example workflow
  - Login as `anonymous`
  - `ls` to list files
  - `type ascii` for text mode
  - `get file.txt` to download

## SMTP basics (sending mail)
- Default port: TCP 25
- Session flow: greet, sender, recipient, message data
- Common commands
  - `HELO` / `EHLO`
  - `MAIL FROM`
  - `RCPT TO`
  - `DATA`, end with `.` on its own line
- Telnet can be used to understand SMTP but is manual

## POP3 basics (retrieving mail)
- Default port: TCP 110 (or 995 for POP3S)
- Common commands
  - `USER`, `PASS`
  - `STAT` (count and size)
  - `LIST` (message list)
  - `RETR` (retrieve message)
  - `DELE` (delete message)
  - `QUIT`

## IMAP basics (mailbox management)
- Default port: TCP 143 (or 993 for IMAPS)
- Common commands
  - `LOGIN` user pass
  - `SELECT` mailbox
  - `FETCH` message parts
  - `MOVE` or `COPY` messages
  - `LOGOUT`

## Security notes
- Prefer encrypted variants when possible
  - SSH instead of Telnet
  - FTPS or SFTP instead of FTP
  - SMTPS/STARTTLS for SMTP, IMAPS/POP3S for mail retrieval
