
Capstone Project – To-Do List Application

A minimal, mobile-first Full Stack Django to-do list application built in VS Code, using:
  - Django (CBVs)
  - PostgreSQL (production – Heroku)
  - SQLite (local development)
  - django-allauth (authentication)
  - WhiteNoise + Gunicorn
  - Deployed to Heroku

------------------------------------

Live Application

Deployed on Heroku.
Admin panel available at:

`/admin/`

(Admin credentials provided separately.)

Project Overview

- Users can:
  1. Register (username + email + password)
  2. Create lists
  3. Create tasks inside lists
  4. Edit / delete lists and tasks
  5. Mark tasks as completed

The application enforces strict authentication and object-level ownership.

------------------------------

- Agile Planning (LO1)
  - Wireframes
  - GitHub Project (Kanban board)
  - Epics + User Stories created as Issues
  - Structured labels (Epic / Type / Priority)
  - Deployment-first development strategy

This ensured continuous deployment and avoided late-stage configuration issues.

------------------------------------------------------------
## Kanban Project Board (18/19 complete)

![Project Board](images/kanban.png)
------------------------------------------------------------
## Wireframes

![Landing Page](images/1.png), ![Sign-in page](images/2.png), ![Register Page](images/3.png), ![Dashboard Page](images/4.png), ![Edit Profile Page](images/5.png), ![Edit Profile Page 2](images/9.png), ![Edit Profile Page 3](images/ten.png), ![Edit Profile Page 4](images/ten2.png), 

----------------------------------------------------

Deployment Architecture

- Production Stack
  - Heroku
  - Gunicorn
  - WhiteNoise
  - Heroku Postgres (essential-0 plan)

Key Production Config

```python
DEBUG = os.environ.get("DEBUG", "False") == "True"

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
```

Production verified using:


`connection.vendor == "postgresql"`

Security:
- SECRET_KEY stored as environment variable
- Hardcoded secret removed and rotated
- .gitignore excludes:
  - db.sqlite3
  - .venv/
  - env files
  - pycache/

-------------------------------------------

Authentication (Phase 1)

Implemented using django-allauth.
  - Login / Signup / Logout
  - Password change
  - Email update
  - Custom template overrides
  - Secure POST logout
  - Environment-based settings
  - DEBUG=False in production


All authentication routes verified locally and in production.

------------------------------------

Database & Models (Phase 2)
Relational Structure

`User → TodoList → Task`

TodoList Model
  - owner → FK(User)
  - name
  - created_on
  - updated_on


Task Model
  - todo_list → FK(TodoList)
  - title
  - description (optional)
  - completed (Boolean)
  - due_date (optional)
  - created_on
  - updated_on
CASCADE deletion ensures referential integrity.

----------------------------------------------------

Authorisation & Security

Strict object-level ownership enforcement.

Implemented Controls
  - LoginRequiredMixin on all protected views
  - Querysets filtered by owner=request.user
  - Nested task routes:

 `/lists/<list_pk>/tasks/<task_pk>/...`

  - get_object_or_404(..., owner=request.user)
  - 404 masking (prevents ID enumeration)
  - Foreign keys assigned server-side
  - No public data endpoints

Result
Users cannot:
  - Access another user's lists
  - Access another user's tasks
  - Manipulate URLs to retrieve data
  - Reassign ownership via POST tampering

All verified locally and in production.

CRUD Functionality

Fully implemented for:
  - Create List
  - Read List
  - Update List
  - Delete List
  - Create Task (nested)
  - Update Task
  - Delete Task
  - Mark Task Complete
Django messages framework used for UX feedback.

All CRUD tested in:
  - Local SQLite
  - Production Heroku Postgres

------------------------------------------------

UI & UX (Phase 3)

Design goals:
  - Mobile-first
  - No frontend frameworks
  - No JavaScript
  - Minimal CSS
  - Wireframe alignment

Key Refinements
  - Public landing page (redirects authenticated users)
  - Custom dashboard layout
  - Scoped message rendering
  - Custom profile hub (/profile/)
  - Username update (custom view)
  - Allauth template overrides
  - Responsive desktop width constraint:

```CSS
@media (min-width: 768px) {
 .auth,
 .dashboard,
 .landing-container {
   max-width: 480px;
   margin: 0 auto;
 }
}
```

Completed tasks:
  - Appear below active tasks
  - Styled with strikethrough + reduced opacity
  - Remain visible until manually deleted


Testing

Manual testing completed locally and in production.

Verified:
  - All CRUD operations
  - Redirect for unauthenticated users
  - Cross-user access returns 404
  - Nested route integrity
  - Messages display correctly
  - Postgres in production
  - DEBUG=False confirmed
All tests passed.

-----------------------------------------

Admin Panel

Django admin enabled for:
  - Users
  - TodoLists
  - Tasks

Production superuser created after Postgres provisioning.

-------------------------------------

Technologies Used
  - Python
  - Django
  - PostgreSQL
  - SQLite
  - Gunicorn
  - WhiteNoise
  - django-allauth
  - Heroku
  - Git / GitHub
  - VS Code

---------------------------------------------------------

Security Summary
 - Environment-based configuration ✔
 - Postgres in production ✔
 - DEBUG=False ✔
 - SECRET_KEY not committed ✔
 - Object-level ownership enforced ✔
 - 404 masking for unauthorised access ✔
 - No data exposure via URL manipulation ✔

---------------------------------------------------

Development Phases

- Phase 1 – Authentication & deployment
- Phase 2 – Custom models + ownership + CRUD
- Phase 3 – UI polish, testing, README finalisation

