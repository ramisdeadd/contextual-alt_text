from sqlmodel import Field, SQLModel
from post.models import ImageBase, AltTextBase

class Image(ImageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hash: str

class AltText(AltTextBase, table=True):
    id: int | None = Field(default=None, primary_key=True)