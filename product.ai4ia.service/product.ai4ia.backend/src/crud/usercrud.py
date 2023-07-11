from fastapi import HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from src import models, schemas
from src.core.security import get_password_hash, verify_password


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filet(models.User.username == username).first()


def get_all_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    hased_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, name=user.name,
                          phone_number=user.phone_number, hashed_password=hased_password)
    try:
        db.add(db_user)
        db.commit()
    except:
        raise HTTPException(status_code=400, detail="Can not create user")
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username, password):
    matched_user = db.query(models.User).filter(
        models.User.username == username).first()
    if not matched_user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    if not verify_password(password, matched_user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return matched_user
