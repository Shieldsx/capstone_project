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

## Phase 2 – Custom Models & Ownership Architecture

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

## Phase 2: List Detail + URL Ownership Enforcement

Added list detail route: /lists/<int:pk>/
Implemented TodoListDetailView with LoginRequiredMixin
Enforced ownership in get_object() using get_object_or_404(TodoList, pk=..., owner=request.user) so URL manipulation returns 404
Updated list index to link to list detail pages
Added minimal list_detail.html template (foundation for Task CRUD)

Manual tests:

Logged-out users redirected to login
User B cannot access User A’s list by direct URL (404)

----------------

## Phase 2: Nested Task Creation (Ownership Inherited from Parent)

A nested route was implemented to allow task creation within a specific list:
/lists/<int:pk>/tasks/new/

Architecture Decisions

Implemented TaskCreateView using LoginRequiredMixin
Parent TodoList resolved using:
get_object_or_404(TodoList, pk=..., owner=request.user)

The todo_list foreign key is not exposed in the form
The parent list is assigned server-side in form_valid()
Redirects back to the parent list detail page on success

This ensures:

Users cannot create tasks inside another user's list
Foreign key tampering via POST manipulation is prevented
Tasks inherit ownership implicitly via their parent list
URL manipulation returns HTTP 404

Template Integration

Updated list_detail.html to:
Display tasks using todo_list.tasks.all
Provide a "+ Add Task" link scoped to the current list
Used related_name="tasks" on the Task foreign key for clean reverse querying

Manual Testing

Tested locally and in production:
Logged-in users can create tasks inside their own list
Tasks display correctly under the parent list
Logged-out users are redirected to login
Attempting to access /lists/<other_user_pk>/tasks/new/ returns 404
Foreign key cannot be overridden via form tampering

Result: Nested Task creation implemented with strict ownership enforcement.

---------------------

## Phase 2: Task Update & Delete

Added nested task edit and delete routes:
/lists/<list_pk>/tasks/<task_pk>/edit/
/lists/<list_pk>/tasks/<task_pk>/delete/

Implemented TaskUpdateView and TaskDeleteView with strict ownership enforcement using:
get_object_or_404(Task, pk=task_pk, todo_list__pk=list_pk, todo_list__owner=request.user)
Prevented FK reassignment by excluding todo_list from forms and enforcing parent list linkage in object retrieval.

Manual testing confirmed (local + production):
Owners can edit/delete their own tasks
Logged-out users are redirected to login
Cross-user URL manipulation returns 404

-----------------------

## Phase 2 – Step 10: UX & Messages

Implemented Django messages framework for CRUD feedback.
Centralised message display in base.html to ensure consistent global rendering.
Added success messages for list and task create, update, and delete actions.
Removed duplicate template message blocks to prevent repeated output.
Manually tested locally and in production.

----------------

## End of Phase 2 Manual Testing

Manual Testing

All core functionality was manually tested in both local development and the deployed Heroku environment.

CRUD & UX Manual Tests (Lists + Tasks)
| Feature | Test Case | Steps | Expected Result | Pass |
|---------|-----------|-------|----------------|------|
| List – Create | Create a new list as logged-in user | Login → “New List” → enter name → Save | List created; success message shown; list appears in “Your lists” | ✅ |
| List – Read | View list detail page | From “Your lists” click a list | List detail loads; only that list’s tasks displayed | ✅ |
| List – Delete | Delete existing list | Open list → Delete → confirm | List removed; success message shown; cannot access list URL after deletion (404) | ✅ |
| Task – Create | Create a task inside a list | Open list → “Add task” → fill fields → Save | Task added under correct list; success message shown | ✅ |
| Task – Update | Edit a task | Open list → Edit task → change fields → Save | Task updates; success message shown | ✅ |
| Task – Mark Complete | Toggle completed flag | Edit task → set Completed true → Save (or checkbox, if used) | Task shows as completed and persists on refresh | ✅ |
| Task – Delete | Delete a task | Open list → Delete task → confirm | Task removed; success message shown; task URL no longer accessible (404) | ✅ |
| Messages | Messages render consistently | Perform create/update/delete actions | Success messages appear once and do not persist incorrectly across pages | ✅ |
| Logged-out protection | Redirect when not authenticated | Logout → visit /lists/ and a list detail URL directly | Redirected to login; no data leaked | ✅ |

------------------------

Authorisation & Security Manual Tests

| Security Area | Test Case | Steps | Expected Result | Pass |
|---------------|-----------|-------|----------------|------|
| List ownership | Another user cannot view your list | Login as User A → copy list URL → logout → login as User B → paste URL | 404, not permission denied | ✅ |
| List ownership | Another user cannot delete your list | As User B attempt list delete URL for User A’s list | 404; list remains for User A | ✅ |
| Task ownership (nested) | Another user cannot edit your task | As User B attempt task edit URL with User A list_pk + task_pk | 404; no task data exposed | ✅ |
| Task ownership (nested) | Another user cannot delete your task | As User B attempt task delete URL with User A list_pk + task_pk | 404; task remains for User A | ✅ |
| Nested integrity | Task cannot be accessed outside its parent list | Try mismatched list_pk with valid task_pk | 404; prevents cross-list ID enumeration | ✅ |
| Authentication required | Protected views require login | Logout → attempt list create/task create/edit/delete URLs | Redirect to login; no server error | ✅ |

----------------------

## Phase 3

Authorisation & Security Implementation

The application enforces strict authentication and object-level ownership controls to prevent unauthorised access.

Authentication

All list and task views are protected using LoginRequiredMixin.
Unauthenticated users attempting to access protected routes are redirected to the login page.
No list or task data is accessible without authentication.

Object-Level Authorisation
Ownership is enforced at the queryset level:

TodoList querysets are filtered using:

owner=request.user

List detail views use get_object_or_404() with owner filtering to prevent cross-user access.
Task routes are nested and validated using:
task_pk
list_pk
todo_list__owner=request.user

This ensures a task cannot be accessed:

By another authenticated user
Outside its parent list
Via manual URL manipulation

ID Enumeration Protection

If a user attempts to access another user's list or task by altering the URL:

The system returns 404 (Not Found).
The application does not reveal whether the object exists.
No sensitive data is exposed.

Foreign Key Protection

Forms do not allow reassignment of owner or todo_list.
Foreign key relationships are enforced server-side.
Users cannot attach tasks to lists they do not own.

Security Summary

The application implements:
Authentication enforcement
Object-level ownership validation
Nested route protection
404 masking for unauthorised access
No public data endpoints

All authorisation behaviour was manually tested in both development and production environments.

------------------

## Template Overrides & UX Improvements

The default django-allauth logout confirmation template was overridden to improve user experience.

A custom template was created at:

templates/account/logout.html

Changes implemented:

Integrated logout confirmation into the main site layout using base.html
Added a “Cancel” option to prevent forced logout
Ensured logout remains a secure POST request
Corrected URL namespacing using todo:list_index

This maintains secure authentication behaviour while improving navigation and usability.

------------------------------------

## UI Refinement & Wireframe Alignment

During Phase 3, the user interface was refined to align with mobile-first wireframes while maintaining strict adherence to assessment requirements and Django best practices.

Landing Page Implementation

A dedicated public landing page was introduced using a HomeView:

Created home.html as a standalone mobile-first landing screen
Implemented authentication-based redirect logic:
Unauthenticated users see the landing page
Authenticated users are redirected to todo:list_index
Removed navigation from unauthenticated views to match wireframes
Ensured no JavaScript was introduced

This maintains clean separation between public and authenticated user flows.

URL Namespacing & Routing Correction

To support clean reverse lookups and prevent routing conflicts:
Moved HomeView to project-level urls.py
Removed root path duplication inside todo/urls.py
Updated redirect logic to use namespaced routes (todo:list_index)
Resolved NoReverseMatch and root path conflicts

This ensures scalable URL structure and proper namespacing.

Static File Configuration

A project-level static directory was implemented:

static/
    css/
        style.css

Configuration updates included:

Corrected STATICFILES_DIRS setting
Linked stylesheet in base.html using {% load static %}
Verified static files load in both local and production (Heroku)

Production static handling continues to use WhiteNoise.
---------------
Authentication Template Overrides

Custom templates were created to override django-allauth defaults:

templates/account/login.html
templates/account/signup.html

Enhancements:

Mobile-first stacked form layout
Full-width primary action buttons
Clear secondary navigation prompts
Styled Django messages
Preserved secure POST authentication behaviour
Maintained allauth default validation logic (no backend modification)

All templates extend base.html and follow consistent structure.
------------------------------
UI Design Principles Applied

Mobile-first layout
Minimal CSS
No frameworks
No JavaScript enhancements
No feature creep
Clean heading hierarchy
Consistent spacing and form structure
Accessibility preserved through semantic HTML
---------------------------
Production Verification

All UI refinements were:

Tested locally
Committed with structured Git history
Deployed to Heroku
Verified in production environment

No regressions in authentication, authorisation, or CRUD functionality were introduced.