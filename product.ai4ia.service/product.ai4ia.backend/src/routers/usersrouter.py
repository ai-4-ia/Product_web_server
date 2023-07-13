from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime, timedelta
from src import crud, schemas
from src.routers.dep import get_db, oauth2_scheme
from src.core.security import create_access_token
from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/users")


@router.get("/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(dependency=get_db)):
    user = crud.usercrud.get_user_by_id(db, user_id)
    if (user is None):
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.get("/{user_email}")
async def get_user_by_id(user_email: str, db: Session = Depends(get_db)):
    user = crud.usercrud.get_user_by_email(db, user_email)
    if (user is None):
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.get("/")
async def get_all_users(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    user = crud.usercrud.get_all_users(db)
    if (user is None):
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.usercrud.create_user(db, user)
    if (user is None):
        raise HTTPException(status_code=400, detail="Can not create user")
    else:
        return user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):

    user = crud.usercrud.authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password", header={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return schemas.Token(access_token=access_token, token_type="bearer")
