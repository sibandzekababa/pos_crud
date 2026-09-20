from collections import defaultdict

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.customer import Customer
from app.models.payment import Payment
from app.models.product import Product
from app.models.receipt import Receipt
from app.models.sale import Sale
from app.models.sale_item import SaleItem


class SaleService:
    """
    Complete checkout transaction for a small supermarket.

    Rules:
    - The authenticated cashier/manager becomes the sale owner.
    - Client cannot choose another user_id.
    - Product prices are read from the database, never trusted from the client.
    - Stock is checked and deducted atomically.
    - Duplicate products in a basket are combined.
    - Payments must cover the sale total.
    - Cash may exceed the total and produces change.
    - M-Pesa/card/store-credit must be exact; no change is returned.
    - One receipt is generated automatically.
    - Customer receives 1 loyalty point for every 100 currency units spent.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_sale(self, sale_id: int):
        sale = (
            self.db.query(Sale)
            .options(
                joinedload(Sale.items),
                joinedload(Sale.payments),
                joinedload(Sale.receipt),
            )
            .filter(Sale.sale_id == sale_id)
            .first()
        )
        if not sale:
            raise HTTPException(404, "Sale record not found")
        return sale

    def get_all_sales(self):
        return (
            self.db.query(Sale)
            .options(joinedload(Sale.items), joinedload(Sale.payments), joinedload(Sale.receipt))
            .order_by(Sale.sale_date.desc())
            .all()
        )

    def process_checkout(self, data: dict, cashier):
        items = data["items"]
        payments = data["payments"]

        # Combine duplicate product lines.
        quantities = defaultdict(int)
        for item in items:
            quantities[item["product_id"]] += item["quantity"]

        if data.get("customer_id") is not None:
            customer = self.db.query(Customer).filter(Customer.id == data["customer_id"]).first()
            if not customer:
                raise HTTPException(404, "Customer not found")

        # Validate all products and stock before changing anything.
        products = {}
        try:
            for product_id, quantity in quantities.items():
                product = (
                    self.db.query(Product)
                    .filter(Product.product_id == product_id)
                    .with_for_update()
                    .first()
                )
                if not product:
                    raise HTTPException(404, f"Product with ID {product_id} does not exist")
                if product.product_price < 0:
                    raise HTTPException(409, f"Product {product.product_name} has an invalid price")
                if product.stock_quantity < quantity:
                    raise HTTPException(
                        400,
                        f"Insufficient stock for {product.product_name}. "
                        f"Available: {product.stock_quantity}, requested: {quantity}",
                    )
                products[product_id] = product

            total = 0.0
            line_data = []
            for product_id, quantity in quantities.items():
                product = products[product_id]
                unit_price = float(product.product_price)
                subtotal = round(unit_price * quantity, 2)
                total += subtotal
                line_data.append((product, quantity, unit_price))

            total = round(total, 2)
            if total <= 0:
                raise HTTPException(400, "Sale total must be greater than zero")

            # Normalize and validate payments.
            payment_total = 0.0
            normalized_payments = []
            for payment in payments:
                method = payment["payment_method"].strip().lower()
                aliases = {"mobile money": "mpesa", "m-pesa": "mpesa", "mobile_money": "mpesa"}
                method = aliases.get(method, method)
                if method not in {"cash", "mpesa", "card", "store_credit"}:
                    raise HTTPException(400, f"Unsupported payment method: {method}")
                amount = round(float(payment["amount_paid"]), 2)
                payment_total += amount
                normalized_payments.append((method, amount))

            payment_total = round(payment_total, 2)
            if payment_total < total:
                raise HTTPException(
                    400,
                    f"Insufficient payment. Sale total is {total:.2f}, "
                    f"but only {payment_total:.2f} was provided.",
                )

            # Only cash is allowed to create change.
            non_cash = round(sum(a for m, a in normalized_payments if m != "cash"), 2)
            if non_cash > total:
                raise HTTPException(
                    400,
                    "M-Pesa, card, and store credit payments cannot exceed the sale total.",
                )

            change_due = round(payment_total - total, 2)
            if change_due > 0 and not any(m == "cash" for m, _ in normalized_payments):
                raise HTTPException(400, "Overpayment is only allowed when cash is included.")

            # Create sale.
            sale = Sale(
                customer_id=data.get("customer_id"),
                user_id=cashier.id,
                total_amount=total,
            )
            self.db.add(sale)
            self.db.flush()

            for product, quantity, unit_price in line_data:
                product.stock_quantity -= quantity
                self.db.add(
                    SaleItem(
                        sale_id=sale.sale_id,
                        product_id=product.product_id,
                        quantity=quantity,
                        unit_price=unit_price,
                    )
                )

            for method, amount in normalized_payments:
                self.db.add(
                    Payment(
                        sale_id=sale.sale_id,
                        payment_method=method,
                        amount_paid=amount,
                    )
                )

            # Receipt number is deterministic and unique because sale_id is unique.
            self.db.add(
                Receipt(
                    receipt_number=f"INV-{sale.sale_id:08d}",
                    sale_id=sale.sale_id,
                )
            )

            # Loyalty: 1 point per 100 currency units.
            if data.get("customer_id") is not None:
                customer = self.db.query(Customer).filter(Customer.id == data["customer_id"]).first()
                customer.loyalty_points += int(total // 100)

            self.db.commit()
            return self.get_sale(sale.sale_id), change_due

        except HTTPException:
            self.db.rollback()
            raise
        except Exception:
            self.db.rollback()
            raise

    def cancel_sale(self, sale_id: int):
        sale = self.get_sale(sale_id)

        try:
            # Restore inventory before deleting the transaction.
            for item in sale.items:
                product = (
                    self.db.query(Product)
                    .filter(Product.product_id == item.product_id)
                    .with_for_update()
                    .first()
                )
                if product:
                    product.stock_quantity += item.quantity

            if sale.customer_id:
                customer = self.db.query(Customer).filter(Customer.id == sale.customer_id).first()
                if customer:
                    customer.loyalty_points = max(
                        0, customer.loyalty_points - int(float(sale.total_amount) // 100)
                    )

            self.db.delete(sale)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
