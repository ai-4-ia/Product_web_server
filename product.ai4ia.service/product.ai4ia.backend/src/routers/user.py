from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from src import crud, schemas
from src.routers.dep import get_db, oauth2_scheme

router = APIRouter(prefix="/users")


@router.get("/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(dependency=get_db)):
    user = crud.user.get_user_by_id(db, user_id)
    if (user is None):
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.get("/{user_email}")
async def get_user_by_id(user_email: str, db: Session = Depends(get_db)):
    user = crud.user.get_user_by_email(db, user_email)
    if (user is None):
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.get("/")
async def get_all_users(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    user = crud.user.get_all_users(db)
    if (user is None):
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.user.create_user(db, user)
    if (user is None):
        raise HTTPException(status_code=400, detail="Can not create user")
    else:
        return user
