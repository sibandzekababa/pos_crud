from sqlalchemy import Column, Integer, String, Float
from database import Base

class TeacherModel(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    department = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    id_number = Column(Integer, nullable=False)
