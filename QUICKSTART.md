# Quick Start Guide

Get the API up and running in 3 steps:

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Seed Database

```bash
python seed_data.py
```

Expected output:
```
🌱 Seeding database...
✓ Database cleared
✓ Database initialized
✓ Added 12 users
✓ Added 8 groups
✓ Added 10 repositories
✓ Added 14 user-group memberships
✓ Added 25 user-repository access entries
✓ Added 17 group-repository access entries

✓ Database seeding completed successfully!
```

## Step 3: Run API

```bash
python main.py
```

API will start at `http://localhost:8000`

## Try It Out

### In your browser:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Via curl:

#### Find a user
```bash
curl "http://localhost:8000/user?username=alice_j"
```

#### Find a group
```bash
curl "http://localhost:8000/group?name=backend"
```

#### Find a repository
```bash
curl "http://localhost:8000/repo?name=api-service"
```

## Available Test Data

### Users (by GitHub username)
alice_j, bsmith, carol_white, dbrown, emma_d, frank_miller, grace_lee, hwilson, itaylor, j.anderson, kthomas, ljackson

### Groups (by name)
backend-platform, frontend, infrastructure, security, data-platform, qa, mobile, core-maintainers

### Repositories (by name)
api-service, web-app, mobile-app, infrastructure, kubernetes-configs, data-pipeline, security-tools, testing-framework, internal-libraries, ci-cd-pipelines

## Documentation

- See [README.md](README.md) for full API documentation
- See [REQUIREMENTS.md](REQUIREMENTS.md) for requirements and specifications
