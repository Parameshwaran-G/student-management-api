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

# response model
class Student_Response(BaseModel):
    student_name : str
    department : str
    cgpa : float

# create student
@app.post("/students",status_code=201)
def create_student(student : Student):
    dataBase.append(student)
    return {
        "Message":"Student Data Created Successfully!!",
        "Student":student
    }

# get student by id
@app.get("/students/{student_id}",response_model=Student_Response)
def get_student(student_id : int):
    for student in dataBase:
        if student.student_id == student_id :
            return student
            
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

# update student information
@app.put("/students/{student_id}")
def update_student(update_student:StudentUpdate,student_id:int):
    for student in dataBase:
        if student.student_id == student_id:
            updated_model = update_student.model_dump(exclude_none=True)
            for key,value in updated_model.items():
                setattr(student,key,value)
            return{
                "Message":"Student Updated Successfully!!"
            }
    raise HTTPException(
        status_code=404,
        detail="Student Not Found!!"
    )

# delete student record
@app.delete("/students/{student_id}")
def delete_student(student_id:int):
    for student in dataBase:
        if student.student_id == student_id :
            dataBase.remove(student)
            return {
                "Message":"Student Data Deleted Successfully!!"
            }
    raise HTTPException(
        status_code=404,
        detail="Student Not Found!!"
    )