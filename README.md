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

### Repository & Environment Configuration

To ensure production security and clean version control:

A .gitignore file was created to exclude:
db.sqlite3 (local development database)
Virtual environment directories (.venv/)
__pycache__/ files
Environment configuration files (env.py, .env)
Sensitive data such as SECRET_KEY is stored in Heroku environment variables.
DEBUG is set to False in production.
PostgreSQL is used in production via DATABASE_URL.
SQLite is used locally for development only.

This prevents:

Accidental credential leaks
Committing local database files
Deployment inconsistencies

------------------------------------------------

Phase 2 – Custom Models & Ownership Architecture

Custom Data Models
Two relational models were implemented to satisfy the custom model requirement:

TodoList Model

owner → ForeignKey to User (required, CASCADE)
name → CharField
created_on → DateTimeField (auto_now_add)
updated_on → DateTimeField (auto_now)

Task Model

todo_list → ForeignKey to TodoList (CASCADE)
title → CharField
description → Optional TextField
completed → BooleanField (default=False)
due_date → Optional DateField
created_on → DateTimeField
updated_on → DateTimeField

This establishes a relational hierarchy:

User → TodoList → Task

Ownership & Authorisation Strategy
Authorisation is enforced at multiple levels:

All list views use LoginRequiredMixin
Querysets filter strictly by owner=request.user
List creation assigns owner=request.user server-side
URL-level access uses get_object_or_404(..., owner=request.user)
Tasks are scoped via todo_list__owner=request.user

This prevents:

Accessing another user’s data via URL manipulation
Spoofing ownership via POST requests
Orphaned records

Non-authorised access returns HTTP 404 to avoid leaking object existence.

Relational Integrity Decisions
on_delete=models.CASCADE used for:
List → User
Task → TodoList

This ensures:

No orphaned tasks
No orphaned lists
Referential integrity maintained in PostgreSQL

Manual Testing (Phase 2)
Tested locally and in production:

Logged-out users redirected to login
Logged-in users see only their own lists
Users cannot access another user's list via direct URL
List creation assigns correct owner
Production migrations applied successfully in Heroku Postgres

Result: Authorisation requirement satisfied.

----------------

## Phase 2 — Step 7: List Detail + URL Ownership Enforcement

Added list detail route: /lists/<int:pk>/
Implemented TodoListDetailView with LoginRequiredMixin
Enforced ownership in get_object() using get_object_or_404(TodoList, pk=..., owner=request.user) so URL manipulation returns 404
Updated list index to link to list detail pages
Added minimal list_detail.html template (foundation for Task CRUD)

Manual tests:

Logged-out users redirected to login
User B cannot access User A’s list by direct URL (404)