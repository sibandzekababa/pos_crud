"""Integration tests for /sales/* (checkout, retrieval, cancellation)."""


def test_checkout_exact_card_payment_success(client, cashier_headers, sample_product):
    response = client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 2}],
            "payments": [{"payment_method": "card", "amount_paid": 500.0}],
        },
        headers=cashier_headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["total_amount"] == 500.0
    assert body["change_due"] == 0.0
    assert len(body["items"]) == 1
    assert body["items"][0]["quantity"] == 2
    assert body["receipt"] is not None
    assert body["receipt"]["receipt_number"].startswith("INV-")


def test_checkout_cash_overpayment_returns_change(client, cashier_headers, sample_product):
    response = client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 1}],
            "payments": [{"payment_method": "cash", "amount_paid": 300.0}],
        },
        headers=cashier_headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["total_amount"] == 250.0
    assert body["change_due"] == 50.0


def test_checkout_decrements_stock(client, cashier_headers, db_session, sample_product):
    client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 5}],
            "payments": [{"payment_method": "cash", "amount_paid": 1250.0}],
        },
        headers=cashier_headers,
    )

    db_session.refresh(sample_product)
    assert sample_product.stock_quantity == 15  # started at 20


def test_checkout_combines_duplicate_product_lines(client, cashier_headers, sample_product):
    response = client.post(
        "/sales/",
        json={
            "items": [
                {"product_id": sample_product.product_id, "quantity": 2},
                {"product_id": sample_product.product_id, "quantity": 3},
            ],
            "payments": [{"payment_method": "cash", "amount_paid": 1250.0}],
        },
        headers=cashier_headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert len(body["items"]) == 1
    assert body["items"][0]["quantity"] == 5


def test_checkout_awards_loyalty_points_to_customer(client, cashier_headers, db_session, sample_product, sample_customer):
    client.post(
        "/sales/",
        json={
            "customer_id": sample_customer.id,
            "items": [{"product_id": sample_product.product_id, "quantity": 4}],
            "payments": [{"payment_method": "card", "amount_paid": 1000.0}],
        },
        headers=cashier_headers,
    )

    db_session.refresh(sample_customer)
    assert sample_customer.loyalty_points == 10  # 1000 currency units / 100


def test_checkout_rejects_zero_value_sale(client, cashier_headers, db_session, sample_product):
    sample_product.product_price = 0.0
    db_session.add(sample_product)
    db_session.commit()

    response = client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 1}],
            "payments": [{"payment_method": "cash", "amount_paid": 1.0}],
        },
        headers=cashier_headers,
    )

    assert response.status_code == 400
    assert "greater than zero" in response.json()["detail"]


def test_checkout_fails_for_insufficient_stock(client, cashier_headers, sample_product):
    response = client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 999}],
            "payments": [{"payment_method": "cash", "amount_paid": 999999.0}],
        },
        headers=cashier_headers,
    )

    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]


def test_checkout_fails_for_insufficient_payment(client, cashier_headers, sample_product):
    response = client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 2}],
            "payments": [{"payment_method": "card", "amount_paid": 100.0}],
        },
        headers=cashier_headers,
    )

    assert response.status_code == 400
    assert "Insufficient payment" in response.json()["detail"]


def test_checkout_fails_for_unknown_product(client, cashier_headers):
    response = client.post(
        "/sales/",
        json={
            "items": [{"product_id": 999999, "quantity": 1}],
            "payments": [{"payment_method": "cash", "amount_paid": 100.0}],
        },
        headers=cashier_headers,
    )

    assert response.status_code == 404


def test_checkout_fails_for_unknown_customer(client, cashier_headers, sample_product):
    response = client.post(
        "/sales/",
        json={
            "customer_id": 999999,
            "items": [{"product_id": sample_product.product_id, "quantity": 1}],
            "payments": [{"payment_method": "cash", "amount_paid": 250.0}],
        },
        headers=cashier_headers,
    )

    assert response.status_code == 404


def test_checkout_fails_when_non_cash_overpays(client, cashier_headers, sample_product):
    response = client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 1}],
            "payments": [{"payment_method": "card", "amount_paid": 300.0}],
        },
        headers=cashier_headers,
    )

    assert response.status_code == 400
    assert "cannot exceed the sale total" in response.json()["detail"]


def test_checkout_requires_authentication(client, sample_product):
    response = client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 1}],
            "payments": [{"payment_method": "cash", "amount_paid": 250.0}],
        },
    )
    assert response.status_code == 401


def test_checkout_rejects_empty_basket(client, cashier_headers):
    response = client.post(
        "/sales/",
        json={"items": [], "payments": [{"payment_method": "cash", "amount_paid": 100.0}]},
        headers=cashier_headers,
    )
    assert response.status_code == 422


def test_get_sale_by_id(client, cashier_headers, sample_product):
    created = client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 1}],
            "payments": [{"payment_method": "card", "amount_paid": 250.0}],
        },
        headers=cashier_headers,
    ).json()

    response = client.get(f"/sales/{created['sale_id']}", headers=cashier_headers)
    assert response.status_code == 200
    assert response.json()["sale_id"] == created["sale_id"]


def test_get_sale_not_found(client, cashier_headers):
    response = client.get("/sales/999999", headers=cashier_headers)
    assert response.status_code == 404


def test_list_sales(client, cashier_headers, sample_product):
    client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 1}],
            "payments": [{"payment_method": "card", "amount_paid": 250.0}],
        },
        headers=cashier_headers,
    )

    response = client.get("/sales/", headers=cashier_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_manager_can_cancel_sale_and_restock(client, cashier_headers, manager_headers, db_session, sample_product):
    created = client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 5}],
            "payments": [{"payment_method": "cash", "amount_paid": 1250.0}],
        },
        headers=cashier_headers,
    ).json()

    response = client.delete(f"/sales/{created['sale_id']}", headers=manager_headers)
    assert response.status_code == 204

    db_session.refresh(sample_product)
    assert sample_product.stock_quantity == 20  # restored back to original

    follow_up = client.get(f"/sales/{created['sale_id']}", headers=manager_headers)
    assert follow_up.status_code == 404


def test_cancel_sale_reverts_customer_loyalty_points(
    client, cashier_headers, manager_headers, db_session, sample_product, sample_customer
):
    created = client.post(
        "/sales/",
        json={
            "customer_id": sample_customer.id,
            "items": [{"product_id": sample_product.product_id, "quantity": 4}],
            "payments": [{"payment_method": "card", "amount_paid": 1000.0}],
        },
        headers=cashier_headers,
    ).json()

    db_session.refresh(sample_customer)
    assert sample_customer.loyalty_points == 10

    response = client.delete(f"/sales/{created['sale_id']}", headers=manager_headers)
    assert response.status_code == 204

    db_session.refresh(sample_customer)
    assert sample_customer.loyalty_points == 0


def test_cashier_cannot_cancel_sale(client, cashier_headers, sample_product):
    created = client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 1}],
            "payments": [{"payment_method": "card", "amount_paid": 250.0}],
        },
        headers=cashier_headers,
    ).json()

    response = client.delete(f"/sales/{created['sale_id']}", headers=cashier_headers)
    assert response.status_code == 403


def test_cancel_sale_not_found(client, manager_headers):
    response = client.delete("/sales/999999", headers=manager_headers)
    assert response.status_code == 404
