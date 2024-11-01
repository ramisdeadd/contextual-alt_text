from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    username: str = Field(index=True)
    first_name: str
    last_name: str
    email: str = Field(unique=True)
    disabled: bool = Field(default=False)

class UserUpdate(SQLModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    disabled: bool | None = None

class UserPasswordUpdate(UserUpdate):
    hashed_password: str | None = None

class UserCreate(UserBase):
    hashed_password: str

class UserPublic(UserBase):
    id: int
