# Day 17 - CloudTrail and Automated SSH IP Blocking

## Summary of Yesterday’s Work

Yesterday, you focused on enhancing your AWS security setup while exploring AWS CloudTrail. Here’s what you accomplished:

Studied AWS CloudTrail: You gained a solid understanding of CloudTrail’s purpose and functionality—recording every action (events) made by users, roles, or AWS services via the AWS Management Console, CLI, SDKs, and APIs. You supplemented this by watching a YouTube video for a practical overview. Although you didn’t think you needed CloudTrail immediately, you explored its components: event history (90-day free log), trails (custom logging to S3), CloudTrail Lake (data lake for analysis), and Insights (anomaly detection).

Set Up a Management Trail: You enabled a management trail to start logging API activities, a key step for monitoring your AWS environment.

Identified SSH Login Attempts: While reviewing your dashboard, you noticed multiple IPs attempting unauthorized SSH logins on your EC2 instance. Although your SSH setup uses public-private keys (no passwords), you took a proactive approach to block these IPs to avoid potential future issues.

### Developed a Python Script: You created a script to

Parse /var/log/auth.log on your EC2 instance to identify IPs with authentication failures.

Filter IPs with more than 5 failures in the last 24 hours.

Store new problematic IPs in a PostgreSQL database.

Trigger a Lambda function (ALC_Denier) to block these IPs (likely via Network ACLs).

Here’s the code snippet you wrote:

```python
import os
import re
import json
import logging
import psycopg2
import boto3
import subprocess
from datetime import datetime, timedelta
# Set up logging
logging.basicConfig(
filename='/var/log/check_ips.log',
level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()
# 🔹 Log file path
AUTH_LOG_PATH = "/var/log/auth.log"
# 🔹 Authentication failure messages to search for
FAILURE_MESSAGES = [
"No supported authentication",
"UnAuthorized",
"invalid user",
"AuthorizedKeysCommand"
]
# 🔹 Regex pattern to extract IPs
IP_PATTERN = re.compile(r'(\d+\.\d+\.\d+\.\d+)')
# 🔹 Database connection details
DB_PARAMS = {
'dbname': os.getenv('DB_NAME'),
'user': os.getenv('DB_USER'),
'password': os.getenv('DB_PASS'),
'host': os.getenv('DB_HOST'),
'port': '5432'
}
# 🔹 AWS Lambda client (adjust region as needed)
lambda_client = boto3.client('lambda', region_name='eu-central-1')
# 🔥 Function to extract problematic IPs
def get_problematic_ips():
try:
ip_counts = {}
end_time = datetime.now()
start_time = end_time - timedelta(hours=24)
print(start_time)
logger.info(f"Reading authentication log from {AUTH_LOG_PATH}")
# 🔹 Run grep command to get failed authentication logs
grep_command = f'grep -E "{"|".join(FAILURE_MESSAGES)}" {AUTH_LOG_PATH}'
result = subprocess.run(grep_command, shell=True, capture_output=True, text=True)
if not result.stdout:
logger.info("No matching log entries found.")
return []
# 🔹 Process each log line
for line in result.stdout.splitlines():
ip_match = IP_PATTERN.search(line)
if ip_match:
ip = ip_match.group(1)
ip_counts[ip] = ip_counts.get(ip, 0) + 1
# 🔹 Filter IPs with more than 5 errors
ip_list = [{'ip': ip, 'error_count': count} for ip, count in ip_counts.items() if count > 5]
logger.info(f"Found {len(ip_list)} problematic IPs")
return ip_list
except Exception as e:
logger.error(f"Error in get_problematic_ips: {str(e)}")
return []
# 🔥 Function to check IPs against database
def check_and_store_ips(ip_list):
print(ip_list)
new_ips = []
try:
# Connect to PostgreSQL
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()
logger.info("Checking IPs against database")
for ip_data in ip_list:
ip = ip_data['ip']
print(ip)
cur.execute("SELECT EXISTS(SELECT 1 FROM ip_errors WHERE ip = %s)", (ip,))
exists = cur.fetchone()[0]
print(exists)
if not exists:
new_ips.append(ip_data)
cur.execute(
"INSERT INTO ip_errors (ip, timestamp, error_count) VALUES (%s, %s, %s)",
(ip, datetime.now(), ip_data['error_count'])
)
logger.info(f"Added new IP to database: {ip}")
conn.commit()
logger.info(f"Stored {len(new_ips)} new IPs in database")
except psycopg2.Error as e:
logger.error(f"Database error in check_and_store_ips: {str(e)}")
except Exception as e:
logger.error(f"Error in check_and_store_ips: {str(e)}")
finally:
cur.close()
conn.close()
return new_ips
# 🔥 Function to trigger AWS Lambda
def trigger_lambda(new_ips):
try:
if new_ips:
logger.info(f"Sending {len(new_ips)} new IPs to Lambda")
lambda_client.invoke(
FunctionName='ALC_Denier',  # 🔹 Replace with actual Lambda function name
InvocationType='Event',
Payload=json.dumps({'new_ips': new_ips})
)
logger.info("Successfully triggered Lambda")
except Exception as e:
logger.error(f"Error triggering Lambda: {str(e)}")
# 🔥 Main function
def main():
try:
# Step 1: Get problematic IPs
problematic_ips = get_problematic_ips()
if not problematic_ips:
logger.info("No problematic IPs found")
print("No problematic IPs found")
return
# Step 2: Check against database and store new IPs
new_ips = check_and_store_ips(problematic_ips)
# Step 3: Trigger AWS Lambda if new IPs are found
if new_ips:
logger.info(f"New IPs detected: {json.dumps(new_ips)}")
print("New IPs detected:")
print(json.dumps(new_ips, indent=2))
trigger_lambda(new_ips)
else:
logger.info("No new IPs detected")
print("No new IPs detected")
except Exception as e:
logger.error(f"Error in main: {str(e)}")
print(f"Error occurred: {str(e)}")
if __name__ == "__main__":
main()
```

## Notes and Important Highlights

### AWS CloudTrail

Tracks API activities (management and data events), providing visibility into your AWS environment.

Your management trail logs management events (e.g., resource changes), which is a great starting point for auditing.

Free 90-day event history is active by default; trails to S3 enable longer retention.

### Security Script

Uses regex (\d+\.\d+\.\d+\.\d+) to efficiently extract IPs from auth.log.

Stores IPs in a PostgreSQL database for tracking and deduplication.

Triggers a Lambda function to automate blocking, reducing manual effort.

### Efficiency

Filters IPs with >5 failures, a reasonable threshold to catch persistent attackers.

Combines grep and Python for fast log parsing.

### Key Takeaways

Proactive security: Blocking IPs even with a secure SSH setup shows foresight.

Automation: Your script ties EC2 logs, a database, and Lambda into a seamless workflow.

Learning: Exploring CloudTrail and acting on dashboard insights reflect a hands-on approach.
