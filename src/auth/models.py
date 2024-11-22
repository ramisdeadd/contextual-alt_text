from sqlmodel import Field, SQLModel
from pydantic import BaseModel
from typing import Generic, TypeVar, List

MAX_RESULTS_PER_PAGE = 50

# Generic Class -> Specifying that the base must be SQLModel
T = TypeVar("T", bound=SQLModel)

class UserBase(SQLModel):
    username: str = Field(index=True)
    first_name: str
    last_name: str
    email: str = Field(unique=True)
    disabled: bool = Field(default=False)
    role: str = Field(default="user")

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

class PaginationInput(BaseModel):
    page: int = Field(default=1, ge=1, description="Requested Page Number")
    page_size: int = Field(
        default=10,
        ge=1,
        le=MAX_RESULTS_PER_PAGE,
        description="Requested Number of Items Per Page"
    )

class Page(BaseModel, Generic(T)):
    items: list[T] = Field(description="List of items in one page")
    total_items: int = Field(ge=0, description="Number of total items")
    start_index: int = Field(ge=0, description="Starting item index")
    end_index: int = Field(ge=0, description="Ending item index")
    total_pages: int = Field(ge=0, description="Total number of pages")
    current_page: int = Field(ge=0, description="Page Number")
    current_page_size: int = Field(ge=0, description="Number of items per page")
