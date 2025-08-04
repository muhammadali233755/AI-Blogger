# routes/comment.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.comment import Comment
from schemas.comment import CommentCreate, CommentOut
from auth.jwt_handler import get_current_user
from models.user import User
from typing import List

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentOut)
async def create_comment(comment: CommentCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_comment = Comment(text=comment.text, blog_id=comment.blog_id, user_id=current_user.id)
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment

@router.get("/", response_model=List[CommentOut])
async def get_comments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Comment))
    return result.scalars().all()

@router.get("/{comment_id}", response_model=CommentOut)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.put("/{comment_id}", response_model=CommentOut)
async def update_comment(comment_id: int, comment: CommentCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    db_comment = result.scalar_one_or_none()
    if not db_comment or db_comment.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not authorized or comment not found")
    
    db_comment.text = comment.text
    db_comment.blog_id = comment.blog_id
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment or comment.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not authorized or comment not found")
    
    await db.delete(comment)
    await db.commit()
    return {"message": "Comment deleted"}
