# Full Stack Web Developer Nanodegree
## Project 1: Logs Analysis
### Description
Access logs of a fictional newspaper website want to be analyzed in order to answer some questions about the site's traffic. These logs are in a PostgreSQL database so SQL queries are used to achieve this purpose. The questions that the script answers are:
* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which days did more than 1% of requests lead to errors?

### Design
The logs_analysis.py script uses python library psycopg2 to interact with the PostgreSQL database from which data wants to be analyzed. Code consists of 2 functions:
* **execute_query:** helper function that takes care of opening and closing database connection and executing a given query.
* **main:** function in which questions about the log are printed to the console, queries are executed using the execute_query helper function and results are printed to the console.

### How to run?
In a terminal window type:
`python2.7 logs_analysis.py`

### Database view definitions
The code relies on the daily_requests and daily_errors views defined on the database. The SQL used to define
these was:
```
-- daily_requests view definition
CREATE VIEW daily_requests AS
SELECT DATE(time) AS day, COUNT(id) AS cnt
FROM log GROUP BY day;

-- daily_errors view definition
CREATE VIEW daily_errors AS
SELECT DATE(time) AS day, COUNT(id) AS cnt
FROM log WHERE status='404 NOT FOUND' GROUP BY day;
```