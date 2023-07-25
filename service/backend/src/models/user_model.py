"""_summary_: Model for SQLALCHEMY
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped
from typing import List

from src.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    hashed_password = Column(String)
    phone_number = Column(Integer)
    is_activate = Column(Boolean, default=True)
    roles = relationship(
        "Role", secondary="user_role", back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    users = relationship(
        "User", secondary="user_role", back_populates="roles")


class UserRole(Base):
    __tablename__ = "user_role"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
