## Systemd
View all logs from all day:
journalctl

Follow logs live (like tail -f):
journalctl -f

Show only today:
journalctl --since today 

shows 2 48 hours worth of logs
journalctl --since "2 days ago"

Show logs for a service:
journalctl -u nginx

Show boot logs:
journalctl -b

Pretty JSON mode:
journalctl -o json-prettyjour