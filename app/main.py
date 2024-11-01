import time

import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine
from .routers import postRoutes, userRoutes

# LOCAL SERVER
app = FastAPI()

# RUNS ORM
models.Base.metadata.create_all(bind=engine)


# POSTGRES DB CONNECT
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi_snj",
            user="postgres",
            password="ahmet",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection established successfully")
        break

    except (Exception, psycopg2.DatabaseError) as e:
        print("Error with connecting to database")
        print("Error: %s" % e)
        time.sleep(2)


### SET ROUTES
app.include_router(postRoutes.router)
app.include_router(userRoutes.router)
