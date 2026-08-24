from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database.database import Base,get_db,engine
from schemas.students import Student, StudentUpdate, StudentResponse
from models.models import Student as StudentModel

Base.metadata.create_all(engine)

router = APIRouter(
    prefix="/students",
    tags=["Student"]
)

@router.post("/",status_code=201)
def create_student(
                    student : Student,
                    db : Session = Depends(get_db)
                   ):
    student_obj = StudentModel(
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

@router.get("/{student_id}",response_model=StudentResponse)
def get_student(
    student_id : int,
    db : Session = Depends(get_db)
    ):

    student = db.get(StudentModel,student_id)

    if student == None :     
        raise HTTPException(
            status_code=404,
            detail="Student Not Found!!"
        )

    return student

@router.put("/{student_id}")
def update_student(
                   update_student:StudentUpdate,
                   student_id:int, 
                   db : Session = Depends(get_db)
                   ):


    student = db.get(StudentModel,student_id)

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

@router.delete("/{student_id}")
def delete_student(
                    student_id:int,
                    db : Session = Depends(get_db)
                   ):

    student = db.get(StudentModel,student_id)

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