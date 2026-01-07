from contextlib import asynccontextmanager 
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
from app.database import engine 
from app.models import Base 
from app.routers import users, projects, courses

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(courses.router)

 
#Replacing @app.on_event("startup") 
@asynccontextmanager 
async def lifespan(app: FastAPI): 
    Base.metadata.create_all(bind=engine)    
    yield 
 
app = FastAPI(lifespan=lifespan) 
 
# CORS (add this block) 
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["*"],   # dev-friendly; tighten in prod 
    allow_methods=["*"], 
    allow_headers=["*"], 
) 