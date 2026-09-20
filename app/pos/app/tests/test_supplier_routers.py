"""Integration tests for /suppliers/*."""


def test_manager_can_create_supplier(client, manager_headers):
    response = client.post(
        "/suppliers/",
        json={
            "company_name": "Fresh Farms Ltd",
            "contact_name": "Peter Farmer",
            "supplier_phoneNumber": "+254744444444",
            "supplier_email": "peter@freshfarms.example",
        },
        headers=manager_headers,
    )

    assert response.status_code == 201
    assert response.json()["company_name"] == "Fresh Farms Ltd"


def test_cashier_cannot_create_supplier(client, cashier_headers):
    response = client.post(
        "/suppliers/",
        json={"company_name": "Fresh Farms Ltd", "supplier_phoneNumber": "+254744444444"},
        headers=cashier_headers,
    )
    assert response.status_code == 403


def test_create_supplier_rejects_missing_required_fields(client, manager_headers):
    response = client.post(
        "/suppliers/",
        json={"contact_name": "No company name or phone"},
        headers=manager_headers,
    )
    assert response.status_code == 422


def test_list_suppliers(client, cashier_headers, sample_supplier):
    response = client.get("/suppliers/", headers=cashier_headers)

    assert response.status_code == 200
    names = [s["company_name"] for s in response.json()]
    assert "Acme Distributors" in names


def test_get_supplier_by_id(client, cashier_headers, sample_supplier):
    response = client.get(f"/suppliers/{sample_supplier.supplier_id}", headers=cashier_headers)

    assert response.status_code == 200
    assert response.json()["company_name"] == "Acme Distributors"


def test_get_supplier_not_found(client, cashier_headers):
    response = client.get("/suppliers/999999", headers=cashier_headers)
    assert response.status_code == 404


def test_update_supplier(client, manager_headers, sample_supplier):
    response = client.put(
        f"/suppliers/{sample_supplier.supplier_id}",
        json={"contact_name": "New Contact"},
        headers=manager_headers,
    )

    assert response.status_code == 200
    assert response.json()["contact_name"] == "New Contact"


def test_update_supplier_not_found(client, manager_headers):
    response = client.put(
        "/suppliers/999999",
        json={"contact_name": "Ghost"},
        headers=manager_headers,
    )
    assert response.status_code == 404


def test_cashier_cannot_update_supplier(client, cashier_headers, sample_supplier):
    response = client.put(
        f"/suppliers/{sample_supplier.supplier_id}",
        json={"contact_name": "Hacked"},
        headers=cashier_headers,
    )
    assert response.status_code == 403


def test_delete_supplier(client, manager_headers, sample_supplier):
    response = client.delete(f"/suppliers/{sample_supplier.supplier_id}", headers=manager_headers)
    assert response.status_code == 204

    follow_up = client.get(f"/suppliers/{sample_supplier.supplier_id}", headers=manager_headers)
    assert follow_up.status_code == 404


def test_delete_supplier_not_found(client, manager_headers):
    response = client.delete("/suppliers/999999", headers=manager_headers)
    assert response.status_code == 404
