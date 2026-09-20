from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Supplier(Base):
    __tablename__ = "supplier_table"
    
    supplier_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(50), nullable=False)
    contact_name = Column(String(36), nullable=True)
    supplier_phoneNumber = Column(String(20), nullable=False)
    supplier_email = Column(String(36), nullable=True)

    products = relationship("Product", back_populates="supplier")
