from pydantic import BaseModel
from typing import List, Optional


class RepositoryAccessInfo(BaseModel):
    repository_id: int
    name: str
    owner: str
    access_level: str


class GroupInfo(BaseModel):
    group_id: int
    name: str
    display_name: str


class UserDetail(BaseModel):
    user_id: int
    ad_id: str
    github_username: str
    display_name: str
    email: str
    job_title: str
    team: str
    groups: List[GroupInfo]
    repositories: List[RepositoryAccessInfo]


class UserListResponse(BaseModel):
    users: List[UserDetail]
    count: int


class UserMemberInfo(BaseModel):
    user_id: int
    ad_id: str
    github_username: str
    display_name: str
    email: str
    job_title: str
    team: str


class RepositoryAccessForGroup(BaseModel):
    repository_id: int
    name: str
    owner: str
    access_level: str


class GroupDetail(BaseModel):
    group_id: int
    name: str
    display_name: str
    ad_group: str
    description: Optional[str]
    members: List[UserMemberInfo]
    repositories: List[RepositoryAccessForGroup]


class GroupListResponse(BaseModel):
    groups: List[GroupDetail]
    count: int


class UserAccessForRepo(BaseModel):
    user_id: int
    github_username: str
    display_name: str
    access_level: str


class GroupAccessForRepo(BaseModel):
    group_id: int
    name: str
    display_name: str
    access_level: str


class RepositoryDetail(BaseModel):
    repository_id: int
    name: str
    owner: str
    description: Optional[str]
    users: List[UserAccessForRepo]
    groups: List[GroupAccessForRepo]


class RepositoryListResponse(BaseModel):
    repositories: List[RepositoryDetail]
    count: int
