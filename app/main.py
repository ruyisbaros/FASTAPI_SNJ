from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models

# from .config import settings
from .database import engine
from .routers import authRoutes, postRoutes, userRoutes, voteRoutes

# LOCAL SERVER
app = FastAPI()

# CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RUNS ORM
# I use Alembic so I disabled below
# models.Base.metadata.create_all(bind=engine)


### SET ROUTES
app.include_router(postRoutes.router)
app.include_router(userRoutes.router)
app.include_router(authRoutes.router)
app.include_router(voteRoutes.router)
