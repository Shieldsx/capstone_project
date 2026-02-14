# Capstone Project – To-Do List Application

This is my Full Stack Django capstone project.
It is a minimal, mobile-first to-do list application built using Django and PostgreSQL, deployed on Heroku.

Deployment-First Development Strategy

The deployment pipeline was configured before development began to ensure:

Continuous deployment

Early detection of configuration issues

Production-ready environment setup from the start

Avoidance of late-stage deployment failures

This approach aligns with Agile principles and project planning best practices.

Setup Instructions
1. Repository & Project Initialisation

Created a GitHub repository named capstone_project

Connected the local workspace to the GitHub repository

Created a GitHub Project (Kanban board)

Added all Epics and User Stories as GitHub Issues

Applied structured labels:

Epic labels

Type labels

Priority labels

This satisfies Agile planning requirements (LO1).

2. Heroku Setup (Early Deployment Strategy)

Installed the Heroku CLI

Logged in via terminal

Created Heroku app:

capstone-todo-f


Linked local repository to Heroku remote

Set initial environment variables in Heroku:

SECRET_KEY

DEBUG=False

This ensures production configuration exists before application development begins.

3. Virtual Environment & Dependencies

Created Python virtual environment:

python -m venv .venv


Activated environment

Installed required packages:

Django

Gunicorn

dj-database-url

psycopg2-binary

WhiteNoise

django-allauth

Generated requirements.txt using:

pip freeze > requirements.txt


This ensures dependency consistency between local and production environments.

4. Runtime Configuration

Created runtime.txt

Specified Python version for Heroku compatibility

This ensures consistent Python runtime between environments.

5. Django Project Scaffold

Created Django project:

django-admin startproject todo_project .


Created Django app:

python manage.py startapp todo


Created Procfile for Heroku deployment:

web: gunicorn todo_project.wsgi


Note: The Procfile required correct capitalisation (Procfile) to be recognised by Heroku.

6. Static File Configuration for Production

To resolve Heroku deployment errors:

Added STATIC_ROOT in settings

Configured WhiteNoise middleware

Added production static storage configuration

Created root-level static/ directory

This resolved the collectstatic build failure.

7. Production Security Configuration

Updated ALLOWED_HOSTS to include Heroku domain

Converted DEBUG to environment-based configuration:

DEBUG = os.environ.get("DEBUG", "False") == "True"


This resolved the DisallowedHost error and ensures secure production settings.

Current Deployment Status

Web dyno running successfully

Gunicorn serving Django

Application accessible via Heroku URL

Initial placeholder route returning HTTP response


