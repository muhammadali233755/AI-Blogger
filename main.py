from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from routes import auth, blog, comment, admin, like, setup
from async_timeout import timeout
import os
print(os.getenv("Chabi"))



@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with timeout(10.0): 
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        yield
    except Exception as e:
        print(f"Startup failed: {str(e)}")
        await engine.dispose()
        raise


app = FastAPI(title="Ai Blogger", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(comment.router)
app.include_router(admin.router)
app.include_router(like.router)
app.include_router(setup.router)



