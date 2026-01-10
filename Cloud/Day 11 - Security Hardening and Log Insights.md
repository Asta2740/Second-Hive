# Day 11 - Security Hardening and Log Insights

## Summary of Yesterday’s Work

i made some serious progress yesterday in securing and monitoring your AWS setup. Here’s what you accomplished:

### Security Improvements

You removed hardcoded AWS credentials from your Python script and assigned an IAM role to your EC2 instance for access. This worked perfectly and is a major security upgrade!

You added try-except blocks to your Python script to handle errors, making it more reliable.

### Log Collection with CloudWatch Agent

You configured the CloudWatch agent to collect logs from three files:

/var/log/auth.log (authentication events)

/var/log/apache2/access.log (Apache web traffic)

/opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log (CloudWatch agent diagnostics)

This gives you a solid foundation for monitoring security, web activity, and the agent itself.

### Apache Log Analysis

You focused on the Apache access logs and wrote a CloudWatch Logs Insights query to parse the @message field, extracting key details like IP, log time, method, URL, status, etc.

You filtered for 404 errors to spot security issues or website problems, then grouped the results to analyze patterns.

You set up an SNS alarm for 404 spikes and added it to your CloudWatch dashboard for real-time visibility.

### Real-World Security Discovery

While checking your dashboard, you noticed an active user who wasn’t you or your friends.

After investigating a flood of 404 error notifications via email, you found a dictionary attack hitting your small site.

Since it’s just a demo site with no sensitive data, there was no harm, but catching this through your logs was a huge win and a great learning experience!

### Anomaly Detection

You enabled anomaly detection for your network in and out metrics, adding another layer to spot unusual traffic patterns.

In short, you didn’t just build a monitoring system—you used it to detect and debug a real security event. That’s impressive!

## Notes and Key Takeaways

Your work yesterday was top-notch, and here are some key points with the details you asked for:

### Security Wins

Replacing hardcoded credentials with an IAM role is a best practice that reduces the risk of leaks and follows AWS’s security standards. Great move!

Adding error handling with try-except ensures your script keeps running smoothly even if something fails.

### Log Collection Config

Here’s the CloudWatch agent configuration you used to collect logs from three sources:

```json
"logs": {
"logs_collected": {
"files": {
"collect_list": [
{
"file_path": "/var/log/auth.log",
"log_group_name": "auth-log",
"log_stream_name": "{instance_id}-auth",
"timezone": "UTC"
},
{
"file_path": "/var/log/apache2/access.log",
"log_group_name": "apache-access-log",
"log_stream_name": "{instance_id}-apache-access",
"timezone": "UTC"
},
{
"file_path": "/opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log",
"log_group_name": "cloudwatch-agent-logs",
"log_stream_name": "{instance_id}-agent",
"timezone": "UTC"
}
]
}
}
}
```

This setup is well thought out—covering security logs, web traffic, and agent health. Using {instance_id} in the stream names makes it easy to track logs per instance.

### Apache Log Query

Here’s the query you debugged and nailed for parsing Apache logs:

```text
fields @timestamp, @message, @logStream, @log
| parse @message /^(?<ip>\S+) \S+ \S+ \[(?<logTime>[^\]]+)] "(?<method>\S+) (?<url>\S+) (?<protocol>\S+)" (?<status>\d{3}) (?<bytes>\d+) "(?<referrer>[^"]*)" "(?<agent>[^"]*)"/
| filter status = 404
| stats count(*) by bin(5m), method, url, ip, status
```

This query is spot-on: it parses the log format correctly, filters for 404s, and groups results by 5-minute intervals, making it easy to spot trends or attacks. Nice work debugging it!

### Real-World Lesson

Catching that dictionary attack was a brilliant use of your setup. It shows how logs, alarms, and dashboards can reveal threats in real time.

Since your site is small, no damage was done, but this experience is gold for understanding security monitoring. Next time, you could add rate limiting or AWS WAF to block such attacks.

### Anomaly Detection

Adding anomaly detection for network traffic is a proactive step. It’ll help you catch DDoS attempts or unexpected spikes moving forward.

**Takeaway:** Your monitoring isn’t just theoretical—you’re already using it to solve real problems. That’s the kind of skill that sets you apart!
