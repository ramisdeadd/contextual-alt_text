from sqlmodel import Field, SQLModel
from pydantic import BaseModel
from auth.models import UserBase
from typing import Generic, TypeVar, List

T = TypeVar("T", bound=SQLModel)

MAX_RESULTS_PER_PAGE = 50

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class PaginationInput(BaseModel):
    page: int = Field(default=1, ge=1, description="Requested Page Number")
    page_size: int = Field(
        default=5,
        ge=1,
        le=MAX_RESULTS_PER_PAGE,
        description="Requested Number of Items Per Page"
    )

class AltCapPage(BaseModel, Generic[T]):
    images: list[T] = Field(description="List of images in one page")
    alttext: list[T] = Field(description="List of alt-text in one page")
    total_items: int = Field(ge=0, description="Number of total items")
    start_index: int = Field(ge=0, description="Starting item index")
    end_index: int = Field(ge=0, description="Ending item index")
    total_pages: int = Field(ge=0, description="Total number of pages")
    current_page: int = Field(ge=0, description="Page Number")
    current_page_size: int = Field(ge=0, description="Number of items per page")

class UserPage(BaseModel, Generic[T]):
    users: list[T] = Field(description="List of users in one page")
    total_items: int = Field(ge=0, description="Number of total items")
    start_index: int = Field(ge=0, description="Starting item index")
    end_index: int = Field(ge=0, description="Ending item index")
    total_pages: int = Field(ge=0, description="Total number of pages")
    current_page: int = Field(ge=0, description="Page Number")
    current_page_size: int = Field(ge=0, description="Number of items per page")
