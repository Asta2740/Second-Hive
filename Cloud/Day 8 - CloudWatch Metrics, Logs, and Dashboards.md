# Day 8 - CloudWatch Metrics, Logs, and Dashboards

## Summary of Your Setup

You’ve made some solid updates to your CloudWatch agent configuration and used that data to create alarms and a dashboard. Here’s what you’ve accomplished:

Updated CloudWatch Agent Configuration:You modified the agent config to collect a variety of metrics and logs every 60 seconds, running as the root user. Here’s what you’re monitoring:

### Metrics

CPU: cpu_usage_idle and cpu_usage_system for all resources (*).

Disk: used_percent for all disks (*).

Disk I/O: io_time, writes, and reads for /dev/xvda1.

Memory: mem_used_percent.

Network: tcp_established and tcp_time_wait from netstat.

Swap: swap_used_percent.

Added dimensions like InstanceId, AutoScalingGroupName, ImageId, and InstanceType for better context.

### Logs

Collecting /var/log/auth.log into a log group named auth-log, with streams named by instance ID (e.g., {instance_id}-auth).

### Created Alarms

You set up alarms based on these metrics, though you didn’t specify the thresholds (we’ll tweak those later!).

### Built a Dashboard

### Added widgets for

CPU utilization (EC2)

Memory utilization

Hard disk utilization

RDS CPU utilization

The auth.log file

**Takeaway:** You’ve got a comprehensive monitoring setup that covers system performance and security—great work getting it all configured!

## Feedback on Your Setup

Your configuration is off to a strong start, but here are some notes and suggestions to make it even better:

### Metrics Selection

You’ve picked a solid set of metrics: CPU, memory, disk, and swap are essentials for performance, while disk I/O and network stats help spot bottlenecks.

Suggestion: If your instance has multiple disks beyond /dev/xvda1, consider adding them to the diskio section for full coverage.

### Log Collection

Monitoring /var/log/auth.log is a smart choice for security—it tracks authentication attempts and related events.

**Note:** Adding raw logs to the dashboard is unconventional since logs are usually analyzed separately. We’ll improve this with a more targeted approach tomorrow.

### Alarms

Awesome that you’ve set up alarms! To make them more effective, consider defining specific thresholds like:

CPU utilization > 80% for 5 minutes

Memory used > 90%

Disk used > 85%

RDS CPU > 70%

Idea: You could also try composite alarms if you want an alert only when multiple conditions are met (e.g., high CPU and high memory).

### Dashboard

Your dashboard covers key metrics, which is perfect for quick checks.

### Enhancement Ideas

Add network metrics (e.g., tcp_established or bytes in/out) to monitor connectivity.

If your RDS instance has other critical metrics (like database connections or latency), include those too.

For auth.log, raw logs might be hard to read—let’s switch to a summarized view (more on that below).

### Cost Consideration

Your 60-second collection interval is reasonable and should stay within the CloudWatch free tier for most metrics. Just keep an eye on custom metrics if you scale up, as they can add to costs.

### Security

Running the agent as root is fine for now, but ensure the IAM role (e.g., CloudWatchAgentServerPolicy) has only the permissions it needs. You’re likely good here, but it’s worth a double-check.

**Takeaway:** Your setup is already impressive—small tweaks like refining alarms and log visualization will take it to the next level.
