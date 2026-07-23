from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

dataBase = []

class Student(BaseModel):
    student_name : str
    student_id : int
    department : str
    cgpa : Optional[float] = None
    email : Optional[str] = None

@app.post("/students")
def create_student(student : Student):
    dataBase.append(student)
    return {
        "Message":"Student Data Created Successfully!!",
        "Student":student
    }
