from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from models.like import Like
from schemas.like import LikeCreate, LikeResponse
from database import get_db, AsyncSession
from crud.like import create_like, delete_like, get_like
from auth.jwt_handler import get_current_user
from models.user import User
from models.blog import Blog
from sqlalchemy import select


router = APIRouter(prefix="/blogs/{blog_id}/likes", tags=["likes"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=LikeResponse)
async def create_like_endpoint(
    blog_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    existing_like = await get_like(db, blog_id, current_user.id)
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already liked this blog"
        )
    
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    

    like_data = LikeCreate(blog_id=blog_id, user_id=current_user.id)
    try:
        new_like = await create_like(db, like_data)
        return new_like
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Failed to create like: {str(e)}")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_like_endpoint(blog_id: int,current_user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    try:
        deleted = await delete_like(db, blog_id, current_user.id)
        if not deleted:
            raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException( status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete like: {str(e)}")