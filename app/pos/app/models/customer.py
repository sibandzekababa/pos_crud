from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = "customer_table"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(36), nullable=True)
    phone = Column(String(20), nullable=True)
    loyalty_points = Column(Integer, nullable=False, default=0)

    sales = relationship("Sale", back_populates="customer")
