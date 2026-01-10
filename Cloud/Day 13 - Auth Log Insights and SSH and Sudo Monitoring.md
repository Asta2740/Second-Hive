# Day 13 - Auth Log Insights and SSH/Sudo Monitoring

## Summary of Yesterday’s Work

Yesterday, you focused on enhancing your security monitoring by analyzing the auth-log with CloudWatch Logs Insights. Here’s what you got done:

### Set Up Log Collection

You added the auth-log to your CloudWatch agent, so now you’re collecting authentication-related logs for analysis.

### Created Queries for Security Insights

### Unauthorized SSH Attempts Query

After some debugging, you crafted a query to filter logs for unauthorized SSH attempts. It extracts the IP and message for logs containing keywords like "No supported authentication", "UnAuthorized", "invalid user", or "AuthorizedKeysCommand".

### Sudo Commands Query

You built a query to track sudo commands, parsing the IP and filtering for logs with "sudo.*COMMAND".

### Accepted SSH Connections Query

You also created a query to monitor successful SSH logins, filtering for "Accepted" or "Success" messages.

### CloudWatch Metric Math Reflection

You noted that the CloudWatch Metric Math task (combining metrics like active sessions and CPU utilization) might not be super useful right now since your active users are just visitors to index.php, tracked via PHP sessions. That’s a fair point, and it’s good you’re thinking critically about what metrics matter for your setup.

In short: You made your system more secure by setting up targeted log queries to monitor SSH activity and sudo commands. That’s a big step toward proactive security!

## Notes and Key Takeaways

Your work yesterday was awesome, and I’ve got some notes to highlight the important parts, including the queries you wrote:

### Queries for Logs Insights

### Unauthorized SSH Attempts

```sql
fields @timestamp, @message
| parse @message /(?<ip>\d+\.\d+\.\d+\.\d+)/
| filter @message like "No supported authentication" or @message like "UnAuthorized" or @message like "invalid user" or @message like "AuthorizedKeysCommand"
| sort @timestamp desc
```

This is a solid query! It extracts the IP and message for potential SSH threats. The keywords you chose are spot-on for catching unauthorized access attempts.

### Sudo Commands

```sql
fields @timestamp, @message
| parse @message /(?<ip>\d+\.\d+\.\d+\.\d+)/
| filter @message like /sudo.*COMMAND/
| sort @timestamp desc
```

Great for tracking privileged actions. This will help you spot any unusual or unauthorized use of sudo.

### Accepted SSH Connections

```sql
fields @timestamp, @message
| parse @message /(?<ip>\d+\.\d+\.\d+\.\d+)/
| filter @message like /Accepted/ or @message like "Success"
| sort @timestamp desc
```

This query is perfect for monitoring successful logins, which is key for auditing access.

### Security Monitoring

You’re thinking comprehensively about security by covering both failed and successful logins, plus sudo usage. That’s a well-rounded approach!

**Tip:** For the unauthorized SSH query, you might want to add a stats count(*) by ip at the end to see which IPs are trying multiple times. This can help spot brute-force attempts.

### CloudWatch Metric Math

You’re right that the metric math might not be super relevant for your current setup since your active users are just on index.php, tracked via PHP sessions. No worries—it’s still a handy skill for future projects where you might need to correlate metrics (e.g., in a more complex app with heavier resource usage).

**Takeaway:** You’ve built a strong foundation for security monitoring with targeted queries. Your critical thinking about which metrics matter shows you’re not just following steps—you’re applying them to your real setup.
