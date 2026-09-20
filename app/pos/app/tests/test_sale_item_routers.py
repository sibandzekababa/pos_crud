"""Integration tests for /sale-items/*."""
import pytest


@pytest.fixture
def completed_sale(client, cashier_headers, sample_product):
    return client.post(
        "/sales/",
        json={
            "items": [{"product_id": sample_product.product_id, "quantity": 3}],
            "payments": [{"payment_method": "card", "amount_paid": 750.0}],
        },
        headers=cashier_headers,
    ).json()


def test_sale_items_require_authentication(client):
    response = client.get("/sale-items/")
    assert response.status_code == 401


def test_list_all_sale_items(client, cashier_headers, completed_sale):
    response = client.get("/sale-items/", headers=cashier_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_items_for_sale(client, cashier_headers, completed_sale):
    response = client.get(f"/sale-items/sale/{completed_sale['sale_id']}", headers=cashier_headers)
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["quantity"] == 3


def test_get_items_for_sale_with_no_items_returns_empty_list(client, cashier_headers):
    response = client.get("/sale-items/sale/999999", headers=cashier_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_get_sale_item_by_id(client, cashier_headers, completed_sale):
    item_id = completed_sale["items"][0]["sale_item_id"]

    response = client.get(f"/sale-items/{item_id}", headers=cashier_headers)
    assert response.status_code == 200
    assert response.json()["sale_item_id"] == item_id


def test_get_sale_item_not_found(client, cashier_headers):
    response = client.get("/sale-items/999999", headers=cashier_headers)
    assert response.status_code == 404
