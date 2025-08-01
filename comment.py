from pydantic import BaseModel, ConfigDict

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    blog_id: int

class CommentOut(CommentBase):
    id: int
    user_id: int
    blog_id: int

    model_config = ConfigDict(from_attributes=True)
