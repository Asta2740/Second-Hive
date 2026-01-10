# Day 12 - Credential Security and S3 Fundamentals

## Summary of Yesterday’s Work

Yesterday, you focused on two main areas: securing your Python script and exploring AWS S3. Here’s what you got done:

### Security Enhancements for Getmetric.py

You stored your database credentials (like DB_USER, DB_PASS, etc.) as environment variables to avoid hardcoding them in your script.

Initially, you added them to your user’s ~/.bashrc file but then switched to system-wide environment variables by editing /etc/environment.

You applied the changes and verified them, then secured the files with appropriate permissions.

### AWS S3 Exploration

You read up on AWS S3, taking detailed notes on its core concepts like buckets, objects, storage classes, security features, and common use cases.

You experimented with hosting a video on S3 and tried using pre-signed URLs for access.

Ultimately, you decided to keep the video on your EC2 instance to avoid unnecessary API calls and potential costs.

### Other Attempts

You mentioned trying something else but didn’t specify—it’s okay to skip that since it didn’t pan out. No big deal!

In short: You made your Python script more secure by using environment variables and got a solid grasp on S3, even if you didn’t fully implement it yet. That’s still valuable progress!

## Notes and Key Takeaways

Your work yesterday was solid, especially on the security front. Here are some notes, including the commands you used, to capture the highlights:

### Security Improvements

Storing credentials in environment variables is a great practice—it keeps sensitive info out of your code and reduces the risk of exposure.

### Commands Used

To apply changes to environment variables:

For user-specific variables: source ~/.bashrc

For system-wide variables: source /etc/environment

To verify variables: echo "Database User: $DB_USER"

To secure files: chmod 600 ~/.bashrc and chmod 600 /etc/environment

Important Note: Make sure your Python script is running in a context where it can access these environment variables. Since you set them system-wide, they should be available, but it’s worth double-checking with a quick print(os.environ['DB_USER']) in your script.

### AWS S3 Learning

You took detailed notes on S3’s core concepts, which is awesome for building your AWS knowledge. Here’s a quick recap of what you learned:

Buckets and Objects: Buckets store objects (files), each with a unique key.

Storage Classes: From S3 Standard for frequent access to Glacier for archiving.

Security: IAM policies, bucket policies, ACLs, and encryption options.

Integration: Works with CloudFront, Lambda, and analytics tools like Athena.

Use Cases: Static hosting, backups, data lakes, and more.

Pre-Signed URLs: You tried using them for secure, temporary access to S3 objects—smart move! Even though you didn’t end up using S3 for the video, understanding pre-signed URLs is a valuable skill for future projects.

### Decision on S3

Keeping the video on EC2 for now is a practical choice to avoid extra API calls and potential costs. You can always revisit S3 later when you’re ready to scale or need its features.

**Takeaway:** You prioritized security and expanded your AWS knowledge—both are wins, even if you didn’t check off a big task. Progress is progress!
