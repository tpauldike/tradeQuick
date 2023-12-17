Quick Guide

    git pull from this branch to have the latest changes made.
    Make sure your mysql server is started.
    Check status to make sure it is running.
    create database and tables with the tradequick.sql by running cat tradequick.sql | sudo mysql -u -p replace user with your mysql user and password once the prompt pops up.
    verify that the database and tables are created.
    Use testrunner.py file to add mock data to the db tables(user, likes, comments, etc) by adding the required parameters and making the neccessary imports. This is to make sure our tables are getting the information it was suppose to.
