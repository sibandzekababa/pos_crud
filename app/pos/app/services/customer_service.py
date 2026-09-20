from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.customer_repository import CustomerRepository

class CustomerService:
    def __init__(self, db: Session):
        self.repository = CustomerRepository(db)

    def get_customer(self, customer_id: int):
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer record not found"
            )
        return customer

    def get_all_customers(self):
        return self.repository.get_all()

    def create_customer(self, data: dict):
        return self.repository.create(data)

    def update_customer(self, customer_id: int, data: dict):
        self.get_customer(customer_id)
        return self.repository.update(customer_id, data)

    def delete_customer(self, customer_id: int):
        self.get_customer(customer_id)
        return self.repository.delete(customer_id)
