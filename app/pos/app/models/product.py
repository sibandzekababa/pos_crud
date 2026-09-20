from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "product_table"
    
    product_id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String(50), nullable=True)
    product_name = Column(String(30), nullable=False)
    product_price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("category_table.id", ondelete="RESTRICT"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("supplier_table.supplier_id", ondelete="RESTRICT"), nullable=False)

    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    sale_items = relationship("SaleItem", back_populates="product")


