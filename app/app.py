from fastapi import FastAPI
from .db import create_db_and_tables
from .routers import posts, users, auth

create_db_and_tables()

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
