nmap -A -p- http://10.81.155.178/
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-06 07:05 EST
Nmap scan report for http://10.81.155.178/
Host is up (0.080s latency).
Not shown: 65524 closed tcp ports (reset)
PORT      STATE SERVICE         VERSION
22/tcp    open  ssh             OpenSSH 9.6p1 Ubuntu 3ubuntu13.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 9a:08:13:d3:6a:6c:22:c1:0b:c5:ef:49:f5:06:56:c3 (ECDSA)
|_  256 5b:02:0d:17:d4:91:db:bf:eb:a9:34:a8:ad:ed:45:30 (ED25519)
80/tcp    open  http            nginx 1.24.0 (Ubuntu)
|_http-title: HopSec Asylum - Security Console
|_http-server-header: nginx/1.24.0 (Ubuntu)
8000/tcp  open  http-alt
| http-title: Fakebook - Sign In
|_Requested resource was /accounts/login/?next=/posts/
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.0 404 Not Found
|     Content-Type: text/html
|     X-Frame-Options: DENY
|     Content-Length: 179
|     Vary: Accept-Language
|     Content-Language: en
|     X-Content-Type-Options: nosniff
|     <!doctype html>
|     <html lang="en">
|     <head>
|     <title>Not Found</title>
|     </head>
|     <body>
|     <h1>Not Found</h1><p>The requested resource was not found on this server.</p>
|     </body>
|     </html>
|   GenericLines, Help, RTSPRequest, SIPOptions, Socks5, TerminalServerCookie: 
|     HTTP/1.1 400 Bad Request
|   GetRequest, HTTPOptions: 
|     HTTP/1.0 302 Found
|     Content-Type: text/html; charset=utf-8
|     Location: /posts/
|     X-Frame-Options: DENY
|     Content-Length: 0
|     Vary: Accept-Language
|     Content-Language: en
|_    X-Content-Type-Options: nosniff
8080/tcp  open  http            SimpleHTTPServer 0.6 (Python 3.12.3)
|_http-server-header: SimpleHTTP/0.6 Python/3.12.3
|_http-title: HopSec Asylum - Security Console
9001/tcp  open  tor-orport?
| fingerprint-strings: 
|   NULL: 
|     ASYLUM GATE CONTROL SYSTEM - SCADA TERMINAL v2.1 
|     [AUTHORIZED PERSONNEL ONLY] 
|     WARNING: This system controls critical infrastructure
|     access attempts are logged and monitored
|     Unauthorized access will result in immediate termination
|     Authentication required to access SCADA terminal
|     Provide authorization token from Part 1 to proceed
|_    [AUTH] Enter authorization token:
13400/tcp open  hadoop-datanode Apache Hadoop 1.24.0 (Ubuntu)
| hadoop-tasktracker-info: 
|_  Logs: loginBtn
|_http-title: HopSec Asylum \xE2\x80\x93 Facility Video Portal
| hadoop-datanode-info: 
|_  Logs: loginBtn
13401/tcp open  http            Werkzeug httpd 3.1.3 (Python 3.12.3)
|_http-title: 404 Not Found
|_http-server-header: Werkzeug/3.1.3 Python/3.12.3
13402/tcp open  http            nginx 1.24.0 (Ubuntu)
|_http-cors: HEAD GET OPTIONS
|_http-server-header: nginx/1.24.0 (Ubuntu)
|_http-title: Welcome to nginx!
13403/tcp open  unknown
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, Help, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NCP, RPCCheck, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, TerminalServerCookie, X11Probe: 
|     HTTP/1.1 400 Bad Request
|     Connection: close
|   FourOhFourRequest: 
|     HTTP/1.1 404 Not Found
|     Date: Sat, 06 Dec 2025 12:08:35 GMT
|     Connection: close
|   GetRequest, HTTPOptions: 
|     HTTP/1.1 404 Not Found
|     Date: Sat, 06 Dec 2025 12:08:33 GMT
|     Connection: close
|   RTSPRequest: 
|     HTTP/1.1 404 Not Found
|     Date: Sat, 06 Dec 2025 12:08:34 GMT
|_    Connection: close
13404/tcp open  unknown
| fingerprint-strings: 
|   FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, Kerberos, LDAPSearchReq, LPDString, RTSPRequest, SIPOptions, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
|_    unauthorized
21337/tcp open  http            Werkzeug httpd 3.0.1 (Python 3.12.3)
|_http-title: Unlock Hopper's Memories
|_http-server-header: Werkzeug/3.0.1 Python/3.12.3
4 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port8000-TCP:V=7.95%I=7%D=12/6%Time=69341CBC%P=x86_64-pc-linux-gnu%r(Ge
SF:nericLines,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(GetReques
SF:t,C9,"HTTP/1\.0\x20302\x20Found\r\nContent-Type:\x20text/html;\x20chars
SF:et=utf-8\r\nLocation:\x20/posts/\r\nX-Frame-Options:\x20DENY\r\nContent
SF:-Length:\x200\r\nVary:\x20Accept-Language\r\nContent-Language:\x20en\r\
SF:nX-Content-Type-Options:\x20nosniff\r\n\r\n")%r(FourOhFourRequest,160,"
SF:HTTP/1\.0\x20404\x20Not\x20Found\r\nContent-Type:\x20text/html\r\nX-Fra
SF:me-Options:\x20DENY\r\nContent-Length:\x20179\r\nVary:\x20Accept-Langua
SF:ge\r\nContent-Language:\x20en\r\nX-Content-Type-Options:\x20nosniff\r\n
SF:\r\n\n<!doctype\x20html>\n<html\x20lang=\"en\">\n<head>\n\x20\x20<title
SF:>Not\x20Found</title>\n</head>\n<body>\n\x20\x20<h1>Not\x20Found</h1><p
SF:>The\x20requested\x20resource\x20was\x20not\x20found\x20on\x20this\x20s
SF:erver\.</p>\n</body>\n</html>\n")%r(Socks5,1C,"HTTP/1\.1\x20400\x20Bad\
SF:x20Request\r\n\r\n")%r(HTTPOptions,C9,"HTTP/1\.0\x20302\x20Found\r\nCon
SF:tent-Type:\x20text/html;\x20charset=utf-8\r\nLocation:\x20/posts/\r\nX-
SF:Frame-Options:\x20DENY\r\nContent-Length:\x200\r\nVary:\x20Accept-Langu
SF:age\r\nContent-Language:\x20en\r\nX-Content-Type-Options:\x20nosniff\r\
SF:n\r\n")%r(RTSPRequest,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%
SF:r(Help,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(TerminalServe
SF:rCookie,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(SIPOptions,1
SF:C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port9001-TCP:V=7.95%I=7%D=12/6%Time=69341CBC%P=x86_64-pc-linux-gnu%r(NU
SF:LL,34F,"\n\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\
SF:xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90
SF:\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9
SF:0\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x
SF:90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\
SF:x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95
SF:\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x9
SF:5\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x
SF:95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\
SF:x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2
SF:\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe
SF:2\x95\x97\n\xe2\x95\x91\x20\x20\x20\x20\x20ASYLUM\x20GATE\x20CONTROL\x2
SF:0SYSTEM\x20-\x20SCADA\x20TERMINAL\x20v2\.1\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\xe2\x95\x91\n\xe2\x95\x91\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20\x20\x20\[AUTHORIZED\x20PERSONNEL\x20ONLY\]\x20\x20\x20\x
SF:20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\xe2\x95\x91\n\xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x
SF:95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\
SF:x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2
SF:\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe
SF:2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\x
SF:e2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\
SF:xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90
SF:\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9
SF:0\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x
SF:90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\
SF:x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95
SF:\x90\xe2\x95\x9d\n\n\[!\]\x20WARNING:\x20This\x20system\x20controls\x20
SF:critical\x20infrastructure\n\[!\]\x20All\x20access\x20attempts\x20are\x
SF:20logged\x20and\x20monitored\n\[!\]\x20Unauthorized\x20access\x20will\x
SF:20result\x20in\x20immediate\x20termination\n\n\[!\]\x20Authentication\x
SF:20required\x20to\x20access\x20SCADA\x20terminal\n\[!\]\x20Provide\x20au
SF:thorization\x20token\x20from\x20Part\x201\x20to\x20proceed\n\n\n\[AUTH\
SF:]\x20Enter\x20authorization\x20token:\x20");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port13403-TCP:V=7.95%I=7%D=12/6%Time=69341CC1%P=x86_64-pc-linux-gnu%r(G
SF:etRequest,52,"HTTP/1\.1\x20404\x20Not\x20Found\r\nDate:\x20Sat,\x2006\x
SF:20Dec\x202025\x2012:08:33\x20GMT\r\nConnection:\x20close\r\n\r\n")%r(HT
SF:TPOptions,52,"HTTP/1\.1\x20404\x20Not\x20Found\r\nDate:\x20Sat,\x2006\x
SF:20Dec\x202025\x2012:08:33\x20GMT\r\nConnection:\x20close\r\n\r\n")%r(RT
SF:SPRequest,52,"HTTP/1\.1\x20404\x20Not\x20Found\r\nDate:\x20Sat,\x2006\x
SF:20Dec\x202025\x2012:08:34\x20GMT\r\nConnection:\x20close\r\n\r\n")%r(RP
SF:CCheck,2F,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r
SF:\n\r\n")%r(DNSVersionBindReqTCP,2F,"HTTP/1\.1\x20400\x20Bad\x20Request\
SF:r\nConnection:\x20close\r\n\r\n")%r(DNSStatusRequestTCP,2F,"HTTP/1\.1\x
SF:20400\x20Bad\x20Request\r\nConnection:\x20close\r\n\r\n")%r(Help,2F,"HT
SF:TP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\n\r\n")%r(SS
SF:LSessionReq,2F,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20cl
SF:ose\r\n\r\n")%r(TerminalServerCookie,2F,"HTTP/1\.1\x20400\x20Bad\x20Req
SF:uest\r\nConnection:\x20close\r\n\r\n")%r(TLSSessionReq,2F,"HTTP/1\.1\x2
SF:0400\x20Bad\x20Request\r\nConnection:\x20close\r\n\r\n")%r(Kerberos,2F,
SF:"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\n\r\n")%r
SF:(SMBProgNeg,2F,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20cl
SF:ose\r\n\r\n")%r(X11Probe,2F,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConn
SF:ection:\x20close\r\n\r\n")%r(FourOhFourRequest,52,"HTTP/1\.1\x20404\x20
SF:Not\x20Found\r\nDate:\x20Sat,\x2006\x20Dec\x202025\x2012:08:35\x20GMT\r
SF:\nConnection:\x20close\r\n\r\n")%r(LPDString,2F,"HTTP/1\.1\x20400\x20Ba
SF:d\x20Request\r\nConnection:\x20close\r\n\r\n")%r(LDAPSearchReq,2F,"HTTP
SF:/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\n\r\n")%r(LDAP
SF:BindReq,2F,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\
SF:r\n\r\n")%r(SIPOptions,2F,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnec
SF:tion:\x20close\r\n\r\n")%r(LANDesk-RC,2F,"HTTP/1\.1\x20400\x20Bad\x20Re
SF:quest\r\nConnection:\x20close\r\n\r\n")%r(TerminalServer,2F,"HTTP/1\.1\
SF:x20400\x20Bad\x20Request\r\nConnection:\x20close\r\n\r\n")%r(NCP,2F,"HT
SF:TP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\n\r\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port13404-TCP:V=7.95%I=7%D=12/6%Time=69341CBC%P=x86_64-pc-linux-gnu%r(G
SF:enericLines,D,"unauthorized\n")%r(GetRequest,D,"unauthorized\n")%r(HTTP
SF:Options,D,"unauthorized\n")%r(RTSPRequest,D,"unauthorized\n")%r(Help,D,
SF:"unauthorized\n")%r(SSLSessionReq,D,"unauthorized\n")%r(TerminalServerC
SF:ookie,D,"unauthorized\n")%r(TLSSessionReq,D,"unauthorized\n")%r(Kerbero
SF:s,D,"unauthorized\n")%r(FourOhFourRequest,D,"unauthorized\n")%r(LPDStri
SF:ng,D,"unauthorized\n")%r(LDAPSearchReq,D,"unauthorized\n")%r(SIPOptions
SF:,D,"unauthorized\n");
Aggressive OS guesses: Linux 4.15 (97%), Linux 2.6.32 - 3.13 (96%), Linux 5.0 - 5.14 (96%), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3) (96%), Linux 3.10 - 4.11 (95%), Linux 3.2 - 4.14 (94%), Linux 4.15 - 5.19 (94%), Linux 2.6.32 - 3.10 (93%), HP P2000 G3 NAS device (93%), MikroTik RouterOS 6.36 - 6.48 (Linux 3.3.5) (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 4 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 5900/tcp)
HOP RTT      ADDRESS
1   58.31 ms 10.8.0.1
2   78.52 ms 192.168.128.1
3   ...
4   78.86 ms http://10.81.155.178/

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 351.03 seconds
