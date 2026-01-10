# Day 7 - CloudWatch Agent Setup and Certification Kickoff

## Summary of Today’s Achievements

### CloudWatch Deep Dive

What You Learned:You read the CloudWatch overview and grasped its core functions: monitoring applications, responding to performance changes, and providing health insights through visualization, automation, and integration with AWS services.

### Hands-On Work

You explored the CloudWatch console and realized default metrics don’t include storage, so you researched and found the CloudWatch agent is needed.

You successfully:

### Downloaded the Agent

wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb

### Installed It

sudo dpkg -i amazon-cloudwatch-agent.deb

### Ran the Config Wizard

sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard

You customized the config file to monitor storage (changing the wildcard * to your specific needs).

### Started the Agent

sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:(config file location) -s

### Verified It Was Running

sudo systemctl status amazon-cloudwatch-agent

You checked logs at /opt/aws/amazon-cloudwatch-agent/logs/ for troubleshooting.

IAM Setup: Attached the CloudWatchAgentServerPolicy to your EC2 instance’s IAM role.

Created an Alarm: Set up a storage alarm in CloudWatch, debugged config issues, and got it working.

**Takeaway:** You didn’t just follow steps—you problem-solved like a pro, which is a key skill for AWS work!

**Note:** if you changed something on your config we need to fetch them again

sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json -s

and to check logs

tail -f /opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log

### Cloud Practitioner Enrollment

You enrolled in the Cloud Practitioner course and completed the “Job Roles in the Cloud” module.

**Takeaway:** It’s great to see your initiative in starting certification prep early, giving you a taste of what’s ahead.

Overall: You made strong technical progress with CloudWatch and took a proactive step toward certification. Awesome work!

## Notes and What You Might Have Missed

### CloudWatch

Additional Metrics: You nailed storage monitoring, but CloudWatch can also track default metrics like CPU usage and network traffic without extra config. Since your agent is set up, you could add memory monitoring too (it’s not default either).

**Pro Tip:** Try creating a CloudWatch dashboard to visualize your metrics—it’s an easy way to see your instance’s health at a glance.

IAM Role Note: The CloudWatchAgentServerPolicy was the right move. For future tasks, if you use Systems Manager (SSM), you might need AmazonEC2RoleforSSM too.

Config Updates: You already know to re-fetch the config after changes (nice catch!), so keep that habit—it’ll save you headaches.

### Cloud Practitioner Detour

Starting the certification is a solid move, but the original plan was to focus on hands-on skills first. This foundation will make the certification content feel like a review later.

Suggestion: Limit certification study to 30-60 minutes daily for now, so you can keep your main focus on practical tasks.

**Takeaway:** You’re doing great, but balancing hands-on work with certification prep will help you stay on track without feeling swamped.
