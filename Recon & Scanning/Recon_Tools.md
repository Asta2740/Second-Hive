## Custom ports interactions

```
nc -v M_IP M_port
```
* this will help you interact with the port and get you the service

## DNS Query 

```
dig @M_IP RRECORD_NEEDED_{A,AAA,MX,CNAME,TXT,NS} Domain_name

```
* A : maps ipv4
* AAAA : Maps ipv6
* MX : Specify the mail server of the Domain
* CNAME : Alias to another domain
* TXT : Hold Redable Text information used often for verification or securty
* NS : Delegates DNS management to other name servers

## listen Listening ports on the machine

```
ss -tunlp
```
on older systems
```
netstat
```
* with root permession you can view the process column