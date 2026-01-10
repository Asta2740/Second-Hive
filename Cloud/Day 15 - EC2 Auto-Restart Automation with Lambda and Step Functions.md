# Day 15 - EC2 Auto-Restart Automation with Lambda and Step Functions

## Key Points

You made significant progress yesterday by setting up an automated system to restart your EC2 instance when CPU utilization is high, using AWS Lambda and Step Functions.

You created three Lambda functions (StopEC2Instances, StartEC2Instances, CheckEC2Instances) and a Step Function to orchestrate them, ensuring the instance is fully stopped before starting again.

You also set up a StateMachineTrigger Lambda function to start the Step Function when a CloudWatch alarm triggers, linked to CPU utilization exceeding 80% for 5 minutes.

The system works, but there are opportunities to improve, like making the instance ID dynamic and optimizing wait times in the Step Function.

## Background

Yesterday, you focused on automating the restart of your EC2 instance using AWS Lambda and Step Functions, a task that builds on your previous work with CloudWatch and EC2 monitoring. This is part of your broader goal to enhance infrastructure engineering skills, particularly in automation, which aligns with Phase 3 of your roadmap.

## Detailed Steps

IAM Policy and Role: You created an IAM policy with minimal permissions for Lambda to interact with CloudWatch Logs and EC2, then attached it to an IAM role. This ensures security by following the principle of least privilege.

### Lambda Functions: You developed three functions

StopEC2Instances: Stops the EC2 instance.

StartEC2Instances: Starts the EC2 instance.

CheckEC2Instances: Checks the instance state to ensure it’s stopped before starting.

Step Function: You designed a state machine to sequence these functions, waiting 60 seconds between checks to ensure the instance reaches the desired state (stopped before starting).

StateMachineTrigger: Created a Lambda function to trigger the Step Function when a CloudWatch alarm fires, passing the instance ID dynamically from the alarm event.

Testing: You tested the setup, confirming the EC2 instance restarts correctly when CPU utilization is high.

### Unexpected Detail

An unexpected aspect is how you used Step Functions to handle the sequential nature of stopping and starting, which is more robust than a single Lambda function that might time out, especially given Lambda’s 15-minute execution limit.

## Survey Note: Comprehensive Analysis of Yesterday’s Work and Today’s Agenda

### Introduction

Yesterday, you made significant strides in automating the restart of your EC2 instance based on high CPU utilization, leveraging AWS Lambda and Step Functions. This task is a critical component of your infrastructure engineering journey, particularly in Phase 3 of your roadmap, which focuses on automation and containerization. Your work demonstrates a deep dive into serverless computing and orchestration, aligning with your goal to transition into infrastructure and eventually security engineering. Below, we detail your achievements, provide notes for improvement, and outline today’s agenda to keep your progress on track.

## Detailed Summary of Yesterday’s Work

Your focus was on creating an automated system to restart your EC2 instance when CPU utilization exceeds 80% for 5 minutes, using a combination of Lambda functions and Step Functions. Here’s a breakdown of your steps:

### IAM Policy and Role Creation

You began by creating an IAM policy to grant the necessary permissions for Lambda functions to interact with CloudWatch Logs and EC2. The policy, adhering to the principle of least privilege, included actions like logs:CreateLogGroup, logs:CreateLogStream, logs:PutLogEvents, ec2:Start*, ec2:Stop*, and ec2:DescribeInstances. This was attached to an IAM role, ensuring secure access control.

### Lambda Function Development

You developed three Lambda functions, each with a specific purpose:

### StopEC2Instances: This function stops the specified EC2 instance. Here’s the code

```python
import boto3
ec2_client = boto3.client('ec2')
def lambda_handler(event, context):
instance_id = event['instance_id']
try:
response = ec2_client.stop_instances(InstanceIds=[instance_id])
current_state = response['StoppingInstances'][0]['CurrentState']['Name']
previous_state = response['StoppingInstances'][0]['PreviousState']['Name']
return {
'status': 'stopping' if current_state == 'stopping' else current_state,
'instance_id': instance_id,
'previous_state': previous_state
}
except Exception as e:
return {'error': str(e)}
```

### StartEC2Instances: This function starts the EC2 instance, with similar error handling

```python
import boto3
ec2_client = boto3.client('ec2')
def lambda_handler(event, context):
instance_id = event['instance_id']
try:
response = ec2_client.start_instances(InstanceIds=[instance_id])
current_state = response['StartingInstances'][0]['CurrentState']['Name']
previous_state = response['StartingInstances'][0]['PreviousState']['Name']
return {
'status': 'starting' if current_state == 'pending' else current_state,
'instance_id': instance_id,
'previous_state': previous_state
}
except Exception as e:
return {'error': str(e)}
```

### CheckEC2Instances: This function checks the instance state, ensuring it’s stopped before starting

```python
import boto3
ec2_client = boto3.client('ec2')
def lambda_handler(event, context):
instance_id = event['instance_id']
try:
response = ec2_client.describe_instances(InstanceIds=[instance_id])
if not response['Reservations']:
return {'error': 'instance not found'}
state = response['Reservations'][0]['Instances'][0]['State']['Name']
return {'status': state, 'instance_id': instance_id}
except Exception as e:
return {'error': str(e)}
```

### Step Function Orchestration

You created a Step Function to sequence these operations, ensuring the instance is fully stopped before starting. The state machine definition is:

```json
{
"Comment": "Restart EC2 Instance based on Alarm",
"StartAt": "StopEC2",
"States": {
"StopEC2": {
"Type": "Task",
"Resource": "arn:aws:lambda:eu-central-1:156041423134:function:StopEC2Instances:$LATEST",
"Next": "WaitForStopped"
},
"WaitForStopped": {
"Type": "Wait",
"Seconds": 60,
"Next": "CheckIfStopped"
},
"CheckIfStopped": {
"Type": "Task",
"Resource": "arn:aws:lambda:eu-central-1:156041423134:function:CheckEC2Instances:$LATEST",
"Next": "IsStopped"
},
"IsStopped": {
"Type": "Choice",
"Choices": [
{
"Variable": "$.status",
"StringEquals": "stopped",
"Next": "StartEC2"
}
],
"Default": "WaitForStopped"
},
"StartEC2": {
"Type": "Task",
"Resource": "arn:aws:lambda:eu-central-1:156041423134:function:StartEC2Instances:$LATEST",
"Next": "WaitForRunning"
},
"WaitForRunning": {
"Type": "Wait",
"Seconds": 60,
"Next": "CheckIfRunning"
},
"CheckIfRunning": {
"Type": "Task",
"Resource": "arn:aws:lambda:eu-central-1:156041423134:function:CheckEC2Instances:$LATEST",
"Next": "IsRunning"
},
"IsRunning": {
"Type": "Choice",
"Choices": [
{
"Variable": "$.status",
"StringEquals": "running",
"Next": "Success"
}
],
"Default": "WaitForRunning"
},
"Success": {
"Type": "Succeed"
}
}
}
```

You tested this, and it successfully simulated the EC2 restart.

### StateMachineTrigger Lambda Function

You created a Lambda function to trigger the Step Function when a CloudWatch alarm fires, extracting the instance ID from the alarm event:

```python
import json
import boto3
step_function_arn = "arn:aws:states:eu-central-1:156041423134:stateMachine:MyStateMachine-MachineRestartflow"
client = boto3.client("stepfunctions")
def lambda_handler(event, context):
instance_id = event['Trigger']['Dimensions'].get('InstanceId')
if not instance_id:
return {
"statusCode": 400,
"body": json.dumps({"error": "Instance ID not found in alarm dimensions."})
}
response = client.start_execution(
stateMachineArn=step_function_arn,
input=json.dumps({"instance_id": instance_id})
)
return {
"statusCode": 200,
"body": json.dumps(response, default=str)
}
```

You also created an IAM policy for this function to start Step Function executions and attached it to the role:

```json
{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Action": "states:StartExecution",
"Resource": "arn:aws:states:eu-central-1:156041423134:stateMachine:MyStateMachine-MachineRestartflow"
}
]
}
```

Finally, you linked this to a CloudWatch alarm for CPU utilization > 80% over 5 minutes.

## Notes and Improvements

Your setup is robust, but here are some notes and potential improvements:

Dynamic Instance ID: You made the instance ID dynamic by passing it through the event, which is a significant improvement over hardcoding. This makes your system scalable for multiple instances.

Wait Times in Step Function: The 60-second waits might be inefficient if the instance stops or starts faster. Consider reducing to 30 seconds and adding retries for better efficiency, balancing cost (more Lambda invocations) and speed.

Error Handling: Your Lambda functions have basic error handling, which is good. Consider adding more specific error messages and logging to CloudWatch for debugging.

Security: Ensure the IAM role has the least privileges (e.g., limit ec2:DescribeInstances to specific instances if possible). Your current policy allows actions on all EC2 resources, which could be tightened.

Testing: Always test in a non-production environment to avoid downtime. Consider simulating high CPU and verifying the restart process.

Cost Consideration: Each Lambda invocation and Step Function execution incurs costs, so monitor usage, especially with frequent checks.
