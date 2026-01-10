# Day 19 - Serverless Portfolio Site Implementation

## Overview

**Goal:** A serverless portfolio site hosted on S3 with a form to submit name and comment, secured with HTTPS via CloudFront, processed by Lambda, and stored in S3.

## Resources

S3 Bucket: mini-hello (ARN: arn:aws:s3:::mini-hello)

CloudFront: d1rbt0ac744n52.cloudfront.net (ARN: arn:aws:cloudfront::156041423134:distribution/E31956LHYM1O1V)

Lambda Function: mini-hello-formsubmissions (ARN: arn:aws:lambda:eu-central-1:156041423134:function:mini-hello-formsubmissions)

API Gateway: mini-submissionapi (ARN: arn:aws:execute-api:eu-central-1:156041423134:48psjszyy3/*/POST/submit)

IAM Role: mini-world (ARN: arn:aws:iam::156041423134:role/mini-world)

## Steps Recap

### S3 Setup

Bucket mini-hello configured for static website hosting.

Uploaded index.html with a form sending data to https://48psjszyy3.execute-api.eu-central-1.amazonaws.com/prod/submit (derived from your API ARN).

Made public for access via http://mini-hello.s3-website-eu-central-1.amazonaws.com.

### CloudFront

Distribution d1rbt0ac744n52.cloudfront.net set up for HTTPS access to mini-hello.

### API Gateway

API mini-submissionapi with /submit POST method.

Initially passed flat event ({"name": "test", "comment": "test2"}), suggesting non-proxy integration.

CORS enabled for browser compatibility.

### Lambda

Function mini-hello-formsubmissions created in eu-central-1.

Initially hit KeyError: 'body', adapted to handle flat event.

Added S3 write capability.

### S3 Storage

Updated Lambda to save form data to mini-hello under messages/ prefix.

## Corrected Lambda Function Code

This code uses your flat event structure ({"name": "test", "comment": "test2"}) and writes it to your S3 bucket mini-hello. It’s tailored to your resource names:

```python
import json
import boto3
from datetime import datetime
# Initialize S3 client
s3 = boto3.client('s3')
def lambda_handler(event, context):
# Log the received event
print("Received event:", json.dumps(event))
# Extract name and comment from flat event
name = event.get('name', 'Unknown')
comment = event.get('comment', 'No comment')
print(f"Name: {name}, Comment: {comment}")
# Prepare data to save
data = {
'name': name,
'comment': comment,
'timestamp': datetime.utcnow().isoformat()
}
# Define S3 bucket and file key
bucket_name = 'mini-hello'
timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')
file_key = f'messages/{timestamp}-{context.aws_request_id}.json'
# Write to S3
try:
s3.put_object(
Bucket=bucket_name,
Key=file_key,
Body=json.dumps(data),
ContentType='application/json'
)
print(f"Saved to S3: s3://{bucket_name}/{file_key}")
except Exception as e:
print(f"Error saving to S3: {str(e)}")
return {
'statusCode': 500,
'headers': {
'Content-Type': 'application/json',
'Access-Control-Allow-Origin': '*'
},
'body': json.dumps({'error': 'Failed to save message'})
}
# Return success response
return {
'statusCode': 200,
'headers': {
'Content-Type': 'application/json',
'Access-Control-Allow-Origin': '*'
},
'body': json.dumps({'message': 'Message received and saved'})
}
```

## IAM Role Permissions

Ensure your Lambda role mini-world (ARN: arn:aws:iam::156041423134:role/mini-world) has permission to write to mini-hello:

### Policy

```json
{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Action": "s3:PutObject",
"Resource": "arn:aws:s3:::mini-hello/*"
}
]
}
```

### Steps

IAM > Roles > mini-world.

Attach this policy (create it under “Create policy” if not already present).

### Testing

### Deploy

Paste the code into mini-hello-formsubmissions in the Lambda console.

Click “Deploy.”

### Submit Form

Visit https://d1rbt0ac744n52.cloudfront.net.

Enter “test” and “test2,” submit.

### Logs

CloudWatch > Log Groups > /aws/lambda/mini-hello-formsubmissions.

### Expected

```text
Received event: {"name": "test", "comment": "test2"}
Name: test, Comment: test2
Saved to S3: s3://mini-hello/messages/2025-03-30-12345-<request_id>.json
```

### S3 Check

### S3 > mini-hello > messages/ > Open a file (e.g., 2025-03-30-12345-abc123.json)

```json
{"name": "test", "comment": "test2", "timestamp": "2025-03-30T12:34:56.789Z"}
```
