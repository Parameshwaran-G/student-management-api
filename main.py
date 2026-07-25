from fastapi import FastAPI,HTTPException
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

class StudentUpdate(BaseModel):
    student_name : Optional[str] = None
    department : Optional[str] = None
    cgpa : Optional[float] = None
    email : Optional[str] = None

# create student
@app.post("/students")
def create_student(student : Student):
    dataBase.append(student)
    return {
        "Message":"Student Data Created Successfully!!",
        "Student":student
    }

# get student by id
@app.get("/students/{student_id}")
def get_student(student_id : int):
    for student in dataBase:
        if student.student_id == student_id :
            return {
                "Message":"Student Found Successfully!!",
                "Student":student
            }
    raise HTTPException(
        status_code=404,
        detail="Student Not Found!!"
    )

# return students of same group (filter by group)
@app.get("/students")
def filter_student(student_dept:str):
    filtered_students = []
    for student in dataBase:
        if student.department == student_dept :
            filtered_students.append(student.student_name)
    if len(filtered_students) == 0 :
        raise HTTPException(
            status_code=404,
            detail="Department Does Not Found!!"
        )
    return {
        "Department":student_dept,
        "Students":filtered_students
    }

