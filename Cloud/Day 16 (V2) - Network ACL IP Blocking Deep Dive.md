# Day 16 (V2) - Network ACL IP Blocking Deep Dive

## Survey Note: Detailed Analysis of AWS Security and Monitoring Setup

Yesterday, you completed the task of blocking IPs using AWS Network ACLs, building on your security monitoring efforts after a day of procrastination. This section provides a comprehensive breakdown of your work, potential improvements, and sets the stage for today’s agenda, ensuring you have all the details for documentation and future reference.

## Context and Recent Progress

Your goal is to transition into infrastructure engineering and eventually security engineering, with a focus on AWS skills. You’ve already built a scalable web server setup with monitoring and automation, and recently completed tasks like restarting EC2 instances on high CPU using Lambda and Step Functions. Yesterday, you tackled IP blocking, which aligns with your security focus. Given today is Monday, March 24, 2025, at 12 AM (as per your request, though it’s actually Wednesday, March 26, 2025, at 11:38 AM PDT, we’ll align with your planning), we’re adjusting the week to fit your progress.

## Summary of Activities

You started by studying AWS WAF and Shield to understand their roles in web application security, reading detailed documentation and noting their functionalities:

AWS WAF: Filters HTTP/HTTPS traffic at Layer 7, protecting against SQL injection, XSS, and other OWASP Top 10 vulnerabilities, with customizable rules, managed rule groups, rate-based rules, and integration with CloudWatch for monitoring.

AWS Shield: Provides DDoS protection, with Standard (free, for Layers 3 and 4) and Advanced (paid, for Layer 7, with 24/7 support and detailed reporting).

However, you realized WAF requires an internet-facing ALB, which could incur costs beyond the free tier, so you explored alternatives. After researching, you compared methods like OS firewalls, router ACLs, and cloud security, opting for Network ACLs due to their scalability and no cost, given they can handle rules from 1 to 32766 and fit your needs for blocking threats.

Your implementation involved:

Theory and Design: You theorized a workflow where an EC2 Python script analyzes Apache logs, identifies IPs with excessive 400-410 errors (over 5 in the last hour), and stores them in an RDS table for reference. A Lambda function then updates the Network ACL to block these IPs, recognizing most public IPs are dynamic, making this more about threat detection and response.

### RDS Table Creation: You created the table to store IPs

```sql
CREATE TABLE ip_errors (
ip VARCHAR(45) PRIMARY KEY,
timestamp TIMESTAMP NOT NULL,
error_count INTEGER NOT NULL,
CONSTRAINT valid_error_count CHECK (error_count > 0)
);
```

Modified Query for Log Analysis: You crafted a query to identify problematic IPs:

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

EC2 Python Script (check_ips.py): You developed a script to analyze logs and store IPs:

```python
import socket
import psycopg2
import boto3
import os
import re
import json
import logging
from datetime import datetime, timedelta
# [Rest of the code as provided, including logging setup, DB_PARAMS, LOG_PATTERN, and functions get_problematic_ips, check_and_store_ips, trigger_lambda, main]
```

### Lambda Function (ALC_Denier): You created a function to update the Network ACL

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

### IAM Permissions: You set up the necessary permissions

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

Scheduling: You scheduled check_ips.py to run every hour via crontab, ensuring periodic checks for problematic IPs.

## Notes and Potential Improvements

Your approach is robust, but here are some notes and areas for enhancement:

Dynamic IPs: Since public IPs are often dynamic, your system is more about threat detection and response, which is appropriate for your current needs. However, consider adding a mechanism to remove old deny rules from the NACL to free up space, given the rule limit.

NACL Rule Limits: Network ACLs have a default limit of 20 rules per ACL, which can be increased, but monitor this to avoid hitting the cap. You might need to implement rule cleanup logic in your Lambda function.

Error Handling: Both scripts have good logging, but ensure the Lambda function handles cases where the NACL rule limit is reached or other errors occur during rule creation.

Testing: Thoroughly test the workflow, including edge cases like no new IPs found or NACL update failures, to ensure reliability.

Monitoring: Set up CloudWatch alarms for the Lambda function to track execution errors or timeouts, enhancing visibility.
