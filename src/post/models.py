from sqlmodel import Field, SQLModel
import uuid

class ImageBase(SQLModel):  
    user_id: uuid.UUID = Field(default=None, foreign_key="user.id")
    caption: str 
    caption_edit: str | None = None
    caption_gen: str
    
class AltTextBase(SQLModel):
    image_id: uuid.UUID = Field(default=None, foreign_key="image.id")
    alt: str 
    alt_edit: str | None = None
    alt_gen: str
    
class AltTextEdit(SQLModel):
    alt_edit: str