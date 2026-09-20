"""Integration tests for /payments/*."""
import pytest


@pytest.fixture
def paid_sale(client, cashier_headers, sample_product):
    """A sale that has already been fully paid for via checkout."""
    return client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 1}],
            "payments": [{"payment_method": "card", "amount_paid": 250.0}],
        },
        headers=cashier_headers,
    ).json()


def test_manager_can_record_extra_cash_payment(client, manager_headers, paid_sale):
    response = client.post(
        "/payments/",
        json={
            "sale_id": paid_sale["sale_id"],
            "payment_method": "cash",
            "amount_paid": 50.0,
        },
        headers=manager_headers,
    )

    assert response.status_code == 201
    assert response.json()["payment_method"] == "cash"


def test_cashier_cannot_record_payment(client, cashier_headers, paid_sale):
    response = client.post(
        "/payments/",
        json={
            "sale_id": paid_sale["sale_id"],
            "payment_method": "cash",
            "amount_paid": 50.0,
        },
        headers=cashier_headers,
    )
    assert response.status_code == 403


def test_payment_exceeding_remaining_balance_for_non_cash(client, manager_headers, paid_sale):
    response = client.post(
        "/payments/",
        json={
            "sale_id": paid_sale["sale_id"],
            "payment_method": "card",
            "amount_paid": 1.0,
        },
        headers=manager_headers,
    )

    assert response.status_code == 400
    assert "exceeds remaining balance" in response.json()["detail"]


def test_payment_rejects_zero_amount(client, manager_headers, paid_sale):
    response = client.post(
        "/payments/",
        json={
            "sale_id": paid_sale["sale_id"],
            "payment_method": "cash",
            "amount_paid": 0,
        },
        headers=manager_headers,
    )
    assert response.status_code == 422


def test_payment_rejects_unsupported_method(client, manager_headers, paid_sale):
    response = client.post(
        "/payments/",
        json={
            "sale_id": paid_sale["sale_id"],
            "payment_method": "bitcoin",
            "amount_paid": 10.0,
        },
        headers=manager_headers,
    )
    assert response.status_code == 400
    assert "Unsupported payment method" in response.json()["detail"]


def test_payment_for_unknown_sale_returns_404(client, manager_headers):
    response = client.post(
        "/payments/",
        json={"sale_id": 999999, "payment_method": "cash", "amount_paid": 10.0},
        headers=manager_headers,
    )
    assert response.status_code == 404


def test_get_all_payments_as_manager(client, manager_headers, paid_sale):
    response = client.get("/payments/", headers=manager_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_all_payments_forbidden_for_cashier(client, cashier_headers):
    response = client.get("/payments/", headers=cashier_headers)
    assert response.status_code == 403


def test_get_payments_for_sale_any_authenticated_user(client, cashier_headers, paid_sale):
    response = client.get(f"/payments/sale/{paid_sale['sale_id']}", headers=cashier_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_payments_for_unknown_sale_returns_404(client, cashier_headers):
    response = client.get("/payments/sale/999999", headers=cashier_headers)
    assert response.status_code == 404


def test_get_payment_by_id(client, manager_headers, paid_sale):
    payment_id = client.get(
        f"/payments/sale/{paid_sale['sale_id']}", headers=manager_headers
    ).json()[0]["payment_id"]

    response = client.get(f"/payments/{payment_id}", headers=manager_headers)
    assert response.status_code == 200
    assert response.json()["payment_id"] == payment_id


def test_get_payment_not_found(client, manager_headers):
    response = client.get("/payments/999999", headers=manager_headers)
    assert response.status_code == 404


def test_get_payment_by_id_forbidden_for_cashier(client, cashier_headers, paid_sale):
    payment_id = client.get(
        f"/payments/sale/{paid_sale['sale_id']}", headers=cashier_headers
    ).json()[0]["payment_id"]

    response = client.get(f"/payments/{payment_id}", headers=cashier_headers)
    assert response.status_code == 403
