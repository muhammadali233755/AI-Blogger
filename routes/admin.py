from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import async_session, get_db
from models.user import User
from schemas.user import UserOut, UserUpdate
from schemas.blog import BlogCreate, BlogOut, BlogUpdate
from schemas.comment import CommentOut
from schemas.admin import AdminPrivilegeUpdate
from crud import user as user_crud, blog as blog_crud, comment as comment_crud
from auth.dependencies import get_current_admin_user
from sqlalchemy import select

router = APIRouter(prefix="/admin", tags=["Admin Panel"])


@router.get("/users/", response_model=List[UserOut])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    return await user_crud.get_all_users(db)


@router.patch("/users/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    return await user_crud.update_user(db, user_id, user_update)


@router.patch("/users/{user_id}/admin-privilege", response_model=UserOut)
async def update_admin_privilege(
    user_id: int,
    privilege_update: AdminPrivilegeUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.is_admin = privilege_update.is_admin
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    return await user_crud.delete_user(db, user_id)


@router.get("/blogs/", response_model=List[BlogOut])
async def get_all_blogs(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    return await blog_crud.get_all_blogs(db)


@router.post("/blogs/", response_model=BlogOut)
async def create_blog(
    blog: BlogCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    return await blog_crud.create_blog(db, blog, admin.id)


@router.patch("/blogs/{blog_id}", response_model=BlogOut)
async def update_blog(
    blog_id: int,
    blog_update: BlogUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    return await blog_crud.update_blog(db, blog_id, blog_update)


@router.delete("/blogs/{blog_id}")
async def delete_blog(
    blog_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    return await blog_crud.delete_blog(db, blog_id)


@router.get("/comments/", response_model=List[CommentOut])
async def get_all_comments(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    return await comment_crud.get_all_comments(db)


@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    return await comment_crud.delete_comment(db, comment_id)
