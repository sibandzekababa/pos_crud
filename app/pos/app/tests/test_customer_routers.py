"""Integration tests for /customers/*."""


def test_cashier_can_create_customer(client, cashier_headers):
    response = client.post(
        "/customers/",
        json={"full_name": "Alice Buyer", "phone": "+254722222222", "loyalty_points": 0},
        headers=cashier_headers,
    )

    assert response.status_code == 201
    assert response.json()["full_name"] == "Alice Buyer"


def test_create_customer_requires_authentication(client):
    response = client.post("/customers/", json={"full_name": "Alice Buyer"})
    assert response.status_code == 401


def test_list_customers(client, cashier_headers, sample_customer):
    response = client.get("/customers/", headers=cashier_headers)

    assert response.status_code == 200
    names = [c["full_name"] for c in response.json()]
    assert "Jane Shopper" in names


def test_get_customer_by_id(client, cashier_headers, sample_customer):
    response = client.get(f"/customers/{sample_customer.id}", headers=cashier_headers)

    assert response.status_code == 200
    assert response.json()["full_name"] == "Jane Shopper"


def test_get_customer_not_found(client, cashier_headers):
    response = client.get("/customers/999999", headers=cashier_headers)
    assert response.status_code == 404


def test_cashier_can_update_customer(client, cashier_headers, sample_customer):
    response = client.put(
        f"/customers/{sample_customer.id}",
        json={"phone": "+254733333333"},
        headers=cashier_headers,
    )

    assert response.status_code == 200
    assert response.json()["phone"] == "+254733333333"


def test_update_customer_not_found(client, cashier_headers):
    response = client.put(
        "/customers/999999",
        json={"phone": "+254733333333"},
        headers=cashier_headers,
    )
    assert response.status_code == 404


def test_cashier_cannot_delete_customer(client, cashier_headers, sample_customer):
    response = client.delete(f"/customers/{sample_customer.id}", headers=cashier_headers)
    assert response.status_code == 403


def test_manager_can_delete_customer(client, manager_headers, sample_customer):
    response = client.delete(f"/customers/{sample_customer.id}", headers=manager_headers)
    assert response.status_code == 204

    follow_up = client.get(f"/customers/{sample_customer.id}", headers=manager_headers)
    assert follow_up.status_code == 404


def test_delete_customer_not_found(client, manager_headers):
    response = client.delete("/customers/999999", headers=manager_headers)
    assert response.status_code == 404
