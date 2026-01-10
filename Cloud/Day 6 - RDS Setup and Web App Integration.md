# Day 6 - RDS Setup and Web App Integration

## Summary of Yesterday’s Achievements

You smashed it yesterday, not only revisiting RDS but also launching your first instance and building a functional web application. Here’s a breakdown of what you accomplished:

### Revisited and Mastered Amazon RDS

You started by refreshing your knowledge on RDS via the AWS RDS page and an introductory YouTube video.

You clarified what a managed database means: RDS handles the heavy lifting (backups, patching, scaling), saving developers time and hassle. You nailed the “why” behind its usefulness!

### Launched Your First RDS Instance

You created a PostgreSQL 17.2 database on the free tier, ensuring it was in the same VPC as your EC2 instance for connectivity.

You set up a new security group for the RDS instance, smartly opening only the necessary ports since it’s not public-facing.

You connected to it from your EC2 instance using:

```bash
psql -h database-1.c5u6guw48o7g.eu-central-1.rds.amazonaws.com -U postgres -d postgres
```

(After installing the PostgreSQL client, of course!)

### Built a Database and Web App

You created a simple table as planned:

```sql
CREATE TABLE entries (
id SERIAL PRIMARY KEY,
name VARCHAR(255),
quota VARCHAR(255)
);
```

Then you went above and beyond by building a PHP-based web app with Apache2 on your EC2 instance. The app lets users:

Submit a name and quota to the database.

View all entries with a delete option.

Play a video (Background.mp4) when a form is submitted—super creative!

### Hosted the Video

You considered using S3 (even created a bucket!), but since it’s a small side project, you kept the video on the EC2 instance for simplicity.

### Documented Your Work

You shared your index.php code and database connection config (dbconfig.php), which is fantastic for tracking progress. Here’s your connection setup:

```php
<?php
define('DB_HOST', 'your-rds-endpoint');
define('DB_NAME', 'your_database_name');
define('DB_USER', 'your_username');
define('DB_PASS', 'your_password');
?>
```

**Takeaway:** You didn’t just learn RDS—you applied it by launching an instance, connecting it to EC2, and building a cool web app. Your initiative to add the video and delete functionality shows you’re having fun while learning, which is the best way to grow!

## Notes and Suggestions for Improvement

Your project is already awesome, but here are some observations and ideas to make it even better—especially for index.php:

### Security Concerns

Hardcoded Credentials: Your dbconfig.php has database credentials (host, user, password) directly in the file. If someone accesses this file, they could compromise your database.

Fix: Store these in environment variables on the EC2 instance or use AWS Secrets Manager for a more secure setup.

### Example with environment variables

```php
$host = getenv('DB_HOST');
$dbname = getenv('DB_NAME');
$user = getenv('DB_USER');
$pass = getenv('DB_PASS');
$conn = pg_connect("host=$host dbname=$dbname user=$user password=$pass");
```

No Input Validation: The form accepts any input, which could lead to SQL injection or bad data.

Fix: You’re already using pg_query_params (great job!), which prevents SQL injection. Add basic checks to ensure fields aren’t empty or malformed.

### Improvements for index.php

Add Input Validation: Before inserting data, check that name and quota aren’t empty:

```php
if (empty($name) || empty($quota)) {
echo "Both name and quota are required.";
} else {
$query = "INSERT INTO entries (name, quota) VALUES ($1, $2)";
$result = pg_query_params($conn, $query, array($name, $quota));
// ... rest of your code
}
```

### Better Error Messages: Instead of “Check logs for details,” show something user-friendly

```php
if (!$conn) {
echo "Oops! Couldn’t connect to the database. Try again later.";
}
Limit Field Lengths: Match the VARCHAR(255) limit from your table:
html
<input type="text" id="name" name="name" maxlength="255" required>
<input type="text" id="quota" name="quota" maxlength="255" required>
```

Sanitize Output: You’re using htmlspecialchars for displaying entries—perfect! Keep that up to avoid XSS attacks.

### Video Hosting

Storing the video on EC2 works for now, but S3 is better for static content (faster, scalable, less load on EC2). You could revisit this later to practice S3 integration.

**Takeaway:** Your code is functional and fun, but tightening security (credentials, validation) and improving user feedback will make it more robust.
