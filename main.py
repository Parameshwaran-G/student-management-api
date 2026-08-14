from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from typing import Optional
from database import engine, Base, get_db
from sqlalchemy.orm import Session
import models

Base.metadata.create_all(engine)
app = FastAPI()

dataBase = []

class Student(BaseModel):
    student_name : str = Field(
        ...,
        min_length=3,
        max_length=25,
        description="Student Name",
        example="Praneshwaran S"
    )
    student_id : int = Field(
        ...,
        description="Student Id",
        example="114"
    )
    department : str = Field(
        ...,
        description="Student Department",
        example="CSE"
    )
    cgpa : float = Field(
        default="0.0",
        ge=0,
        le=10,
        description="Student CGPA",
        example="8.45"
    )
    email : str = Field(
        default="student@gmail.com",
        description="Student Email",
        example="abc@gmail.com"
    )

class StudentUpdate(BaseModel):
    student_name : Optional[str] = None
    department : Optional[str] = None
    cgpa : Optional[float] = None
    email : Optional[str] = None

# response model
class Student_Response(BaseModel):
    student_name : str
    department : str
    cgpa : float
    email : str

# create student
@app.post("/students",status_code=201)
def create_student(
                    student : Student,
                    db : Session = Depends(get_db)
                   ):
    student_obj = models.Student(
        student_name = student.student_name,
        student_id = student.student_id,
        department = student.department,
        cgpa = student.cgpa,
        email = student.email
    )
    db.add(student_obj)
    db.commit()
    db.refresh(student_obj)

    return {
        "Message":"Student Data Created Successfully!!",
        "Student":student
    }

# get student by id
@app.get("/students/{student_id}",response_model=Student_Response)
def get_student(
    student_id : int,
    db : Session = Depends(get_db)
    ):

    student = db.get(models.Student,student_id)

    if student == None :     
        raise HTTPException(
            status_code=404,
            detail="Student Not Found!!"
        )

    return student

# return students of same group (filter by group)
# query parameter validation
@app.get("/students")
def filter_student(
    student_dept : Optional[str] = None,
    cgpa : float = Query(None,ge=0,le=10)
    ):
    filtered_students = []
    for student in dataBase:
        if (student_dept==None or student.department == student_dept) and \
           (cgpa == None or student.cgpa == cgpa) :
            filtered_students.append(student)
    if len(filtered_students) == 0 :
        raise HTTPException(
            status_code=404,
            detail="Student Not Found!!"
        )
    return filtered_students

# update student information
@app.put("/students/{student_id}")
def update_student(
                   update_student:StudentUpdate,
                   student_id:int, 
                   db : Session = Depends(get_db)
                   ):


    student = db.get(models.Student,student_id)

    if student is None :
        raise HTTPException(
                status_code=404,
                detail="Student Not Found!!"
            )

    updated_student = update_student.model_dump(exclude_none=True)
    for key,value in updated_student.items():
        setattr(student,key,value)

    db.commit()

    return {
        "Message":"Student Details Updated Successfully!!",
        "Student":updated_student
    }
    

# delete student record
@app.delete("/students/{student_id}")
def delete_student(
                    student_id:int,
                    db : Session = Depends(get_db)
                   ):

    student = db.get(models.Student,student_id)

    if student is None :
        raise HTTPException(
            status_code=404,
            detail="Student Not Found!!"
        )

    db.delete(student)
    db.commit()

    return {
        "Message":"Student Removed Successfully !!"
    }