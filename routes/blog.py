from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.blog import Blog
from schemas.blog import BlogCreate, BlogOut, BlogOutput
from typing import List
from auth.jwt_handler import get_current_user
from models.user import User 
from openai import OpenAI
import os

router = APIRouter(prefix="/blogs", tags=["Blogs"])

client = OpenAI(api_key=os.getenv("Chabi"))

@router.post("/", response_model=BlogOut)
async def create_blog(blog: BlogCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_blog = Blog(title=blog.title, content=blog.content, user_id=current_user.id)
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog

@router.get("/", response_model=List[BlogOut])
async def get_blogs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog))
    return result.scalars().all()

@router.get("/{blog_id}", response_model=BlogOut)
async def get_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.put("/{blog_id}", response_model=BlogOut)
async def update_blog(blog_id: int, updated: BlogCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if not blog or blog.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not authorized or blog not found")

    blog.title = updated.title
    blog.content = updated.content
    await db.commit()
    await db.refresh(blog)
    return blog

@router.delete("/{blog_id}")
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if not blog or blog.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not authorized or blog not found")
    await db.delete(blog)
    await db.commit()
    return {"message": "Blog deleted"}



@router.post("/write_blog")
async def Ai_Blog(blog:BlogOutput, db:AsyncSession = Depends(get_db), current_user:User = Depends(get_current_user)):
    response=client.responses.create(
        model="gpt-4.1",
        input= f"Write a blog of 200 words on this topic: {blog.title}"
    )
    text = response.output_text

    ai_blog = Blog(title=blog.title, user_id=current_user.id, content=text)
    db.add(ai_blog)
    await db.commit()
    await db.refresh(ai_blog)
    return {"success":True}
    
    

