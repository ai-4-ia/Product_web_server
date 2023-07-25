from fastapi import HTTPException, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session, joinedload, relationship
from src.models import user_model
from src.schemas import user_schema
from src.core.security import get_password_hash, verify_password


def get_user_by_id(db: Session, user_id: int):
    # try:
    user = db.query(user_model.User).options(joinedload(
        user_model.User.roles)).filter(user_model.User.id == user_id).first()
    # except:
    #     raise HTTPException(status.HTTP_404_NOT_FOUND)
    return user


def get_user_by_email(db: Session, email: str):
    try:
        user = db.query(user_model.User).filter(
            user_model.User.email == email).options(joinedload(user_model.User.roles)).first()
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return user


def get_user_by_username(db: Session, username: str):
    try:
        user = db.query(user_model.User).filter(
            user_model.User.username == username).options(joinedload(user_model.User.roles)).first()
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return user


def get_all_users(db: Session):
    try:
        users = db.query(user_model.User).all()
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return users


def create_user(db: Session, user: user_schema.UserCreate):
    hased_password = get_password_hash(user.password)
    db_user = user_model.User(username=user.username, email=user.email, name=user.name,
                              phone_number=user.phone_number, hashed_password=hased_password)
    try:
        db.add(db_user)
        db.commit()
    except:
        raise HTTPException(status_code=400, detail="Can not create user")
    db.refresh(db_user)
    return db_user


def add_roles_to_user(user_id: int, roles_id: int, db: Session):
    user = db.query(user_model.User).filter(
        user_model.User.id == user_id).one()
    roles = db.query(user_model.Role).filter(
        user_model.Role.id.in_(roles_id)).all()

    if not user or not roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User or role not found")
    user.roles.extend(roles)
    db.commit()
