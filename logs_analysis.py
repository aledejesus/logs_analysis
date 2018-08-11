#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Full Stack Web Developer Nanodegree Project 1: Logs Analysis

Use SQL queries to answer the following questions about a
fictional newspaper website:
* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which days did more than 1% of requests lead to errors?

This script does not support command line arguments.
"""
import psycopg2


def execute_query(query):
    """
    Open db connection, execute a
    given query and close connection.

    Arguments:
        - query (str): string representing SQL query to run

    Returns:
        - list containing query results
    """
    with psycopg2.connect("dbname=news") as db:
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows


def main():
    """
    Print project's questions, call execute_query with the queries
    used to answer each question and print the results.

    No arguments nor return values.
    """
    # Question 1
    print "* What are the most popular three articles of all time?"
    results = execute_query("""
        SELECT art.title, COUNT(log.path) AS views
        FROM articles AS art
        JOIN log ON log.path LIKE ('/article/' || art.slug)
        GROUP BY art.title ORDER BY views DESC LIMIT 3;""")
    for title, views in results:
        print "\"%s\" – %s views" % (title, views)
    print ""

    # Question 2
    print "* Who are the most popular article authors of all time?"
    results = execute_query("""
        SELECT aut.name, COUNT(log.path) AS views FROM authors AS aut
        JOIN articles AS art ON aut.id=art.author
        JOIN log ON log.path LIKE ('/article/' || art.slug)
        GROUP BY aut.name ORDER BY views DESC;""")
    for name, views in results:
        print "%s – %s views" % (name, views)
    print ""

    # Question 3
    print "* On which days did more than 1% of requests lead to errors?"
    results = execute_query("""
        SELECT
            TO_CHAR(day, 'FMMonth DD, YYYY'),
            TO_CHAR(error_percent, 'FM999.99')
        FROM(
            SELECT
                daily_requests.day,
                ((daily_errors.cnt::float / daily_requests.cnt) * 100)
                    AS error_percent
            FROM daily_requests  -- database view
            JOIN daily_errors  -- database view
            ON daily_requests.day=daily_errors.day) AS errors_per_day
        WHERE error_percent>1.0
        ORDER BY error_percent DESC;""")

    for day, error_percent in results:
        print "%s – %s%% errors" % (day, error_percent)
    print ""


main()
