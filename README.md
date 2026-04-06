# GitHub-to-AD Account Mapping API

A FastAPI-based REST API for querying GitHub user-to-Active Directory (AD) account mappings and access control information across repositories and groups.

## Overview

This API solves the problem of employees without GitHub admin access being unable to identify which GitHub account belongs to which AD account. It provides three main query endpoints for users, groups, and repositories.

## Features

- **User Endpoint** (`GET /user`): Query users by username, email, or name
  - Returns user details (name, email, job title, team)
  - Shows group memberships
  - Lists repository access with access levels
  
- **Group Endpoint** (`GET /group`): Query groups by name or AD group
  - Returns group details and associated AD group
  - Lists group members with full details
  - Shows repository access with access levels
  
- **Repository Endpoint** (`GET /repo`): Query repositories by name or owner
  - Returns repository details
  - Lists users with access and access levels
  - Lists groups with access and access levels

- **OpenAPI Documentation**: Auto-generated interactive API docs at `/docs`
- **Health Check**: `/health` endpoint for monitoring

## Architecture

```
fictional_api/
├── app/
│   ├── __init__.py
│   ├── models.py           # SQLAlchemy ORM models
│   ├── schemas.py          # Pydantic response schemas
│   ├── database.py         # Database connection and initialization
│   └── routes.py           # API endpoint definitions
├── main.py                 # FastAPI application entry point
├── seed_data.py            # Mock data seeding script
├── requirements.txt        # Python dependencies
├── REQUIREMENTS.md         # User Requirements Document
└── README.md              # This file
```

## Data Model

### Entities

- **User**: GitHub-to-AD mapping with personal details
- **Group**: GitHub groups mapped to AD groups
- **Repository**: GitHub repositories with access tracking
- **Access Levels**: pull (read), push (read/write), maintain, admin

### Relationships

- Users belong to Groups (many-to-many)
- Users have access to Repositories with an access level
- Groups have access to Repositories with an access level

## Setup & Installation

### Prerequisites

- Python 3.9+
- PostgreSQL (or SQLite for development)

### Installation

1. Clone/navigate to the project directory:
```bash
cd fictional_api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database URL
# Default: DATABASE_URL=sqlite:///./test.db (for development)
```

5. Seed the database with mock data:
```bash
python seed_data.py
```

## Running the API

### Development

```bash
python main.py
```

The API will start at `http://localhost:8000`

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### 1. Query Users

```
GET /user?username=alice_j
GET /user?email=alice.johnson@acme.com
GET /user?name=Alice
```

**Parameters:**
- `username` (optional): Exact GitHub username match
- `email` (optional): Exact email match
- `name` (optional): Partial display name match (case-insensitive)

**At least one parameter must be provided.**

**Response:**
```json
{
  "users": [
    {
      "user_id": 1,
      "ad_id": "ACME\\alice.johnson",
      "github_username": "alice_j",
      "display_name": "Alice Johnson",
      "email": "alice.johnson@acme.com",
      "job_title": "Senior Software Engineer",
      "team": "Backend Platform",
      "groups": [
        {
          "group_id": 8,
          "name": "core-maintainers",
          "display_name": "Core Maintainers"
        }
      ],
      "repositories": [
        {
          "repository_id": 1,
          "name": "api-service",
          "owner": "acme-company",
          "access_level": "admin"
        }
      ]
    }
  ],
  "count": 1
}
```

### 2. Query Groups

```
GET /group?name=backend
GET /group?ad_group=ACME\\Backend-Platform-Team
```

**Parameters:**
- `name` (optional): Group name (partial match, case-insensitive)
- `ad_group` (optional): Associated AD group name

**At least one parameter must be provided.**

**Response:**
```json
{
  "groups": [
    {
      "group_id": 1,
      "name": "backend-platform",
      "display_name": "Backend Platform",
      "ad_group": "ACME\\Backend-Platform-Team",
      "description": "Core backend infrastructure and services",
      "members": [
        {
          "user_id": 1,
          "ad_id": "ACME\\alice.johnson",
          "github_username": "alice_j",
          "display_name": "Alice Johnson",
          "email": "alice.johnson@acme.com",
          "job_title": "Senior Software Engineer",
          "team": "Backend Platform"
        }
      ],
      "repositories": [
        {
          "repository_id": 1,
          "name": "api-service",
          "owner": "acme-company",
          "access_level": "admin"
        }
      ]
    }
  ],
  "count": 1
}
```

### 3. Query Repositories

```
GET /repo?name=api-service
GET /repo?owner=acme-company
```

**Parameters:**
- `name` (optional): Repository name (partial match, case-insensitive)
- `owner` (optional): Organization/owner name (partial match, case-insensitive)

**At least one parameter must be provided.**

**Response:**
```json
{
  "repositories": [
    {
      "repository_id": 1,
      "name": "api-service",
      "owner": "acme-company",
      "description": "Main REST API service",
      "users": [
        {
          "user_id": 1,
          "github_username": "alice_j",
          "display_name": "Alice Johnson",
          "access_level": "admin"
        }
      ],
      "groups": [
        {
          "group_id": 1,
          "name": "backend-platform",
          "display_name": "Backend Platform",
          "access_level": "admin"
        }
      ]
    }
  ],
  "count": 1
}
```

## Interactive Documentation

Once the API is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Mock Data

The project includes mock data for 12+ users, 8 groups, and 10 repositories with realistic access patterns. Run `python seed_data.py` to reset and reload the mock data.

### Sample Data Includes:

- **Users**: Alice Johnson (Senior Engineer), Bob Smith (Frontend), Carol White (Manager), etc.
- **Groups**: Backend Platform, Frontend, Infrastructure, Security, Data Platform, QA, Mobile, Core Maintainers
- **Repositories**: api-service, web-app, mobile-app, infrastructure, kubernetes-configs, data-pipeline, security-tools, testing-framework, internal-libraries, ci-cd-pipelines

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful query
- `400 Bad Request`: Missing required query parameters
- `404 Not Found`: No results matching the query
- `422 Unprocessable Entity`: Invalid request format
- `500 Internal Server Error`: Server error

Example error response:
```json
{
  "detail": "At least one query parameter (username, email, or name) must be provided"
}
```

## Requirements Document

See [REQUIREMENTS.md](REQUIREMENTS.md) for the full User Requirements Document including:
- Business drivers and user personas
- Detailed functional and non-functional requirements
- Data model specifications
- Success criteria and acceptance criteria

## Development Notes

- The API uses SQLAlchemy ORM for database abstraction
- Pydantic models ensure type-safe request/response handling
- FastAPI automatically generates OpenAPI 3.1.0 specification
- Database initialization and seeding are fully automated
- Mock data is realistic and representative of real organizational structures

## Future Enhancements (Out of Scope)

- Authentication and authorization mechanisms
- Write operations (POST, PUT, DELETE)
- Real-time synchronization with GitHub and AD
- Rate limiting and caching
- Webhook integrations for real-time updates
- Audit logging of API access

## Support

For issues or questions:
1. Check the OpenAPI documentation at `/docs`
2. Review error messages for guidance on required parameters
3. Verify mock data is loaded with `python seed_data.py`
