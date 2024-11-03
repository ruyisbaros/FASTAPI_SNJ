import time

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:ahmet@localhost/fastapi_snj"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# POSTGRES DB CONNECT IF WE WORK WITH VANILLA SQL
""" while True:
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
        time.sleep(2) """
