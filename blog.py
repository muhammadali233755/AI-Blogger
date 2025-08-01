from pydantic import BaseModel, ConfigDict
from typing import Optional

class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class BlogOut(BlogBase):
    id: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)

class BlogUpdate(BaseModel):
    title: Optional[str] = None   
    content: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
    
class BlogOutput(BaseModel):
    title: str
    
    model_config = ConfigDict(from_attributes=True)

