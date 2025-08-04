from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.comment import Comment

async def get_all_comments(db: AsyncSession):
    result = await db.execute(select(Comment))
    return result.scalars().all()

async def delete_comment(db: AsyncSession, comment_id: int):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise Exception("Comment not found")
    await db.delete(comment)
    await db.commit()
    return {"detail": "Comment deleted"}
