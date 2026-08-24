from pydantic import BaseModel, Field
from typing import Optional

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

class StudentResponse(BaseModel):
    student_name : str
    department : str
    cgpa : float
    email : str
