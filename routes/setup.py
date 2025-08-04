import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.user import User
from schemas.admin import AdminCreate
from auth.hash import hash_password
from sqlalchemy import select

router = APIRouter(tags=["Setup"])

@router.post("/create-first-admin", status_code=status.HTTP_201_CREATED)
async def create_first_admin(admin_data: AdminCreate, db: AsyncSession = Depends(get_db)):

    if os.getenv("ALLOW_ADMIN_CREATION", "false").lower() != "true":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin creation is disabled. Set ALLOW_ADMIN_CREATION=true environment variable"
        )
    
    result = await db.execute(select(User).where(User.is_admin == True))
    if result.scalars().first():
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Admin already exists")
    
    result = await db.execute(select(User).where(User.username == admin_data.username))
    if result.scalars().first():
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered" )
    
   
    result = await db.execute(select(User).where(User.email == admin_data.email))
    if result.scalars().first():
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    
    
    
    hashed_password = hash_password(admin_data.password)
    new_admin = User(
        username=admin_data.username,
        email=admin_data.email,
        hashed_password=hashed_password,
        is_admin=True,
        is_active=True
    )
    
    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)
    
    return {
        "message": "First admin created successfully", 
        "admin_id": new_admin.id,
        "username": new_admin.username,
        "email": new_admin.email
    }