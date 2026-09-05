from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database.database import Base,get_db,engine
from app.schemas.students import Student, StudentUpdate, StudentResponse
from app.services.student import create_student as create_student_service
from app.services.student import get_student as get_student_service
from app.services.student import update_student as update_student_service
from app.services.student import delete_student as delete_student_service

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

    return create_student_service(student,db)

@router.get("/{student_id}",response_model=StudentResponse)
def get_student(
    student_id : int,
    db : Session = Depends(get_db)
    ):

    student = get_student_service(student_id,db)

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

    updated_student = update_student_service(student_id,db,update_student)

    if updated_student is None :
        raise HTTPException(
                status_code=404,
                detail="Student Not Found!!"
            )

    return {
        "Message":"Student Details Updated Successfully!!",
        "Student":updated_student
    }

@router.delete("/{student_id}")
def delete_student(
                    student_id:int,
                    db : Session = Depends(get_db)
                   ):

    student = delete_student_service(student_id,db)
    if student is None :
        raise HTTPException(
            status_code=404,
            detail="Student Not Found!!"
        )

    return {
        "Message":"Student Removed Successfully !!"
    }

@router.get("/test/error")
def test_error():
    result = 10 / 0
    return result

@router.get("/test/type")
def test_type():
    result = "result"-0
    return result