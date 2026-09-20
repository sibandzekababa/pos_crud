from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.sale import Sale


class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    def get_payment(self, payment_id: int):
        payment = self.db.query(Payment).filter(Payment.payment_id == payment_id).first()
        if not payment:
            raise HTTPException(404, "Payment record not found")
        return payment

    def get_payments_for_sale(self, sale_id: int):
        if not self.db.query(Sale).filter(Sale.sale_id == sale_id).first():
            raise HTTPException(404, "Sale record not found")
        return self.db.query(Payment).filter(Payment.sale_id == sale_id).all()

    def get_all_payments(self):
        return self.db.query(Payment).order_by(Payment.payment_date.desc()).all()

    def create_payment(self, data: dict):
        sale = self.db.query(Sale).filter(Sale.sale_id == data["sale_id"]).first()
        if not sale:
            raise HTTPException(404, "Linked sale transaction not found")

        method = data["payment_method"].strip().lower()
        aliases = {"mobile money": "mpesa", "m-pesa": "mpesa", "mobile_money": "mpesa"}
        method = aliases.get(method, method)
        if method not in {"cash", "mpesa", "card", "store_credit"}:
            raise HTTPException(400, "Unsupported payment method")

        already_paid = sum(float(p.amount_paid) for p in sale.payments)
        remaining = round(float(sale.total_amount) - already_paid, 2)
        amount = round(float(data["amount_paid"]), 2)

        if amount <= 0:
            raise HTTPException(400, "Payment amount must be greater than zero")
        if amount > remaining and method != "cash":
            raise HTTPException(400, f"Payment exceeds remaining balance of {remaining:.2f}")

        payment = Payment(
            sale_id=sale.sale_id,
            payment_method=method,
            amount_paid=amount,
        )
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment
