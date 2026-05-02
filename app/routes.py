from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import User, Group, Repository, user_repository_association, group_repository_association
from app.schemas import (
    UserListResponse, UserDetail, GroupInfo, RepositoryAccessInfo,
    GroupListResponse, GroupDetail, UserMemberInfo, RepositoryAccessForGroup,
    RepositoryListResponse, RepositoryDetail, UserAccessForRepo, GroupAccessForRepo
)

router = APIRouter()


@router.get("/user", response_model=UserListResponse, tags=["users"])
def query_users(
    username: str = Query(None, description="Filter by GitHub username (exact match)"),
    email: str = Query(None, description="Filter by email address"),
    name: str = Query(None, description="Filter by display name (partial match, case-insensitive)"),
    db: Session = Depends(get_db)
):
    """
    Query users and retrieve their details, group memberships, and repository access.

    At least one query parameter must be provided.
    """
    # Validate that at least one parameter is provided
    if not any([username, email, name]):
        raise HTTPException(
            status_code=400,
            detail="At least one query parameter (username, email, or name) must be provided"
        )

    query = db.query(User)

    if username:
        query = query.filter(User.github_username == username)
    if email:
        query = query.filter(User.email == email)
    if name:
        query = query.filter(User.display_name.ilike(f"%{name}%"))

    users = query.all()

    if not users:
        return UserListResponse(users=[], count=0)

    user_details = []
    for user in users:
        # Get groups
        groups = [
            GroupInfo(
                group_id=g.id,
                name=g.name,
                display_name=g.display_name
            )
            for g in user.groups
        ]

        # Get repository access
        repos = []
        for repo in user.repositories:
            # Get access level from association table
            stmt = db.query(user_repository_association).filter(
                user_repository_association.c.user_id == user.id,
                user_repository_association.c.repository_id == repo.id
            ).first()
            access_level = stmt[2] if stmt else "pull"

            repos.append(
                RepositoryAccessInfo(
                    repository_id=repo.id,
                    name=repo.name,
                    owner=repo.owner,
                    access_level=access_level
                )
            )

        user_details.append(
            UserDetail(
                user_id=user.id,
                ad_id=user.ad_id,
                github_username=user.github_username,
                display_name=user.display_name,
                email=user.email,
                job_title=user.job_title,
                team=user.team,
                groups=groups,
                repositories=repos
            )
        )

    return UserListResponse(users=user_details, count=len(user_details))


@router.get("/group", response_model=GroupListResponse, tags=["groups"])
def query_groups(
    name: str = Query(None, description="Filter by group name"),
    ad_group: str = Query(None, description="Filter by associated AD group"),
    db: Session = Depends(get_db)
):
    """
    Query groups and retrieve their details, member users, and repository access.

    At least one query parameter must be provided.
    """
    # Validate that at least one parameter is provided
    if not any([name, ad_group]):
        raise HTTPException(
            status_code=400,
            detail="At least one query parameter (name or ad_group) must be provided"
        )

    query = db.query(Group)

    if name:
        query = query.filter(Group.name.ilike(f"%{name}%"))
    if ad_group:
        query = query.filter(Group.ad_group == ad_group)

    groups = query.all()

    if not groups:
        return GroupListResponse(groups=[], count=0)

    group_details = []
    for group in groups:
        # Get members
        members = [
            UserMemberInfo(
                user_id=u.id,
                ad_id=u.ad_id,
                github_username=u.github_username,
                display_name=u.display_name,
                email=u.email,
                job_title=u.job_title,
                team=u.team
            )
            for u in group.users
        ]

        # Get repository access
        repos = []
        for repo in group.repositories:
            # Get access level from association table
            stmt = db.query(group_repository_association).filter(
                group_repository_association.c.group_id == group.id,
                group_repository_association.c.repository_id == repo.id
            ).first()
            access_level = stmt[2] if stmt else "pull"

            repos.append(
                RepositoryAccessForGroup(
                    repository_id=repo.id,
                    name=repo.name,
                    owner=repo.owner,
                    access_level=access_level
                )
            )

        group_details.append(
            GroupDetail(
                group_id=group.id,
                name=group.name,
                display_name=group.display_name,
                ad_group=group.ad_group,
                description=group.description,
                members=members,
                repositories=repos
            )
        )

    return GroupListResponse(groups=group_details, count=len(group_details))


@router.get("/repo", response_model=RepositoryListResponse, tags=["repositories"])
def query_repositories(
    name: str = Query(None, description="Filter by repository name"),
    owner: str = Query(None, description="Filter by organization/owner"),
    db: Session = Depends(get_db)
):
    """
    Query repositories and retrieve their details, user access, and group access.

    At least one query parameter must be provided.
    """
    # Validate that at least one parameter is provided
    if not any([name, owner]):
        raise HTTPException(
            status_code=400,
            detail="At least one query parameter (name or owner) must be provided"
        )

    query = db.query(Repository)

    if name:
        query = query.filter(Repository.name.ilike(f"%{name}%"))
    if owner:
        query = query.filter(Repository.owner.ilike(f"%{owner}%"))

    repos = query.all()

    if not repos:
        return RepositoryListResponse(repositories=[], count=0)

    repo_details = []
    for repo in repos:
        # Get user access
        users = []
        for user in repo.users:
            # Get access level from association table
            stmt = db.query(user_repository_association).filter(
                user_repository_association.c.user_id == user.id,
                user_repository_association.c.repository_id == repo.id
            ).first()
            access_level = stmt[2] if stmt else "pull"

            users.append(
                UserAccessForRepo(
                    user_id=user.id,
                    github_username=user.github_username,
                    display_name=user.display_name,
                    access_level=access_level
                )
            )

        # Get group access
        groups = []
        for group in repo.groups:
            # Get access level from association table
            stmt = db.query(group_repository_association).filter(
                group_repository_association.c.group_id == group.id,
                group_repository_association.c.repository_id == repo.id
            ).first()
            access_level = stmt[2] if stmt else "pull"

            groups.append(
                GroupAccessForRepo(
                    group_id=group.id,
                    name=group.name,
                    display_name=group.display_name,
                    access_level=access_level
                )
            )

        repo_details.append(
            RepositoryDetail(
                repository_id=repo.id,
                name=repo.name,
                owner=repo.owner,
                description=repo.description,
                users=users,
                groups=groups
            )
        )

    return RepositoryListResponse(repositories=repo_details, count=len(repo_details))
