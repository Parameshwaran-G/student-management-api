from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

class Student(Base):
    __tablename__ = "Student"

    student_name : Mapped[str]
    student_id : Mapped[int] = mapped_column(primary_key=True)
    department : Mapped[str]
    cgpa : Mapped[float] = mapped_column(nullable=False)
    email : Mapped[str]
