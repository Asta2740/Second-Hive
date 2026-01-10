# Day 4 - EC2 Networking, Security Groups, and SSH

## Summary of Yesterday’s Achievements

Here’s what you did yesterday:

Launched Two EC2 Instances:You created one Ubuntu and one Debian instance, placing them in the same subnet. This was a smart move to test connectivity between them.

Troubleshot Ping Issue:Initially, pinging between the instances didn’t work. You figured out that the security group (acting as a firewall) was blocking ICMP packets. After adding an inbound rule to allow ICMP, the pings worked perfectly. Nice troubleshooting!

Set Up SSH Access:During instance creation, you opened the SSH port (port 22) in the security groups for both instances. Using PuTTY and keypair authentication, you successfully connected to them. Your familiarity with Ubuntu and Linux made this smooth, and you were happy to see the pings working.

Explored Multiple IPs:You read about assigning a secondary IP address to an EC2 instance. You’re wondering how this interacts with load balancers and whether it’s useful for hosting multiple sites on a single server. You also questioned why you’d use this approach, which is a great sign you’re thinking critically!

**Takeaway:** You set up instances, fixed a networking issue, connected via SSH, and started exploring advanced concepts like multiple IPs—all in a day’s work. Well done!

## Notes and Clarifications

Here are some notes based on what you did, plus answers to your questions:

**Security Groups:** You nailed the security group fix by allowing ICMP for pings and SSH for access. A quick tip: security groups are stateful, so allowing inbound traffic automatically permits the related outbound traffic. This is why your pings worked once you opened the inbound rule.

### Multiple IPs on a Single Instance

What It Means: You can assign a secondary private IP (or even an Elastic IP) to an instance. Each IP can be used for a different service or website. For example, you could run two web servers on one instance, each tied to a different IP.

Use Case: This lets you host multiple sites or services on a single server without needing separate instances. It’s a way to save resources, but it’s less common now with scalable options like load balancers and containers.

Why Do It? It’s useful if you want to keep costs low and manage everything on one machine. However, if one site gets heavy traffic, the whole instance could slow down since resources are shared.

Load Balancer Interaction: Load balancers (like AWS Elastic Load Balancer) distribute traffic across multiple instances, not multiple IPs on one instance. So, if you’re using multiple IPs on a single server, a load balancer wouldn’t directly interact with that setup—it’s more for spreading load across separate machines.

Anything You Missed?You didn’t miss much yesterday! One thing to note: when you adjusted the security group, you could’ve also tested outbound rules explicitly (though it wasn’t needed here due to statefulness). Also, since you’re curious about infrastructure, you might eventually look into VPC settings (subnets, route tables), but that’s for later.

**Takeaway:** Your understanding of security groups is spot-on, and your question about multiple IPs shows you’re thinking about practical applications. Load balancers and multiple IPs serve different purposes—let’s explore that today.
