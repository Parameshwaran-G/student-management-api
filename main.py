from fastapi import FastAPI
from routes.student import router

app = FastAPI(
    title="Student Management Api"
)

app.include_router(router)