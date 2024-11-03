from fastapi import FastAPI

from . import models

# from .config import settings
from .database import engine
from .routers import authRoutes, postRoutes, userRoutes

# LOCAL SERVER
app = FastAPI()

# RUNS ORM
models.Base.metadata.create_all(bind=engine)


### SET ROUTES
app.include_router(postRoutes.router)
app.include_router(userRoutes.router)
app.include_router(authRoutes.router)
