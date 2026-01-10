# Day 9 - Alarm Tuning and Custom Metrics for EC2/RDS

## Summary of Yesterday’s Work

Yesterday, you focused on fine-tuning your CloudWatch setup for your EC2 instance and RDS database to ensure availability and good performance. Here’s what you did:

### EC2 Monitoring

High CPU Utilization Alarm: Set to detect potential overload on your EC2 instance.

Network Traffic (In/Out) Alarms: Established to monitor for unusual activity, such as traffic spikes.

StatusCheckFailed Alarm: Added to alert you to instance health issues requiring immediate attention.

Memory Usage & Disk Space Alarms: Configured using the CloudWatch agent to track resource utilization.

### RDS Monitoring

CPU Utilization Alarm: Set to monitor performance, similar to EC2.

Freeable Memory Alarm: Created to warn of memory pressure that could lead to swapping.

Database Connections Alarm: Added, though you’re unsure of the ideal threshold.

Storage Space Alarm: Set to alert you when storage runs low.

High IOPS Alarms (Read/Write): Configured with a baseline (e.g., ReadIOPS > 1000 for 5 minutes) to detect disk bottlenecks, but you’d like more clarification on this.

### Dashboard Adjustments

Updated your CloudWatch dashboard to include these metrics and alarms, giving you a comprehensive health overview of your system.

### AWS Anomaly Detection

Explored CloudWatch Anomaly Detection for security purposes but decided against enabling it now. It’s recommended to have 14 days of data for best results, and since you shut down your instance after studying, you postponed this feature.

### Custom Metric for Active Sessions

Started building a custom metric to track active sessions on your website.

Used PHP session monitoring and created an RDS table (sessions) to store session data (session ID, IP, and last activity timestamp).

Updated index.php to log sessions into this table, but you haven’t yet connected this data to CloudWatch for visualization.

## Notes and Feedback

Your progress yesterday was impressive! You’ve laid a strong foundation for monitoring your EC2 and RDS setup. Here are some notes and suggestions:

### EC2 Alarms

Great Choices: The alarms for CPU utilization, network traffic, and StatusCheckFailed are excellent for ensuring availability and catching issues early.

Network Traffic Tip: Since your site likely has low baseline traffic, consider setting alarms relative to your normal usage (e.g., a 50% spike over your average). This could help detect unusual activity like a DDoS attack.

### RDS Alarms

Database Connections: For a small project, a threshold of 50-100 connections (e.g., >50 for 5 minutes) is a good starting point. You can tweak this later based on your app’s behavior.

IOPS Clarification: Your baseline of ReadIOPS > 1000 for 5 minutes is reasonable for a small app. If your site is read-heavy (e.g., lots of SELECT queries), you might want separate alarms for ReadIOPS and WriteIOPS to better pinpoint bottlenecks. For example:

ReadIOPS > 800 for 5 minutes (if reads dominate).

WriteIOPS > 200 for 5 minutes (if writes are less frequent).

Adjust these based on your app’s typical IOPS, which you can check in CloudWatch metrics over a few days.

Freeable Memory: Consider triggering this alarm when memory drops below 20% of your RDS instance’s total (e.g., <500 MB on a 2 GB instance) to avoid performance issues.

### Anomaly Detection

Smart Delay: You’re correct that anomaly detection needs historical data (ideally 14 days) to work well. Since you shut down your instance often, sticking with standard alarms makes sense for now.

Threshold Note: The "2 threshold" you mentioned likely refers to the anomaly detection band width (e.g., 2 standard deviations from the mean). Values outside this band trigger alerts, but you don’t need to worry about this until you enable it later.

Custom Metric and index.php

Solid Start: Your sessions table and PHP code to track session activity are well-implemented. The logic to insert new sessions and update existing ones based on last_activity is efficient.

Next Step: To get this data into CloudWatch, you’ll need to periodically query the active session count and push it as a custom metric. Your index.php already calculates this (SELECT COUNT(*) ...), so you’re halfway there!
