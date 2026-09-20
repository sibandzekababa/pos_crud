"""Integration tests for /receipts/*."""
import pytest


@pytest.fixture
def completed_sale(client, cashier_headers, sample_product):
    return client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 1}],
            "payments": [{"payment_method": "card", "amount_paid": 250.0}],
        },
        headers=cashier_headers,
    ).json()


def test_receipts_require_authentication(client):
    response = client.get("/receipts/")
    assert response.status_code == 401


def test_list_all_receipts(client, cashier_headers, completed_sale):
    response = client.get("/receipts/", headers=cashier_headers)
    assert response.status_code == 200
    numbers = [r["receipt_number"] for r in response.json()]
    assert completed_sale["receipt"]["receipt_number"] in numbers


def test_get_receipt_by_sale_id(client, cashier_headers, completed_sale):
    response = client.get(f"/receipts/sale/{completed_sale['sale_id']}", headers=cashier_headers)
    assert response.status_code == 200
    assert response.json()["sale_id"] == completed_sale["sale_id"]


def test_get_receipt_by_sale_id_not_found(client, cashier_headers):
    response = client.get("/receipts/sale/999999", headers=cashier_headers)
    assert response.status_code == 404


def test_get_receipt_by_id(client, cashier_headers, completed_sale):
    receipt_id = completed_sale["receipt"]["receipt_id"]

    response = client.get(f"/receipts/{receipt_id}", headers=cashier_headers)
    assert response.status_code == 200
    assert response.json()["receipt_id"] == receipt_id


def test_get_receipt_by_id_not_found(client, cashier_headers):
    response = client.get("/receipts/999999", headers=cashier_headers)
    assert response.status_code == 404
