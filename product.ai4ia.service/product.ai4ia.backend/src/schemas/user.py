"""_summary_: Pydantic Model, use to store data in backend
"""

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str
    phone_number: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_activate: bool

    class Config:
        orm_mode = True
