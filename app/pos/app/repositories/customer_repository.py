from sqlalchemy.orm import Session
from app.models.customer import Customer

class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Customer

    def get_by_id(self, customer_id: int):
        return self.db.query(self.model).filter(self.model.id == customer_id).first()

    def get_all(self):
        return self.db.query(self.model).all()

    def create(self, data: dict):
        db_customer = self.model(**data)
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer

    def update(self, customer_id: int, data: dict):
        db_customer = self.get_by_id(customer_id)
        if db_customer:
            for key, value in data.items():
                if value is not None:
                    setattr(db_customer, key, value)
            self.db.commit()
            self.db.refresh(db_customer)
        return db_customer

    def delete(self, customer_id: int):
        db_customer = self.get_by_id(customer_id)
        if db_customer:
            self.db.delete(db_customer)
            self.db.commit()
            return True
        return False
