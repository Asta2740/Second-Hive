# Day 16 - Automated IP Blocking with Network ACLs

## Key Points

It seems likely that you’ve made good progress on your AWS learning, focusing on security and automation tasks.

Research suggests sticking to the current hands-on phase, as it aligns with your infrastructure engineering goals and will make certification prep easier later.

The evidence leans toward continuing with planned tasks, but we can adjust if you prefer to start Cloud Practitioner certification earlier.

## Summary of Work Done

Yesterday, you completed the task of blocking IPs using AWS Network ACLs, building on your security monitoring efforts. You started by studying AWS WAF and Shield to understand their roles in web application security, but due to cost concerns and the need for an internet-facing ALB, you opted for Network ACLs, which are cost-effective and scalable. You created a Python script on your EC2 instance to analyze Apache logs, identify IPs with excessive 400-410 errors (over 5 in the last hour), and store them in an RDS table. You then developed a Lambda function to update the Network ACL with deny rules for these IPs, ensuring your system can automatically block potential threats. You set up the necessary IAM permissions and scheduled the EC2 script to run every hour via crontab.

## Notes and Highlights

Security Focus: Your decision to use Network ACLs instead of WAF shows a practical approach to staying within the free tier while enhancing security.

Effective Design: Separating log analysis (EC2) and NACL updates (Lambda) keeps each component focused, aligning with best practices.

Cost Consideration: Network ACLs have a default limit of 20 rules per ACL, which you should monitor to avoid hitting the cap.

Unexpected Detail: You discovered that most public IPs are dynamic, making your system more about threat detection and response than permanent blocking.

## Code Snippets for Documentation

Here are the key code snippets for reference:

### EC2 Python Script (check_ips.py)

```python
import socket
import psycopg2
import boto3
import os
import re
import json
import logging
from datetime import datetime, timedelta
# Set up logging
logging.basicConfig(
filename='/var/log/check_ips.log',
level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()
# Database connection details (using environment variables)
DB_PARAMS = {
'dbname': os.getenv('DB_NAME'),
'user': os.getenv('DB_USER'),
'password': os.getenv('DB_PASS'),
'host': os.getenv('DB_HOST'),
'port': '5432'
}
# Apache log pattern
LOG_PATTERN = re.compile(
r'^(?P<ip>\S+) \S+ \S+ \[(?P<logTime>[^\]]+)] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" (?P<status>\d{3}) (?P<bytes>\d+) "(?P<referrer>[^"]*)" "(?P<agent>[^"]*)"'
)
def get_problematic_ips():
try:
ip_counts = {}
end_time = datetime.now()
start_time = end_time - timedelta(hours=24)
with open('/var/log/apache2/access.log', 'r') as f:
for line in f:
match = LOG_PATTERN.match(line.strip())
if not match:
continue
log_time_str = match.group('logTime')
log_time = datetime.strptime(log_time_str.split()[0], '%d/%b/%Y:%H:%M:%S')
if start_time <= log_time <= end_time:
status = int(match.group('status'))
ip = match.group('ip')
if 400 <= status <= 410:
ip_counts[ip] = ip_counts.get(ip, 0) + 1
ip_list = [{'ip': ip, 'error_count': count} for ip, count in ip_counts.items() if count > 5]
logger.info(f"Found {len(ip_list)} IPs with frequent errors")
return ip_list
except FileNotFoundError:
logger.error("Apache access log file not found at /var/log/apache2/access.log")
return []
except Exception as e:
logger.error(f"Error in get_problematic_ips: {str(e)}")
return []
def check_and_store_ips(ip_list):
new_ips = []
try:
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS ip_errors (
ip VARCHAR(45) PRIMARY KEY,
timestamp TIMESTAMP,
error_count INTEGER
)
''')
for ip_data in ip_list:
ip = ip_data['ip']
cur.execute("SELECT EXISTS(SELECT 1 FROM ip_errors WHERE ip = %s)", (ip,))
exists = cur.fetchone()[0]
if not exists:
new_ips.append(ip_data)
cur.execute(
"INSERT INTO ip_errors (ip, timestamp, error_count) VALUES (%s, %s, %s)",
(ip, datetime.now(), ip_data['error_count'])
)
conn.commit()
except psycopg2.Error as e:
logger.error(f"Database error in check_and_store_ips: {str(e)}")
except Exception as e:
logger.error(f"Error in check_and_store_ips: {str(e)}")
finally:
cur.close()
conn.close()
return new_ips
def trigger_lambda(new_ips):
try:
if new_ips:
logger.info(f"Sending {len(new_ips)} new IPs to Lambda")
lambda_client.invoke(
FunctionName='ALC_Denier',
InvocationType='Event',
Payload=json.dumps({'new_ips': new_ips})
)
except Exception as e:
logger.error(f"Error triggering Lambda: {str(e)}")
def main():
try:
problematic_ips = get_problematic_ips()
if not problematic_ips:
logger.info("No problematic IPs found")
print("No problematic IPs found")
return
new_ips = check_and_store_ips(problematic_ips)
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
print(f"Error occurred: {e}")
if __name__ == "__main__":
main()
```

### Lambda Function (ALC_Denier)

```python
import boto3
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
ec2_client = boto3.client('ec2')
nacl_id = 'acl-0b1c28739eafe6265'
try:
new_ips_data = event.get('new_ips', [])
specific_ips = [ip_data['ip'] for ip_data in new_ips_data]
if not specific_ips:
logger.info("No IPs provided in event payload")
return {
'statusCode': 200,
'body': json.dumps({'message': 'No IPs provided to process'})
}
except KeyError as e:
logger.error(f"Invalid event payload: {str(e)}")
return {
'statusCode': 400,
'body': json.dumps({'error': 'Invalid event payload format'})
}
try:
response = ec2_client.describe_network_acls(NetworkAclIds=[nacl_id])
inbound_rules = []
used_rule_numbers = set()
existing_ips = set()
for nacl in response['NetworkAcls']:
for entry in nacl['Entries']:
if not entry.get('Egress', True):
rule = {
'RuleNumber': entry['RuleNumber'],
'Type': entry.get('Protocol', '-1'),
'Protocol': 'All' if entry['Protocol'] == '-1' else entry['Protocol'],
'PortRange': entry.get('PortRange', {'From': 'All', 'To': 'All'}),
'Source': entry['CidrBlock'],
'Action': entry['RuleAction']
}
inbound_rules.append(rule)
used_rule_numbers.add(entry['RuleNumber'])
existing_ips.add(entry['CidrBlock'])
new_ips_to_add = [ip for ip in specific_ips if f"{ip}/32" not in existing_ips]
if new_ips_to_add:
next_rule_number = 32765
new_rules_added = []
for ip in new_ips_to_add:
while next_rule_number in used_rule_numbers and next_rule_number > 0:
next_rule_number -= 1
if next_rule_number <= 0:
logger.error("No available rule numbers left")
return {
'statusCode': 500,
'body': json.dumps({'error': 'No available rule numbers left'})
}
ec2_client.create_network_acl_entry(
NetworkAclId=nacl_id,
RuleNumber=next_rule_number,
Protocol='-1',
RuleAction='deny',
Egress=False,
CidrBlock=f'{ip}/32',
PortRange={'From': 0, 'To': 65535}
)
used_rule_numbers.add(next_rule_number)
new_rules_added.append(next_rule_number)
next_rule_number -= 1
response = ec2_client.describe_network_acls(NetworkAclIds=[nacl_id])
inbound_rules = [
{
'RuleNumber': entry['RuleNumber'],
'Type': entry.get('Protocol', '-1'),
'Protocol': 'All' if entry['Protocol'] == '-1' else entry['Protocol'],
'PortRange': entry.get('PortRange', {'From': 'All', 'To': 'All'}),
'Source': entry['CidrBlock'],
'Action': entry['RuleAction']
}
for nacl in response['NetworkAcls']
for entry in nacl['Entries']
if not entry.get('Egress', True)
]
else:
logger.info("No new IPs to add; all specified IPs already exist in NACL")
return {
'statusCode': 200,
'body': json.dumps({
'inbound_rules': inbound_rules,
'ips_checked': specific_ips,
'new_ips_added': new_ips_to_add
})
}
except Exception as e:
logger.error(f"Error occurred: {str(e)}")
return {
'statusCode': 500,
'body': json.dumps({'error': str(e)})
}
```

### IAM Permissions for EC2 Script and Lambda

For logs access:

```json
{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Action": [
"logs:StartQuery",
"logs:GetQueryResults"
],
"Resource": "arn:aws:logs:eu-central-1:156041423134:log-group:apache-access-log:*"
},
{
"Effect": "Allow",
"Action": [
"logs:DescribeLogGroups"
],
"Resource": "arn:aws:logs:eu-central-1:156041423134:log-group:apache-access-log:*"
}
]
}
For EC2 and logging:
json
{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Action": [
"ec2:DescribeNetworkAcls",
"ec2:CreateNetworkAclEntry"
],
"Resource": "*"
},
{
"Effect": "Allow",
"Action": [
"logs:CreateLogGroup",
"logs:CreateLogStream",
"logs:PutLogEvents"
],
"Resource": "arn:aws:logs:eu-central-1:156041423134:*"
}
]
}
```

### RDS Table Creation

```sql
CREATE TABLE ip_errors (
ip VARCHAR(45) PRIMARY KEY,
timestamp TIMESTAMP NOT NULL,
error_count INTEGER NOT NULL,
CONSTRAINT valid_error_count CHECK (error_count > 0)
);
```

### Modified Query for Log Analysis

```text
SELECT COUNT(*) AS error_count
FROM logs
WHERE
message MATCHES /^(?<ip>\S+) \S+ \S+ \[(?<logTime>[^\]]+)] "(?<method>\S+) (?<url>\S+) (?<protocol>\S+)" (?<status>\d{3}) (?<bytes>\d+) "(?<referrer>[^"]*)" "(?<agent>[^"]*)"/
AND status >= 400
AND status <= 410
GROUP BY ip, TIME_BUCKET(1h)
HAVING error_count > 5
ORDER BY error_count DESC
```
