from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

class Payment(Base):
    __tablename__ = "payment_table"
    
    payment_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sale_table.sale_id", ondelete="CASCADE"), nullable=False)
    payment_method = Column(String(30), nullable=False)
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(DateTime, server_default=func.now(), nullable=False)

    sale = relationship("Sale", back_populates="payments")
