from sqlalchemy import Column, Integer, String
from database import Base  # Assuming you have a SQLAlchemy Base setup

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    country = Column(String, nullable=False)
    id_number = Column(Integer, nullable=False)
