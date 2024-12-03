from sqlmodel import Field, SQLModel
from post.models import ImageBase, AltTextBase
import uuid

class Image(ImageBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hash: str

class AltText(AltTextBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
