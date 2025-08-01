from pydantic import BaseModel, EmailStr

class AdminCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class AdminPrivilegeUpdate(BaseModel):
    user_id: int
    is_admin: bool