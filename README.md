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

Initial placeholder route returning HTTP response.

----------------

## Authentication Configuration (django-allauth)

Django-allauth was installed and configured to handle user authentication.

The following configuration steps were completed:

- Added `django.contrib.sites` to INSTALLED_APPS
- Added:
    - allauth
    - allauth.account
    - allauth.socialaccount
- Configured AUTHENTICATION_BACKENDS to include Allauth backend
- Set SITE_ID = 1
- Created project-level templates directory
- Added `django.template.context_processors.request` (required by allauth)
- Configured login and logout redirect URLs
- Set minimal account settings for MVP:
    - Email required
    - Username required
    - Email verification disabled (MVP scope)

This prepares the project for implementing Register, Login, Logout, and Account Management functionality in Phase 1.

After realizing my secret was hardcoded in my settings.py file I moved SECRET_KEY to env var; rotated after accidental exposure.

----------------

## Middleware & URL Wiring

After configuring django-allauth in settings.py, the authentication system was fully wired into the project:
Added allauth.account.middleware.AccountMiddleware to MIDDLEWARE
Included path("accounts/", include("allauth.urls")) in todo_project/urls.py
Confirmed SITE_ID = 1 and updated local Site record for development

Verified all required migrations for:

account
auth
sessions
sites
socialaccount

This ensured the authentication routes were active and functional.

--------

Template Scaffold (Authentication Phase)

To establish a consistent UI foundation:

Created a project-level templates/ directory
Created base.html as the shared layout
Created templates/todo/home.html
Updated home view to render todo/home.html
Confirmed navigation conditionally displays:
Login / Register (anonymous users)
Logout + Account links (authenticated users)

This establishes the base layout for Phase 1 before introducing List and Task models.

-------

Local & Production Alignment

Confirmed authentication routes work locally:

/accounts/login/
/accounts/signup/
/accounts/password/reset/
Verified application deploys successfully on Heroku
Confirmed Gunicorn boots correctly with no startup errors
Maintained environment variable configuration for SECRET_KEY
Rotated exposed secret key and removed hardcoded value from codebase

-----------

Authentication — Production Verification (Heroku)
Manual production testing completed on Heroku to confirm the Phase 1 authentication scaffold is working end-to-end.

Tests performed (Production):

Home page loads successfully (/)
Signup works (/accounts/signup/)
User is automatically logged in after signup
Redirect to home (/) confirmed
Authenticated navigation displays account actions (Update Email / Change Password / Logout)
No email verification required (MVP setting)
No debug traceback visible in production (DEBUG=False)

Result: Pass (Phase 1 complete)


Development Phases
Phase 1: Authentication scaffold + production verification (Complete)
Phase 2: Custom models (List, Task) + ownership + CRUD
Phase 3: UX polish (messages, confirmations), testing, README finalisation, AI reflection

----------
## Production Database Setup (Heroku Postgres)

During deployment verification, the app was initially found to be using SQLite in production (`/app/db.sqlite3`) despite `DATABASE_URL` being set. This would not meet the requirement for PostgreSQL in production.

### Fix: DATABASES configuration
`settings.py` was updated so that:
- In production (when `DATABASE_URL` exists), Django uses PostgreSQL via `dj_database_url`
- In local development (when `DATABASE_URL` is not set), Django falls back to SQLite

Production database usage was verified on Heroku using Django shell (`connection.vendor == "postgresql"`).

### Heroku Postgres provisioning
A Heroku Postgres add-on was attached to the app:

- Plan: `heroku-postgresql:essential-0`

Provisioning was confirmed using:
- `heroku addons:info ...`
- `heroku pg:wait`
- `heroku pg:info`
- `heroku config:get DATABASE_URL`

### Production migrations + admin verification
After attaching Postgres:
- Production migrations were applied (`python manage.py migrate`)
- A production superuser was created (`python manage.py createsuperuser`)
- Admin login was confirmed via `/admin/`