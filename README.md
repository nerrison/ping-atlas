# Ping Atlas

Community-driven uptime monitoring platform.

Ping Atlas is a platform for communities to register, monitor, and share the reliability status of services and endpoints.

Unlike traditional personal monitoring dashboards, Ping Atlas is designed around shared visibility and collaboration. Communities can create monitoring groups, add endpoints, track availability, and maintain service reliability together.

---

# Overview

A Ping Atlas group represents a collection of services that need monitoring.

Examples:

* Community infrastructure
* Open-source projects
* Public APIs
* Websites
* Online services

Each group can contain multiple endpoints. The backend continuously verifies these endpoints and records:

* Availability status
* Response times
* Health check history
* Incidents and failures

The goal is to provide reliable, transparent service monitoring for communities.

---

# Core Concepts

Ping Atlas separates three different ideas:

## Monitoring

Monitoring determines whether an endpoint is healthy.

The backend is responsible for:

* Checking endpoints
* Measuring response times
* Recording health history
* Detecting failures
* Tracking incidents

## Visibility

Visibility determines who can see endpoint information.

Future endpoint visibility controls will allow:

* Public endpoints visible to everyone
* Hidden endpoints visible only to authorized managers

Hidden endpoints will continue to be monitored normally. Hiding an endpoint only controls who can view the information.

## Permissions

Permissions determine who can modify monitoring resources.

Users can only manage groups where they have the appropriate relationship.

---

# Permissions Model

## Public Users

Visitors can:

* View public groups
* View public endpoints
* View service status
* View monitoring history
* View incidents

They cannot:

* Create groups
* Modify endpoints
* Manage services

---

## Verified Users

Verified users can:

* Create monitoring groups
* Add endpoints
* Suggest changes
* Comment on services
* Report issues
* Become group co-managers

A verified user does not automatically have management access to every group.

---

## Group Creators

The creator of a group has management authority over that group.

Creators can:

* Update group information
* Add and remove endpoints
* Manage monitoring resources
* Assign co-managers
* Resolve reported issues

---

## Co-Managers

Creators can appoint verified users as co-managers.

Co-managers can manage only groups they have been assigned to.

They can:

* Update assigned groups
* Manage assigned endpoints
* Help maintain monitoring information
* Assist with incident resolution

---

## Verified Users Without Management Access

Verified users who are not creators or co-managers can still contribute.

They can:

* Suggest changes
* Comment on services
* Report problems

They cannot:

* Modify groups
* Modify endpoints
* Change monitoring configuration

---

# Current Features

## Groups

Groups organize related monitored services.

A group contains:

* Name
* Description
* Type
* Associated endpoints

---

## Endpoints

Endpoints represent services being monitored.

Stored information includes:

* URL
* HTTP method
* Current status
* Response time
* Last check time

---

## Monitoring History

Ping Atlas records monitoring results over time.

Stored information includes:

* Latency
* Availability
* Errors
* Check timestamps

---

## Incidents

Incidents represent detected service problems.

Stored information includes:

* Endpoint affected
* Error information
* Status changes
* Incident timestamps

---

# Technology Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* Pydantic
* Uvicorn

## Frontend

Current frontend:

* HTML
* CSS
* JavaScript

---

# Backend Architecture

Ping Atlas follows a layered backend architecture:

```
Routes
   |
   v
Services
   |
   v
Repositories
   |
   v
Models
   |
   v
PostgreSQL
```

---

# Backend Structure

```
server/
├── app/
│   ├── core/
│   │   └── Application configuration
│   │
│   ├── db/
│   │   └── Database connection and sessions
│   │
│   ├── models/
│   │   └── SQLAlchemy database models
│   │
│   ├── schemas/
│   │   └── API request and response models
│   │
│   ├── repositories/
│   │   └── Database operations
│   │
│   ├── services/
│   │   └── Business logic
│   │
│   ├── routes/
│   │   └── API endpoints
│   │
│   ├── mapper/
│   │   └── Data transformation helpers
│   │
│   └── utils/
│       └── Shared utilities
│
├── alembic/
│   └── Database migrations
│
└── main.py
```

---

# Database Design

## Groups

Groups represent collections of monitored services.

Relationship:

```
Group
 |
 +-- Endpoint
```

---

## Endpoints

Endpoints represent services being monitored.

Relationship:

```
Endpoint
 |
 +-- History
 |
 +-- Incident
```

---

## Histories

Stores endpoint monitoring results.

Examples:

* Response latency
* Availability
* Errors
* Check times

---

## Incidents

Stores detected endpoint failures.

Examples:

* Service downtime
* Failed checks
* Error messages

---

# Local Development

## Requirements

* Python 3.12+
* PostgreSQL

---

## Setup

Clone the repository:

```bash
git clone https://github.com/nerrison/ping-atlas.git
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
```

---

# Database Migrations

Create a migration:

```bash
alembic revision --autogenerate -m "message"
```

Apply migrations:

```bash
alembic upgrade head
```

Check migration status:

```bash
alembic current
```

---

# Running the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

API documentation:

```
/docs
```

---

# Testing

Tests are written using pytest.

Run:

```bash
pytest
```

---

# Roadmap

## Authentication and Identity

* Verified email accounts
* User identity management
* Group ownership

## Permissions and Collaboration

* Co-manager assignments
* Group-level permissions
* Suggestions
* Comments
* Issue tracking

## Monitoring Engine

* Background monitoring workers
* Scheduled checks
* Automatic failure detection
* Recovery tracking
* Monitoring reliability improvements

## Endpoint Visibility

* Public endpoints
* Hidden endpoints
* Permission-controlled visibility

Hidden endpoints will continue to be monitored but will only be visible to authorized users.

## Platform Features

* Notifications
* Public status pages
* Advanced analytics
* Historical uptime reports
* Reliability statistics

---

# License

To be decided.
