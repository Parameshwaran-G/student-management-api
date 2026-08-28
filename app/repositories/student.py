from sqlalchemy.orm import Session
from app.models.models import Student as StudentModel

def create_student(
        db : Session,
        student : StudentModel
):
    db.add(student)
    db.commit()
    db.refresh(student)

    return student

def get_students(
        db : Session,
        student_id : int
):
    student = db.get(StudentModel , student_id)

    return student

def update_student(
        db : Session,
        student : StudentModel
):
    db.commit()
    db.refresh(student)

    return student

def delete_student(
        db : Session,
        student : StudentModel
):
    db.delete(student)
    db.commit()

    return student
