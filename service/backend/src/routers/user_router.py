from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import timedelta


from src.crud import user_crud
from src.schemas import user_schema, token_schema
from src.routers.dep import get_db, oauth2_scheme, authenticate_user, admin_role, user_role
from src.core.security import create_access_token
from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/users")


@router.get("/admin")
async def test_admin(current_user=Depends(admin_role)):
    return "hello admin"


@router.get("/by_id/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(dependency=get_db)):
    user = user_crud.get_user_by_id(db, user_id)
    if (user is None):
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.get("/by_email/{user_email}")
async def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, user_email)
    if (user is None):
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.get("/")
async def get_all_users(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    user = user_crud.get_all_users(db)
    if (user is None):
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.get("/user")
async def test_user(current_user=Depends(user_role)):
    return "hello user"


@router.post("/create_user", response_model=user_schema.User)
async def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.create_user(db, user)
    if (user is None):
        raise HTTPException(status_code=400, detail="Can not create user")
    else:
        return user


@router.post("/token", response_model=token_schema.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):

    user = authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password", header={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return token_schema.Token(access_token=access_token, token_type="bearer")


@router.put("add_roles_to_user", response_model=user_schema.User)
async def add_roles_to_user(user_id: int, roles_id: list[int], db: Session = Depends(get_db)):
    user = user_crud.add_roles_to_user(user_id, roles_id, db)
    if (user is None):
        raise HTTPException(status_code=400, detail="Can not add role to user")
    else:
        return user
