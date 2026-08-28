from app.schemas.students import Student
from sqlalchemy.orm import Session
from app.models.models import Student as StudentModel
from app.repositories.student import create_student as create_student_repo
from app.repositories.student import get_students as get_student_repo
from app.repositories.student import update_student as update_student_repo
from app.repositories.student import delete_student as delete_student_repo

def create_student(student : Student , db : Session):
    student_obj = StudentModel(
        student_name = student.student_name,
        student_id = student.student_id,
        department = student.department,
        cgpa = student.cgpa,
        email = student.email
    )

    return create_student_repo(db,student_obj)
    
def get_student(student_id : int, db: Session):
    return get_student_repo(db,student_id)

def update_student(student_id : int, db : Session, update_student : Student):
    student = get_student_repo(db,student_id)

    if student is None :
        return None

    update_object = update_student.model_dump(exclude_none=True)
    for key,value in update_object.items():
        setattr(student,key,value)

    return update_student_repo(db,student)

def delete_student(student_id : int, db : Session):
    student = get_student_repo(db,student_id)
    if student is None :
        return None
    
    return delete_student_repo(db,student)
