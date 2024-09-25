from sqlmodel import Field
from auth.models import UserBase

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str