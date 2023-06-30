from fastapi import HTTPException
from sqlalchemy.orm import Session
from src import models, schemas


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_all_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password+"willbehashlater"
    db_user = models.User(email=user.email, name=user.name,
                          phone_number=user.phone_number, hashed_password=fake_hashed_password)
    try:
        db.add(db_user)
        db.commit()
    except:
        raise HTTPException(status_code=400, detail="Can not create user")
    db.refresh(db_user)
    return db_user
