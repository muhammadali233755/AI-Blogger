from pydantic import BaseModel, ConfigDict
from datetime import datetime

class LikeBase(BaseModel):
    blog_id: int
    user_id: int

class LikeCreate(LikeBase):
    pass

class LikeResponse(LikeBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)





