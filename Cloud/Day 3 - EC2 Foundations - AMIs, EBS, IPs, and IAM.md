# Day 3 - EC2 Foundations: AMIs, EBS, IPs, and IAM

## Summary of Day 3: Achievements

Despite your limited time, you covered a lot of ground on Day 3. Here’s what you learned and did:

Custom AMI Creation:You understand the basics of creating a custom AMI but feel you need more clarity. A custom AMI is made by launching an instance, customizing it (e.g., installing software), and saving it as a new AMI via the AWS Console (“Actions” > “Create Image”). No ISO upload is needed—you modify an existing instance and save its state.

Elastic Block Storage (EBS):You learned that EBS is like a virtual hard drive for EC2 instances. You also explored EBS snapshots (point-in-time backups) and the lifecycle manager, which automates snapshot creation and cross-account copying. The lifecycle manager helps set up backup schedules and retention policies, but you might want to dig deeper into how it works.

Multiple IP Addresses:You mentioned hosting multiple websites on a single server and tied it to routing tables. Let’s clarify:

Multiple IP Addresses: You can assign multiple Elastic IPs or secondary private IPs to a single EC2 instance. This lets one instance host multiple websites, each linked to a different IP.

Routing Tables: These are part of VPC networking and direct traffic between subnets, not directly related to hosting multiple websites on one instance.Takeaway: For multiple websites, focus on assigning multiple IPs to the instance, not routing tables. We’ll revisit this today.

**Elastic IP:** You grasped the concept of Elastic IPs (static public IPs) and how to assign them. You’re on the right track—later, you can practice associating one with your instance.

**Security Groups:** You understood that security groups act as virtual firewalls, controlling inbound and outbound traffic. You saw how to configure rules (e.g., allowing port 80 for HTTP), which is a great start.

Key Pairs:You correctly interpreted key pairs as public-key encryption for secure SSH access. The private key (.pem file) is yours to keep, while AWS stores the public key.

IAM (Identity and Access Management):You enabled IAM for your instance, even though you’re the only user. IAM manages who can access what in your AWS account (e.g., users, roles, permissions). For now, your root account is enough, but exploring IAM is smart for future multi-user setups.

Budget Creation:You set up a zero-spend budget to stay within the free tier. AWS will alert you if usage nears your limits, keeping costs in check.

EC2 Instance Creation:You launched a new EC2 instance and booted it but didn’t have time to test it fully. This is a big win—we’ll build on it today!

**Takeaway:** You packed a lot into an hour—great work! Your proactive steps, like setting a budget, show you’re thinking ahead.

## Notes from Day 3

Here are the key points and clarifications from your Day 3 learning:

### Custom AMI Creation

Start with a predefined AMI, customize the instance, then save it as a new AMI.

No ISO upload required; it’s all done within AWS.

### EBS and Snapshots

EBS = virtual hard drives for EC2.

Snapshots = backups of EBS volumes.

Lifecycle manager automates snapshot creation and management (e.g., scheduling backups).

### Multiple IP Addresses vs. Routing Tables

Multiple IPs: Assign multiple Elastic IPs or secondary private IPs to one instance for hosting multiple websites.

Routing Tables: Control traffic flow between VPC subnets, not for hosting websites on a single instance.

### Elastic IP

A static public IP you can assign to instances for consistent access.

### Security Groups

Virtual firewalls; configure rules to control traffic (e.g., allow HTTP on port 80).

### Key Pairs

Used for secure SSH access; you keep the private key, AWS holds the public key.

### IAM

Manages access to AWS resources (users, permissions). Optional for solo use but good to learn.

### Budget

Zero-spend budget set to monitor free tier usage and avoid charges.

**Takeaway:** You’ve built a solid conceptual base. Now, let’s get hands-on with your EC2 instance.
