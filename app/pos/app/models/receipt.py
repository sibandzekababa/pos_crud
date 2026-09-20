from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from database import Base


class Receipt(Base):
    __tablename__ = "receipt_table"

    receipt_id = Column(Integer, primary_key=True, index=True)
    receipt_number = Column(String(50), unique=True, nullable=False, index=True)
    sale_id = Column(Integer, ForeignKey("sale_table.sale_id", ondelete="CASCADE"), unique=True, nullable=False)
    issued_at = Column(DateTime, server_default=func.now(), nullable=False)

    sale = relationship("Sale", back_populates="receipt")
