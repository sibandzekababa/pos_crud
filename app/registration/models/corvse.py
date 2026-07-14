from sqlalchemy import Column, Integer, String
from database import Base

class CourseModel(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    code = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    department = Column(String, nullable=False)
    max_capacity = Column(Integer, nullable=False)
