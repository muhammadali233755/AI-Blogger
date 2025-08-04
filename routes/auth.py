from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserOut
from schemas.token import Token
from auth.hash import hash_password, verify_password
from auth.jwt_handler import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Auth"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(User).where(User.username == user.username))
    existing_user = query.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
   
    query = await db.execute(select(User).where(User.email == user.email))
    existing_user = query.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_pw,
        is_admin=user.is_admin
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    
    query = await db.execute(select(User).where(User.username == form_data.username))
    user = query.scalar_one_or_none()
    
  
    if not user:
        query = await db.execute(select(User).where(User.email == form_data.username))
        user = query.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail="User account is disabled")
    
    access_token = create_access_token(user)
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "is_admin": user.is_admin
    }