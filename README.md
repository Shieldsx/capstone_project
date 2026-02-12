# Django To-Do List
This is my capstone project. It is a to-do list.

The deployment pipeline was configured before development began to ensure continuous deployment and prevent late-stage configuration issues.
Setup Instructions
1. Repository & Project Initialisation

Created a GitHub repository named capstone_project

Connected the local workspace to the GitHub repository

Created a GitHub Project (Kanban board) and added all user stories as issues

Applied labels for Epics, Type, and Priority

2. Heroku Setup (Early Deployment Strategy)

Installed the Heroku CLI

Logged in via terminal

Created Heroku app:

capstone-project-f


Confirmed Heroku remote was added to local repository

Set initial environment variables in Heroku:

SECRET_KEY (temporary placeholder)

DEBUG=False

This ensures deployment configuration is established before development begins.

3. Runtime Configuration

Created runtime.txt

Specified Python version to ensure consistency between local and production environments.


