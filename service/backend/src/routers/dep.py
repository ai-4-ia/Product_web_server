from typing import Generator, Annotated
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session, joinedload
from jose import jwt, JWTError
from pydantic import ValidationError

from src.core.security import verify_password
from src.db.database import SessionLocal
from src.core.config import SECRET_KEY, ALGORITHM
from src.models import user_model
from src.schemas import token_schema
from src.crud import user_crud


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token",
                                     scheme_name="JWT",
                                     scopes={"administrator": "master of the sofware", "user": "the customer who use this software"})


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def authenticate_user(db: Session, username, password):
    matched_user = db.query(user_model.User).filter(
        user_model.User.username == username).options(joinedload(user_model.User.roles)).first()
    if not matched_user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    if not verify_password(password, matched_user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return matched_user


def get_current_user(security_scopes: SecurityScopes, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = user_crud.get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception

    # Check permission
    user_scopes = [role.name for role in user.roles]
    intersection_scope = set(user_scopes).intersection(security_scopes.scopes)
    if not intersection_scope:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permission",
            headers={"WWW-Authenticate": authenticate_value}
        )
    return user


def get_current_activate_user(current_user: Annotated[user_model.User, Security(get_current_user)]):
    if current_user.is_activate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactivate user")
    return current_user


def admin_role(current_user: Annotated[user_model.User, Security(get_current_user, scopes=["administrator"])]):
    return current_user


def user_role(current_user: Annotated[user_model.User, Security(get_current_user, scopes=["administrator", "user"])]):
    return current_user
