from datetime import datetime
from pydantic import BaseModel, ConfigDict

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

