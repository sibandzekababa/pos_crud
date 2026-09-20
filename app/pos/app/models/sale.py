from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

class Sale(Base):
    __tablename__ = "sale_table"
    
    sale_id = Column(Integer, primary_key=True, index=True)
    sale_date = Column(DateTime, server_default=func.now(), nullable=False)
    total_amount = Column(Float, nullable=False, default=0.0)
    customer_id = Column(Integer, ForeignKey("customer_table.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(Integer, ForeignKey("user_table.id", ondelete="RESTRICT"), nullable=False)

    customer = relationship("Customer", back_populates="sales")
    user = relationship("User", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="sale", cascade="all, delete-orphan")
    receipt = relationship("Receipt", uselist=False, back_populates="sale", cascade="all, delete-orphan")
