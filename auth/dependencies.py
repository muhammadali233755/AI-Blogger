from fastapi import Depends, HTTPException, status 
from models.user import User
from auth.jwt_handler import get_current_user  
from database import get_db , AsyncSession



async def get_current_admin_user(
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)) -> User:
        
    refreshed_user = await db.get(User, current_user.id)
    
    if not refreshed_user or not refreshed_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return refreshed_user
