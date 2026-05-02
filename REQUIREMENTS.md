# User Requirements Document (URD)
## GitHub-to-AD Account Mapping API

**Document Version:** 1.0  
**Date:** April 2026  
**Status:** Approved

---

## 1. Executive Summary

The fictional company uses GitHub for code repositories and collaboration, with employees using personal GitHub accounts added to the company's GitHub organization. Currently, employees without GitHub admin access cannot easily determine which GitHub account belongs to which Active Directory (AD) account. This API provides a solution to map GitHub accounts to AD accounts and query access permissions across the organization.

---

## 2. Business Drivers

- **Problem Statement:** Difficulty identifying the real identity behind GitHub nicknames without admin access
- **Business Value:** Improved security management, user identification, and access control visibility
- **Scope:** Query-only interface for reading GitHub-to-AD mappings and access levels

---

## 3. User Personas

### 3.1 Team Lead
- **Goal:** Quickly identify who owns a GitHub account when reviewing pull requests
- **Needs:** Search by GitHub username, see user's name, email, job title, and team
- **Frequency:** Several times per week

### 3.2 Security/Compliance Officer
- **Goal:** Audit group memberships and repository access levels
- **Needs:** Query groups, see member lists and associated AD groups; query repos to see who has access
- **Frequency:** Monthly for audits, ad-hoc for investigations

### 3.3 Repository Manager
- **Goal:** Understand who has access to specific repositories
- **Needs:** Query a repository and see all users/groups with access and their permission levels
- **Frequency:** Weekly during onboarding/offboarding

---

## 4. Functional Requirements

### 4.1 User Endpoint (`GET /user`)

**Purpose:** Query user information and their access context

**Input Parameters:**
- Query parameter: `username` (optional, filters by GitHub username)
- Query parameter: `email` (optional, filters by email address)
- Query parameter: `name` (optional, filters by display name, partial match)

**Output:** Returns an array of user objects containing:
- User ID (AD account identifier)
- GitHub username
- Display name
- Email address
- Job title
- Team/Department
- List of groups the user is a member of
- List of repositories they have access to with access level (push, pull, maintain, admin)

**Business Logic:**
- At least one query parameter must be provided
- Search should be case-insensitive
- Return all matching users if multiple results exist

### 4.2 Group Endpoint (`GET /group`)

**Purpose:** Query group information and membership

**Input Parameters:**
- Query parameter: `name` (optional, filters by group name)
- Query parameter: `ad_group` (optional, filters by associated AD group)

**Output:** Returns an array of group objects containing:
- Group ID
- GitHub group name
- Display name
- Associated AD group name
- List of member users (with user details)
- List of repositories the group has access to with access level

**Business Logic:**
- At least one query parameter must be provided
- Return all matching groups if multiple results exist

### 4.3 Repository Endpoint (`GET /repo`)

**Purpose:** Query repository access and permissions

**Input Parameters:**
- Query parameter: `name` (optional, filters by repository name)
- Query parameter: `owner` (optional, filters by organization/owner)

**Output:** Returns an array of repository objects containing:
- Repository ID
- Repository name
- Organization/owner
- List of users with access (with access level)
- List of groups with access (with access level)
- Default access level for the repository

**Business Logic:**
- At least one query parameter must be provided
- Return all matching repositories if multiple results exist

---

## 5. Non-Functional Requirements

### 5.1 Performance
- API responses must complete within 2 seconds for typical queries
- Support concurrent requests from up to 50 users

### 5.2 Security
- API should be read-only (no write operations)
- Authentication/authorization scope is out of current phase
- Data should not expose unnecessary sensitive information (passwords, tokens)

### 5.3 Data Quality
- Mock data should represent realistic organizational structures
- Include diverse job titles, teams, and access patterns
- Minimum 10 entries per entity type for testing

### 5.4 Scalability
- Database schema should support growth to 1000+ users without major refactoring
- Use proper indexes for query performance

### 5.5 API Standards
- RESTful design with proper HTTP methods and status codes
- JSON request/response format
- Comprehensive OpenAPI 3.0 specification
- Self-documenting via `/docs` endpoint

---

## 6. Data Requirements

### 6.1 User Entity
- AD account ID (unique)
- GitHub username (unique)
- Display name
- Email address
- Job title
- Team/Department
- Active status

### 6.2 Group Entity
- Group ID (unique)
- GitHub group name
- Display name
- Associated AD group name
- Description

### 6.3 Repository Entity
- Repository ID (unique)
- Name
- Organization/owner
- Description

### 6.4 Relationships
- User-to-Group membership (many-to-many)
- User-to-Repository access (many-to-many, with access level)
- Group-to-Repository access (many-to-many, with access level)

### 6.5 Access Levels
- **pull:** Read-only access
- **push:** Read and write access
- **maintain:** Maintain repository (manage without delete)
- **admin:** Full administrative access

---

## 7. Constraints & Assumptions

### 7.1 Constraints
- Phase 1 uses mocked/static data (no live GitHub/AD integration)
- No authentication required for prototype phase
- Read-only operations only
- PostgreSQL database backend

### 7.2 Assumptions
- All users exist in both GitHub and AD
- All GitHub groups map to AD groups
- Access levels are managed externally (API only queries, doesn't modify)

---

## 8. Success Criteria

- ✓ API successfully queries users by username, email, or name
- ✓ API successfully queries groups by name or AD group
- ✓ API successfully queries repositories by name or owner
- ✓ All endpoints return complete, accurate data from mock dataset
- ✓ OpenAPI specification generated and available at `/docs`
- ✓ Database contains 10+ realistic data entries
- ✓ All queries complete within 2 seconds
- ✓ Error handling returns appropriate HTTP status codes and messages

---

## 9. Out of Scope (Future Phases)

- Authentication/authorization mechanisms
- Write operations (POST, PUT, DELETE)
- Real-time synchronization with GitHub or AD
- Rate limiting/throttling policies
- Webhook integrations
- Audit logging of API access

---

## 10. Acceptance Criteria

1. All three endpoints implemented and working with mock data
2. Each endpoint supports the specified query parameters
3. Responses match the documented output format
4. OpenAPI spec is auto-generated and accessible
5. Mock data includes realistic scenarios (users in multiple groups, repos with mixed access, etc.)
6. No production data included in mock dataset
