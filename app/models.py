from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

# Association tables for many-to-many relationships

user_group_association = Table(
    'user_group_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

user_repository_association = Table(
    'user_repository_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('repository_id', Integer, ForeignKey('repositories.id')),
    Column('access_level', String(50))
)

group_repository_association = Table(
    'group_repository_association',
    Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id')),
    Column('repository_id', Integer, ForeignKey('repositories.id')),
    Column('access_level', String(50))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    ad_id = Column(String(255), unique=True, nullable=False)
    github_username = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    job_title = Column(String(255), nullable=False)
    team = Column(String(255), nullable=False)
    active = Column(Integer, default=1)

    groups = relationship(
        'Group',
        secondary=user_group_association,
        back_populates='users'
    )
    repositories = relationship(
        'Repository',
        secondary=user_repository_association,
        back_populates='users'
    )


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    ad_group = Column(String(255), nullable=False)
    description = Column(String(1000))

    users = relationship(
        'User',
        secondary=user_group_association,
        back_populates='groups'
    )
    repositories = relationship(
        'Repository',
        secondary=group_repository_association,
        back_populates='groups'
    )


class Repository(Base):
    __tablename__ = 'repositories'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    owner = Column(String(255), nullable=False)
    description = Column(String(1000))

    users = relationship(
        'User',
        secondary=user_repository_association,
        back_populates='repositories'
    )
    groups = relationship(
        'Group',
        secondary=group_repository_association,
        back_populates='repositories'
    )

    __table_args__ = (
        # Ensure unique repository per owner
        # Can have multiple repos with same name in different orgs
    )
