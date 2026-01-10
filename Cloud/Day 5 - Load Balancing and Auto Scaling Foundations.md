# Day 5 - Load Balancing and Auto Scaling Foundations

## Summary of Today’s Achievements

Here’s what you accomplished today:

### Mastered Elastic Load Balancing (ELB)

You explored how ELB works and its benefits, focusing on security features like SSL/TLS termination, integrated certificate management, and client certificate authentication.

You initially thought ELB scaled by creating or terminating instances, but after digging into forums and discussions, you clarified that ELB only distributes traffic across registered instances—it doesn’t manage them.

You learned that ELB’s “automatic scaling” means it adjusts its own capacity to handle traffic changes, not the number of instances.

You created an Application Load Balancer (ALB), perfect for the Apache server you’re setting up.

### Set Up an Auto Scaling Group (ASG)

You used AWS documentation to create a launch template and an ASG, getting familiar with scaling policies like Predictive Scaling and Dynamic Scaling.

You tweaked the setup by setting the minimum instance count to 0 and adding a warm pool with one stopped instance, ensuring efficiency while keeping a backup ready.

You verified everything worked as intended, showing you’re comfortable with the hands-on process.

### Experimented with Secondary IPs

You assigned a secondary IP to your instance but, after reflecting on ELB and ASG, realized it wasn’t necessary for high availability or hosting multiple websites.

You removed it, which was a solid decision given your scalable setup.

### Customized Apache

You installed Apache on your instance, edited the default index page to add your personal touch, and documented everything—a great practice for tracking your work.

**Takeaway:** You’ve built a scalable web server setup with ALB and ASG, understood their roles, and even optimized your configuration. That’s a big win for one day!

## Notes and Clarifications

Here are some notes to solidify what you learned, with extra clarification on ELB’s security features and scaling:

### ELB’s Security Features

SSL/TLS Termination: ELB can encrypt traffic between clients and itself, then decrypt it before sending it to your instances. This offloads the encryption work from your servers, making them more efficient. You can also re-encrypt traffic to your instances if needed.

Integrated Certificate Management: ELB works with AWS Certificate Manager (ACM) to provide and renew SSL/TLS certificates for free, simplifying HTTPS setup.

Client Certificate Authentication: ELB can verify clients by checking their SSL/TLS certificates, adding security for apps where only trusted users should connect.

**Takeaway:** These features let ELB secure your app without bogging down your instances—perfect for a lightweight, scalable setup.

### ELB vs. ASG in Scaling

ELB: Automatically adjusts its capacity (not instances) to handle more or less traffic. It also monitors instance health and stops sending traffic to unhealthy ones.

ASG: Manages the number of instances—creating new ones when traffic spikes or terminating them when it drops—based on metrics like CPU usage or requests per second.

How They Work Together: ELB spreads traffic across whatever instances ASG provides. If ASG adds instances during a spike, ELB starts using them right away.

**Takeaway:** ELB handles traffic flow, ASG handles instance count—together, they make your app scale seamlessly.

### Warm Pool

Your warm pool with one stopped instance is a pre-initialized backup. When ASG needs to scale up, it can start that instance faster than launching a new one from scratch.

**Takeaway:** It’s a cost-effective way to stay ready for traffic spikes without running extra instances all the time.

### Secondary IPs

A secondary IP lets one instance handle multiple services or sites (each tied to a different IP). But with ELB distributing traffic and ASG scaling instances, you don’t need this for high availability or multiple sites—ELB can route based on domains instead.

**Takeaway:** You were right to ditch it; it’s overkill for your setup and less flexible than ELB’s routing.

### Apache

Changing the index page is a solid start! Later, you could use Apache’s virtual hosts to serve different content based on domain names, especially with ALB’s routing rules.

**Takeaway:** You’ve nailed the basics of ELB and ASG, and your instincts about secondary IPs show you’re thinking ahead. Keep it up!
