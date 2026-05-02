"""
Script to seed the database with mock data for testing.
Run with: python seed_data.py
"""
import os
import sys
from sqlalchemy.orm import Session

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal, init_db
from app.models import Base, User, Group, Repository, user_group_association, user_repository_association, group_repository_association

def clear_database():
    """Clear all tables"""
    Base.metadata.drop_all(bind=engine)
    print("✓ Database cleared")

def seed_users(db: Session):
    """Seed users with realistic data"""
    users = [
        User(
            ad_id="ACME\\alice.johnson",
            github_username="alice_j",
            display_name="Alice Johnson",
            email="alice.johnson@acme.com",
            job_title="Senior Software Engineer",
            team="Backend Platform"
        ),
        User(
            ad_id="ACME\\bob.smith",
            github_username="bsmith",
            display_name="Bob Smith",
            email="bob.smith@acme.com",
            job_title="Software Engineer",
            team="Frontend"
        ),
        User(
            ad_id="ACME\\carol.white",
            github_username="carol_white",
            display_name="Carol White",
            email="carol.white@acme.com",
            job_title="Engineering Manager",
            team="Backend Platform"
        ),
        User(
            ad_id="ACME\\david.brown",
            github_username="dbrown",
            display_name="David Brown",
            email="david.brown@acme.com",
            job_title="DevOps Engineer",
            team="Infrastructure"
        ),
        User(
            ad_id="ACME\\emma.davis",
            github_username="emma_d",
            display_name="Emma Davis",
            email="emma.davis@acme.com",
            job_title="Security Engineer",
            team="Security"
        ),
        User(
            ad_id="ACME\\frank.miller",
            github_username="fmiller",
            display_name="Frank Miller",
            email="frank.miller@acme.com",
            job_title="QA Engineer",
            team="Quality Assurance"
        ),
        User(
            ad_id="ACME\\grace.lee",
            github_username="grace_lee",
            display_name="Grace Lee",
            email="grace.lee@acme.com",
            job_title="Technical Lead",
            team="Frontend"
        ),
        User(
            ad_id="ACME\\henry.wilson",
            github_username="hwilson",
            display_name="Henry Wilson",
            email="henry.wilson@acme.com",
            job_title="Software Engineer",
            team="Backend Platform"
        ),
        User(
            ad_id="ACME\\iris.taylor",
            github_username="itaylor",
            display_name="Iris Taylor",
            email="iris.taylor@acme.com",
            job_title="Data Engineer",
            team="Data Platform"
        ),
        User(
            ad_id="ACME\\jack.anderson",
            github_username="j.anderson",
            display_name="Jack Anderson",
            email="jack.anderson@acme.com",
            job_title="Software Engineer",
            team="Mobile"
        ),
        User(
            ad_id="ACME\\karen.thomas",
            github_username="kthomas",
            display_name="Karen Thomas",
            email="karen.thomas@acme.com",
            job_title="Engineering Manager",
            team="Infrastructure"
        ),
        User(
            ad_id="ACME\\leo.jackson",
            github_username="ljackson",
            display_name="Leo Jackson",
            email="leo.jackson@acme.com",
            job_title="Software Engineer",
            team="Security"
        ),
    ]

    db.add_all(users)
    db.commit()
    print(f"✓ Added {len(users)} users")
    return users

def seed_groups(db: Session):
    """Seed groups with realistic data"""
    groups = [
        Group(
            name="backend-platform",
            display_name="Backend Platform",
            ad_group="ACME\\Backend-Platform-Team",
            description="Core backend infrastructure and services"
        ),
        Group(
            name="frontend",
            display_name="Frontend Team",
            ad_group="ACME\\Frontend-Team",
            description="React and web frontend development"
        ),
        Group(
            name="infrastructure",
            display_name="Infrastructure",
            ad_group="ACME\\Infrastructure-Team",
            description="DevOps, Kubernetes, and cloud infrastructure"
        ),
        Group(
            name="security",
            display_name="Security Team",
            ad_group="ACME\\Security-Team",
            description="Application and infrastructure security"
        ),
        Group(
            name="data-platform",
            display_name="Data Platform",
            ad_group="ACME\\Data-Platform-Team",
            description="Data pipelines and analytics"
        ),
        Group(
            name="qa",
            display_name="QA Team",
            ad_group="ACME\\QA-Team",
            description="Quality assurance and testing"
        ),
        Group(
            name="mobile",
            display_name="Mobile Team",
            ad_group="ACME\\Mobile-Team",
            description="iOS and Android development"
        ),
        Group(
            name="core-maintainers",
            display_name="Core Maintainers",
            ad_group="ACME\\Core-Maintainers",
            description="Maintainers of critical infrastructure"
        ),
    ]

    db.add_all(groups)
    db.commit()
    print(f"✓ Added {len(groups)} groups")
    return groups

def seed_repositories(db: Session):
    """Seed repositories with realistic data"""
    repos = [
        Repository(
            name="api-service",
            owner="acme-company",
            description="Main REST API service"
        ),
        Repository(
            name="web-app",
            owner="acme-company",
            description="React web application"
        ),
        Repository(
            name="mobile-app",
            owner="acme-company",
            description="React Native mobile application"
        ),
        Repository(
            name="infrastructure",
            owner="acme-company",
            description="Terraform and infrastructure code"
        ),
        Repository(
            name="kubernetes-configs",
            owner="acme-company",
            description="Kubernetes deployment configurations"
        ),
        Repository(
            name="data-pipeline",
            owner="acme-company",
            description="Apache Spark data processing pipeline"
        ),
        Repository(
            name="security-tools",
            owner="acme-company",
            description="Internal security tools and utilities"
        ),
        Repository(
            name="testing-framework",
            owner="acme-company",
            description="Custom testing framework and utilities"
        ),
        Repository(
            name="internal-libraries",
            owner="acme-company",
            description="Shared internal libraries and SDKs"
        ),
        Repository(
            name="ci-cd-pipelines",
            owner="acme-company",
            description="GitHub Actions and CI/CD workflows"
        ),
    ]

    db.add_all(repos)
    db.commit()
    print(f"✓ Added {len(repos)} repositories")
    return repos

def seed_user_group_memberships(db: Session):
    """Assign users to groups"""
    # Get all data
    users = db.query(User).all()
    groups = db.query(Group).all()

    # Create a mapping for easier access
    user_map = {u.github_username: u for u in users}
    group_map = {g.name: g for g in groups}

    # Define memberships
    memberships = [
        ("alice_j", ["backend-platform", "core-maintainers"]),
        ("bsmith", ["frontend"]),
        ("carol_white", ["backend-platform"]),
        ("dbrown", ["infrastructure"]),
        ("emma_d", ["security"]),
        ("frank_miller", ["qa"]),
        ("grace_lee", ["frontend", "core-maintainers"]),
        ("hwilson", ["backend-platform"]),
        ("itaylor", ["data-platform"]),
        ("j.anderson", ["mobile"]),
        ("kthomas", ["infrastructure", "core-maintainers"]),
        ("ljackson", ["security"]),
    ]

    count = 0
    for github_username, group_names in memberships:
        user = user_map.get(github_username)
        if user:
            for group_name in group_names:
                group = group_map.get(group_name)
                if group and group not in user.groups:
                    user.groups.append(group)
                    count += 1

    db.commit()
    print(f"✓ Added {count} user-group memberships")

def seed_user_repository_access(db: Session):
    """Assign users to repositories with access levels"""
    users = db.query(User).all()
    repos = db.query(Repository).all()

    user_map = {u.github_username: u for u in users}
    repo_map = {r.name: r for r in repos}

    # Define access levels
    # Format: (github_username, repo_name, access_level)
    access = [
        ("alice_j", "api-service", "admin"),
        ("alice_j", "internal-libraries", "admin"),
        ("alice_j", "ci-cd-pipelines", "maintain"),
        ("bsmith", "web-app", "push"),
        ("bsmith", "api-service", "pull"),
        ("carol_white", "api-service", "maintain"),
        ("carol_white", "internal-libraries", "push"),
        ("dbrown", "infrastructure", "admin"),
        ("dbrown", "kubernetes-configs", "admin"),
        ("emma_d", "security-tools", "admin"),
        ("emma_d", "api-service", "pull"),
        ("emma_d", "infrastructure", "maintain"),
        ("frank_miller", "testing-framework", "push"),
        ("frank_miller", "api-service", "pull"),
        ("frank_miller", "web-app", "pull"),
        ("grace_lee", "web-app", "admin"),
        ("grace_lee", "api-service", "maintain"),
        ("hwilson", "api-service", "push"),
        ("hwilson", "internal-libraries", "push"),
        ("itaylor", "data-pipeline", "admin"),
        ("itaylor", "api-service", "pull"),
        ("j.anderson", "mobile-app", "admin"),
        ("j.anderson", "api-service", "pull"),
        ("kthomas", "infrastructure", "maintain"),
        ("kthomas", "kubernetes-configs", "maintain"),
        ("kthomas", "ci-cd-pipelines", "admin"),
        ("ljackson", "security-tools", "push"),
        ("ljackson", "infrastructure", "maintain"),
    ]

    count = 0
    for github_username, repo_name, access_level in access:
        user = user_map.get(github_username)
        repo = repo_map.get(repo_name)
        if user and repo:
            # Insert into association table with access level
            stmt = user_repository_association.insert().values(
                user_id=user.id,
                repository_id=repo.id,
                access_level=access_level
            )
            db.execute(stmt)
            count += 1

    db.commit()
    print(f"✓ Added {count} user-repository access entries")

def seed_group_repository_access(db: Session):
    """Assign groups to repositories with access levels"""
    groups = db.query(Group).all()
    repos = db.query(Repository).all()

    group_map = {g.name: g for g in groups}
    repo_map = {r.name: r for r in repos}

    # Define access levels
    # Format: (group_name, repo_name, access_level)
    access = [
        ("backend-platform", "api-service", "admin"),
        ("backend-platform", "internal-libraries", "maintain"),
        ("frontend", "web-app", "admin"),
        ("frontend", "api-service", "pull"),
        ("infrastructure", "infrastructure", "admin"),
        ("infrastructure", "kubernetes-configs", "admin"),
        ("infrastructure", "ci-cd-pipelines", "maintain"),
        ("security", "security-tools", "admin"),
        ("security", "api-service", "maintain"),
        ("data-platform", "data-pipeline", "admin"),
        ("qa", "testing-framework", "admin"),
        ("qa", "api-service", "pull"),
        ("qa", "web-app", "pull"),
        ("mobile", "mobile-app", "admin"),
        ("mobile", "api-service", "pull"),
        ("core-maintainers", "ci-cd-pipelines", "admin"),
        ("core-maintainers", "internal-libraries", "maintain"),
    ]

    count = 0
    for group_name, repo_name, access_level in access:
        group = group_map.get(group_name)
        repo = repo_map.get(repo_name)
        if group and repo:
            stmt = group_repository_association.insert().values(
                group_id=group.id,
                repository_id=repo.id,
                access_level=access_level
            )
            db.execute(stmt)
            count += 1

    db.commit()
    print(f"✓ Added {count} group-repository access entries")

def main():
    print("🌱 Seeding database...")

    # Create session
    db = SessionLocal()

    try:
        # Clear existing data
        clear_database()

        # Reinitialize tables after clearing
        init_db()
        print("✓ Database initialized")

        # Seed data
        users = seed_users(db)
        groups = seed_groups(db)
        repos = seed_repositories(db)
        seed_user_group_memberships(db)
        seed_user_repository_access(db)
        seed_group_repository_access(db)

        print("\n✓ Database seeding completed successfully!")
        print(f"  - {len(users)} users")
        print(f"  - {len(groups)} groups")
        print(f"  - {len(repos)} repositories")

    except Exception as e:
        print(f"✗ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
