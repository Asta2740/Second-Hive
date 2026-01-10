# Day 10 - Custom CloudWatch Metrics with Python and Alerts

## Summary of Yesterday’s Work

Yesterday, you made great progress building a custom metric monitoring system for your website! Here’s what you accomplished:

Custom Metric for Active Sessions: You created a Python script to track active user sessions (sessions with activity in the last 30 minutes) by querying your PostgreSQL database. You then pushed this data to AWS CloudWatch as a custom metric called ActiveSessions. After some trial and error with PHP, you switched to Python—your preferred language—which worked perfectly.

Automation: You set up a cron job to run the script every 5 minutes, ensuring the metric updates regularly without manual effort.

Dashboard Integration: You added the ActiveSessions metric to your CloudWatch dashboard, giving you real-time visibility into active sessions.

SNS Notifications: You enabled Amazon SNS (Simple Notification Service) for all your CloudWatch alarms, so you’ll get notifications (e.g., via email) whenever an alarm enters the "In Alarm" state.

Your Python script connects to the database, counts active sessions, and sends the data to CloudWatch with the namespace PythonWebMetric, metric name ActiveSessions, and a dimension Machine: Pre_production. It’s working as intended, and you’re off to a strong start!

## Notes and Highlights

### Highlights

Switching to Python: Great decision to move from PHP to Python since you’re more comfortable with it. This made troubleshooting easier and sped up your success.

Custom Metric Success: You’ve bridged your application data (active sessions) with CloudWatch, a key skill for monitoring custom metrics.

Automation with Cron: Running the script every 5 minutes via cron keeps your data fresh without any manual work—excellent choice!

SNS Alerts: Setting up SNS for alarms ensures you’re proactively notified of issues, which is critical for system reliability.

## Important Notes

Security Concern: Your script contains hardcoded AWS credentials (aws_access_key_id and aws_secret_access_key). This is a big security risk because:

Anyone with access to your code (e.g., in a repo or on the server) could misuse these keys.

Fix: Use an IAM role for your EC2 instance instead. This is safer and lets boto3 authenticate automatically without credentials in the code.

Error Handling Missing: Your script assumes the database connection and query always work. If they fail (e.g., due to a network issue), the script will crash. Adding error handling can make it more reliable.

Metric Frequency: Updating every 5 minutes is a solid choice for most needs. It keeps you well within CloudWatch’s free tier (about 8,640 requests/month vs. the 1 million free limit).

## What You Need to Know

IAM Roles for Security: Instead of hardcoding AWS credentials, attach an IAM role to your EC2 instance with permissions like CloudWatchFullAccess (or a custom policy with just the permissions you need). Then, remove the aws_access_key_id and aws_secret_access_key lines from your script. boto3 will use the IAM role automatically.

CloudWatch Costs: Custom metrics are free up to 1 million API requests per month. Your current setup (12 pushes/hour * 24 hours * 30 days = ~8,640 requests) is safely within this limit, so no extra costs for now.

Metric Retention: CloudWatch keeps your metrics for 15 months, so you can look back at historical data if needed (e.g., to spot trends in active sessions).

Dimensions: Using the Machine: Pre_production dimension is smart—it’ll help you filter metrics if you add more servers later.

Here’s an improved version of your script with error handling and no hardcoded credentials (assuming an IAM role):

import socket

import psycopg2

import boto3

from dbconfig import DB_HOST, DB_NAME, DB_USER, DB_PASS

# Connect to CloudWatch (no credentials needed with IAM role)

cloudwatch = boto3.client('cloudwatch', region_name='eu-central-1')

### try

# Connect to PostgreSQL database

conn = psycopg2.connect(

host=DB_HOST,

dbname=DB_NAME,

user=DB_USER,

password=DB_PASS

)

cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM sessions WHERE last_activity > NOW() - INTERVAL '30 minutes'")

active_sessions = cur.fetchone()[0]

print(f"Active sessions: {active_sessions}")

### except Exception as e

print(f"Database error: {e}")

active_sessions = 0  # Default value if query fails

### finally

### if 'cur' in locals()

cur.close()

### if 'conn' in locals()

conn.close()

# Send the metric to CloudWatch

response = cloudwatch.put_metric_data(

### Namespace='PythonWebMetric',

### MetricData=[

{

'MetricName': 'ActiveSessions',

'Dimensions': [

{

'Name': 'Machine',

'Value': 'Pre_production'

}

],

'Value': int(active_sessions),

'Unit': 'Count'

}

]

)

print(response)
