from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "category_table"
    
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), nullable=False)
    category_description = Column(String, nullable=True)

    products = relationship("Product", back_populates="category")
