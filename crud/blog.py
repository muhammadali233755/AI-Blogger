from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.blog import Blog
from schemas.blog import BlogCreate, BlogUpdate
from starlette import status

async def get_all_blogs(db: AsyncSession):
    result = await db.execute(select(Blog))
    return result.scalars().all()

async def create_blog(db: AsyncSession, blog: BlogCreate, user_id: int):
    new_blog = Blog(**blog.model_dump(), user_id=user_id)
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog



async def update_blog(db: AsyncSession, blog_update: BlogUpdate, blog_id: int) -> Blog:
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog not found")

    update_data = blog_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(blog, key, value)

    await db.commit()
    await db.refresh(blog)
    return blog



async def delete_blog(db: AsyncSession, blog_id: int):
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise Exception("Blog not found")
    await db.delete(blog)
    await db.commit()
    return {"detail": "Blog deleted"}
