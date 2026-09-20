"""Integration tests for /categories/*."""


def test_manager_can_create_category(client, manager_headers):
    response = client.post(
        "/categories/",
        json={"category_name": "Snacks", "category_description": "Chips and crisps"},
        headers=manager_headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["category_name"] == "Snacks"
    assert "id" in body


def test_cashier_cannot_create_category(client, cashier_headers):
    response = client.post(
        "/categories/",
        json={"category_name": "Snacks"},
        headers=cashier_headers,
    )
    assert response.status_code == 403


def test_create_category_requires_authentication(client):
    response = client.post("/categories/", json={"category_name": "Snacks"})
    assert response.status_code == 401


def test_create_category_rejects_missing_name(client, manager_headers):
    response = client.post(
        "/categories/",
        json={"category_description": "No name given"},
        headers=manager_headers,
    )
    assert response.status_code == 422


def test_list_categories(client, cashier_headers, sample_category):
    response = client.get("/categories/", headers=cashier_headers)

    assert response.status_code == 200
    names = [c["category_name"] for c in response.json()]
    assert "Beverages" in names


def test_get_category_by_id(client, cashier_headers, sample_category):
    response = client.get(f"/categories/{sample_category.id}", headers=cashier_headers)

    assert response.status_code == 200
    assert response.json()["category_name"] == "Beverages"


def test_get_category_not_found(client, cashier_headers):
    response = client.get("/categories/999999", headers=cashier_headers)
    assert response.status_code == 404


def test_update_category(client, manager_headers, sample_category):
    response = client.put(
        f"/categories/{sample_category.id}",
        json={"category_name": "Cold Beverages"},
        headers=manager_headers,
    )

    assert response.status_code == 200
    assert response.json()["category_name"] == "Cold Beverages"


def test_update_category_not_found(client, manager_headers):
    response = client.put(
        "/categories/999999",
        json={"category_name": "Ghost"},
        headers=manager_headers,
    )
    assert response.status_code == 404


def test_update_category_forbidden_for_cashier(client, cashier_headers, sample_category):
    response = client.put(
        f"/categories/{sample_category.id}",
        json={"category_name": "Hacked"},
        headers=cashier_headers,
    )
    assert response.status_code == 403


def test_delete_category(client, manager_headers, sample_category):
    response = client.delete(f"/categories/{sample_category.id}", headers=manager_headers)
    assert response.status_code == 204

    follow_up = client.get(f"/categories/{sample_category.id}", headers=manager_headers)
    assert follow_up.status_code == 404


def test_delete_category_not_found(client, manager_headers):
    response = client.delete("/categories/999999", headers=manager_headers)
    assert response.status_code == 404


def test_delete_category_forbidden_for_cashier(client, cashier_headers, sample_category):
    response = client.delete(f"/categories/{sample_category.id}", headers=cashier_headers)
    assert response.status_code == 403
