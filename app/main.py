from fastapi import FastAPI, Request
from app.routes.student import router
from app.middleware.middleware import time_counter
from app.middleware.exception_handler import exception_handler as handler

app = FastAPI(
    title="Student Management Api"
)

app.include_router(router)

app.middleware("http")(handler)  
app.middleware("http")(time_counter)
  