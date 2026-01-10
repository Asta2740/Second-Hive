# Day 2 - EC2 Fundamentals and First Instance Launch

## Summary of Day 2: Achievements

You successfully completed your tasks for Day 2, gaining a solid grasp of EC2 and its role in cloud infrastructure. Here’s what you accomplished:

### Watched Two EC2 Videos

The first video (link) explained the importance of EC2, showing how it replaces on-site servers and enables cloud-based services with low latency.

The second video (link) provided a hands-on demo of launching an EC2 instance, which you followed to launch your own instance.

### Key Learnings

EC2 acts as virtual servers in the cloud, allowing you to build and scale applications without physical hardware.

### Steps to launch an EC2 instance include

Choosing an AMI (predefined or custom templates with OS and software).

Selecting an instance type (e.g., compute-optimized, memory-optimized, general-purpose).

Configuring network settings (VPC, security groups for firewall rules).

Adding storage (EBS volumes, like virtual hard drives).

Using tags (e.g., "Name: MyServer") to organize and identify instances.

You learned there are two types of AMIs: predefined (provided by AWS, tweakable) and custom (user-created).

### Hands-On Experience

You launched your first EC2 instance—a major milestone!

You noted that you focused more on the demo than exploring the AWS Management Console, so you’ll revisit that tomorrow to get more comfortable with the dashboard.

**Takeaway:** You now understand EC2’s role as the “servers of the cloud” and have hands-on experience launching an instance. Awesome work!

## Notes from Day 2

Here are the key points and clarifications based on what you learned and asked:

### EC2 Overview

EC2 provides virtual servers (instances) that replace traditional on-site servers, offering scalability and flexibility.

It’s ideal for running applications, hosting websites, and more, with low latency thanks to AWS’s global infrastructure.

### AMI (Amazon Machine Image)

AMIs are templates for EC2 instances, containing the operating system and software.

Predefined AMIs are provided by AWS (e.g., Amazon Linux, Ubuntu) and can be customized.

### Custom AMIs are ones you create yourself. Here’s how

Launch an instance from a predefined AMI.

Customize it (e.g., install software, tweak settings).

Save it as a new AMI using the AWS Console or CLI (under “Actions” > “Create Image”).

No ISO Upload Needed: You don’t upload an ISO file; you modify an existing instance and save it as a custom AMI.

**Tip:** Rewatch the last 10 minutes of the second video or check AWS’s AMI guide for a step-by-step breakdown.

### Instance Types

### Choose based on your workload

General-purpose (e.g., t2.micro, great for free tier).

Compute-optimized (for CPU-heavy tasks like data processing).

Memory-optimized (for large datasets).

GPU instances (for graphics or AI workloads).

### Billing and Free Tier

### Free Tier Limits

You get 750 hours/month of t2.micro (or t3.micro) instances for your first 12 months with AWS.

This means you can run one t2.micro instance 24/7 (since 750 hours ≈ 31 days) or multiple instances as long as the total hours don’t exceed 750.

### Notifications

AWS won’t automatically notify you before charges kick in, but you can set up budget alerts.

Go to AWS Budgets in the console, create a budget, and set an alert (e.g., email when you near 750 hours or a cost threshold).

**Tip:** Always select the “Free Tier” option when launching instances to stay within limits, and double-check your usage in the Billing Dashboard.

### EC2 Configuration

**Networking:** Set up a VPC and security groups (firewall rules) to control who accesses your instance.

**Storage:** Attach EBS volumes for persistent storage (think of them as virtual hard drives).

**Tags:** Add key-value pairs (e.g., "Purpose: Testing") to keep track of instances.

### Hands-On Demo

You launched an instance but didn’t fully explore the console. No worries—tomorrow’s tasks will help you get familiar with it.

**Takeaway:** You’ve got a strong start with EC2. Understanding custom AMIs and setting up billing alerts will give you more confidence moving forward.
