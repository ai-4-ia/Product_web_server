"""_summary_: Pydantic Model, use to store data in backend
"""

from pydantic import BaseModel


class UserBase(BaseModel):
    """The base schema for user without password

    Args:
        BaseModel (_type_): _description_
    """
    username: str
    email: str
    name: str
    phone_number: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_activate: bool
    roles: list

    class Config:
        from_attributes = True
