 ## simple port scan

 ```
 nmap  M_IP
 ```
 * scans for the Most common 1000 port 


 ## Banner script

```
nmap --script=banner  M_IP

```
* shows what's behind each port 

## UDP Scan

```
nmap -sU M_IP
```
* nmap usually scans the tcp , the -sU flag checks for UDP ports

## nmap Flags

### Additional flags

```
-sL 	                         List scan – list targets without scanning
--reason 	                     explains how Nmap made its conclusion
-v 	                             verbose
-vv 	                         very verbose
-d 	                             debugging
-dd                         	 more details for debugging
--source-port PORT_NUM           specify source port number
--data-length NUM                append random data to reach given length
```
### Host Discovery 	
```
-sn 	Ping scan – host discovery only
-n 	        no DNS lookup
-R 	        reverse-DNS lookup for all hosts
```

## Port Scanning 	
```
-sT 	                        TCP connect scan – complete three-way handshake
-sS 	                        TCP SYN – only first step of the three-way handshake
-sU         	                UDP Scan
-F 	                            Fast mode – scans the 100 most common ports
-p[range] 	                    Specifies a range of port numbers – -p- scans all the ports
-Pn 	                        SKIP Network discovery
-O          	                OS detection
-sV 	                        Service version detection
-sV --version-light         	try the most likely probes (2)
-sV --version-all 	            try all available probes (9)
--traceroute 	                run traceroute to target
--script=SCRIPTS            	Nmap scripts to run
-sC or --script=default 	    run default scripts
-A          	                EQUivlent to -sV -O -sC --traceroute 
```
## Timing 	
```
-T<0-5> 	        Timing template 
                    paranoid (0), sneaky (1), polite (2), normal (3), aggressive (4), and insane (5)
--min-parallelism <numprobes> and --max-parallelism <numprobes> 	
                    Minimum and maximum number of parallel probes
--min-rate <number> and --max-rate <number> 
                	Minimum and maximum rate (packets/second)
--host-timeout 	    Maximum amount of time to wait for a target host Real-time output 	

-v 	                Verbosity level – for example, -vv and -v4
-d              	Debugging level – for example -d and -d9
```
## Reports output
```
-oN <filename> 	Normal output
-oX <filename> 	XML output
-oG <filename> 	grep-able output
-oA <basename> 	Output in all major formats
```

## Host Discovery

Scan Type 	Example Command
```
ARP Scan        	            sudo nmap -PR -sn MACHINE_IP/24
ICMP Echo Scan              	sudo nmap -PE -sn MACHINE_IP/24
ICMP Timestamp Scan         	sudo nmap -PP -sn MACHINE_IP/24
ICMP Address Mask Scan 	        sudo nmap -PM -sn MACHINE_IP/24
TCP SYN Ping Scan 	            sudo nmap -PS22,80,443 -sn MACHINE_IP/30
TCP ACK Ping Scan 	            sudo nmap -PA22,80,443 -sn MACHINE_IP/30
UDP Ping Scan               	sudo nmap -PU53,161,162 -sn MACHINE_IP/30
```

## Advanced port scanning

TCP Null Scan 	                sudo nmap -sN MACHINE_IP
TCP FIN Scan                	sudo nmap -sF MACHINE_IP
TCP Xmas Scan 	                sudo nmap -sX MACHINE_IP
TCP Maimon Scan             	sudo nmap -sM MACHINE_IP
TCP ACK Scan 	                sudo nmap -sA MACHINE_IP
TCP Window Scan              	sudo nmap -sW MACHINE_IP
Custom TCP Scan             	sudo nmap --scanflags URGACKPSHRSTSYNFIN MACHINE_IP
Spoofed Source IP           	sudo nmap -S SPOOFED_IP MACHINE_IP
Spoofed MAC Address         	--spoof-mac SPOOFED_MAC
Decoy Scan 	                    nmap -D DECOY_IP,ME MACHINE_IP
Idle (Zombie) Scan 	            sudo nmap -sI ZOMBIE_IP MACHINE_IP
Fragment IP data into 8 bytes 	-f
Fragment IP data into 16 bytes 	-ff