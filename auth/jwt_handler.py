from datetime import datetime, timedelta
from jose import JWTError, jwt
from schemas.token import TokenData
from fastapi import HTTPException, Depends , status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.user import User
from sqlalchemy import select
  
SECRET_KEY = "supersecretkey"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(user: User):  
    to_encode = { "sub": user.email,  "is_admin": user.is_admin,  "id": str(user.id) }
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin")
        user_id: str = payload.get("id")
        
        if not email or not user_id:
            raise credentials_exception
            
        token_data = TokenData(email=email,is_admin=is_admin,id=user_id)
    except JWTError:
        raise credentials_exception

    
    query = await db.execute(select(User).where(User.email == token_data.email))
    user = query.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
        
    if user.is_admin != token_data.is_admin or str(user.id) != token_data.id:
        raise HTTPException( status_code=401,detail="User privileges changed - please reauthenticate")
        return user
