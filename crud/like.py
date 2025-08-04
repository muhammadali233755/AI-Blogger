from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.like import Like
from schemas.like import LikeCreate
from fastapi import HTTPException, status


async def create_like(db: AsyncSession, like_data: LikeCreate) -> Like:
    try:
        like = Like(**like_data.model_dump())
        db.add(like)
        await db.commit()
        await db.refresh(like)
        return like
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not create like: {str(e)}")


async def delete_like(db: AsyncSession, blog_id: int, user_id: int) -> bool:
  
    try:
        result = await db.execute(
            select(Like)
            .where(Like.blog_id == blog_id)
            .where(Like.user_id == user_id)
        )
        like = result.scalar_one_or_none()
        
        if not like:
            return False
            
        await db.delete(like)
        await db.commit()
        return True
        
    except Exception as e:
        await db.rollback()
        raise  


async def get_like(db: AsyncSession, blog_id: int, user_id: int) -> Like | None:
    result = await db.execute(select(Like).where(Like.blog_id == blog_id).where(Like.user_id == user_id))
    return result.scalar_one_or_none()