# Secure Protocols Overview

## Goal
Provide a quick reference for common secure network protocols and when to use them.

## Transport security (TLS)
- TLS provides encryption, integrity, and server authentication
- Common ports
  - HTTPS: TCP 443
  - SMTPS: TCP 465, SMTP with STARTTLS on 587
  - IMAPS: TCP 993
  - POP3S: TCP 995
- Certificates validate the server identity; clients must check the chain and hostname

## Remote access
- SSH (TCP 22) replaces Telnet
  - Secure shell, terminal, and tunneling
  - Key-based authentication preferred

## File transfer
- SFTP runs over SSH (TCP 22)
- FTPS runs FTP over TLS (TCP 21 plus data channel)

## Email security
- SMTP with STARTTLS or SMTPS for sending
- IMAPS or POP3S for retrieving
- SPF, DKIM, and DMARC for domain-level validation

## DNS security
- DNS over TLS (DoT) uses TCP 853
- DNS over HTTPS (DoH) uses HTTPS 443
- DNSSEC provides authenticity for DNS records

## VPN and tunneling
- IPsec (IKEv2) for site-to-site or remote access VPN
- WireGuard for modern, lightweight VPNs
- OpenVPN (TLS-based) for flexible deployments

## Best practices
- Disable insecure protocols (Telnet, FTP, HTTP for admin panels)
- Use strong cipher suites and modern TLS versions
- Keep certificates valid and rotate keys regularly
- Enforce least privilege and MFA where possible

## Note
The source Word document was empty; this is a baseline overview built from the file name.
