"""Integration tests for /users/* (staff management)."""


def test_admin_can_create_user(client, admin_headers):
    response = client.post(
        "/users/",
        json={
            "username": "staff_one",
            "password": "StaffPass123!",
            "full_name": "Staff One",
            "role": "cashier",
        },
        headers=admin_headers,
    )

    assert response.status_code == 201
    assert response.json()["username"] == "staff_one"


def test_manager_cannot_create_admin_user(client, manager_headers):
    response = client.post(
        "/users/",
        json={
            "username": "wannabe_admin",
            "password": "WannabePass123!",
            "full_name": "Wannabe Admin",
            "role": "admin",
        },
        headers=manager_headers,
    )

    assert response.status_code == 403


def test_cashier_cannot_create_users(client, cashier_headers):
    response = client.post(
        "/users/",
        json={
            "username": "nope",
            "password": "NopePass123!",
            "full_name": "Nope",
            "role": "cashier",
        },
        headers=cashier_headers,
    )

    assert response.status_code == 403


def test_create_user_rejects_duplicate_username(client, admin_headers, cashier_user):
    response = client.post(
        "/users/",
        json={
            "username": "cashier_user",
            "password": "AnotherPass123!",
            "full_name": "Duplicate",
            "role": "cashier",
        },
        headers=admin_headers,
    )

    assert response.status_code == 409


def test_list_users_as_admin(client, admin_headers, cashier_user, manager_user):
    response = client.get("/users/", headers=admin_headers)

    assert response.status_code == 200
    usernames = {u["username"] for u in response.json()}
    assert {"admin_user", "cashier_user", "manager_user"} <= usernames


def test_list_users_forbidden_for_cashier(client, cashier_headers):
    response = client.get("/users/", headers=cashier_headers)
    assert response.status_code == 403


def test_get_user_by_id(client, admin_headers, cashier_user):
    response = client.get(f"/users/{cashier_user.id}", headers=admin_headers)

    assert response.status_code == 200
    assert response.json()["username"] == "cashier_user"


def test_get_user_not_found(client, admin_headers):
    response = client.get("/users/999999", headers=admin_headers)
    assert response.status_code == 404


def test_update_user_full_name(client, admin_headers, cashier_user):
    response = client.put(
        f"/users/{cashier_user.id}",
        json={"full_name": "Updated Name"},
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"


def test_update_user_not_found(client, admin_headers):
    response = client.put(
        "/users/999999",
        json={"full_name": "Ghost"},
        headers=admin_headers,
    )
    assert response.status_code == 404


def test_manager_cannot_modify_admin_account(client, manager_headers, admin_user):
    response = client.put(
        f"/users/{admin_user.id}",
        json={"full_name": "Hacked Name"},
        headers=manager_headers,
    )
    assert response.status_code == 403


def test_manager_cannot_promote_user_to_admin(client, manager_headers, cashier_user):
    response = client.put(
        f"/users/{cashier_user.id}",
        json={"role": "admin"},
        headers=manager_headers,
    )
    assert response.status_code == 403


def test_admin_can_deactivate_user(client, admin_headers, cashier_user):
    response = client.put(
        f"/users/{cashier_user.id}",
        json={"is_active": False},
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_update_user_password_is_rehashed(client, admin_headers, cashier_user):
    response = client.put(
        f"/users/{cashier_user.id}",
        json={"password": "BrandNewPass123!"},
        headers=admin_headers,
    )
    assert response.status_code == 200

    # The old password must no longer work...
    old_login = client.post(
        "/auth/login",
        data={"username": "cashier_user", "password": "CashierPass123!"},
    )
    assert old_login.status_code == 401

    # ...only the new one does, proving it was actually rehashed and persisted.
    new_login = client.post(
        "/auth/login",
        data={"username": "cashier_user", "password": "BrandNewPass123!"},
    )
    assert new_login.status_code == 200


def test_admin_can_delete_user(client, admin_headers, cashier_user):
    response = client.delete(f"/users/{cashier_user.id}", headers=admin_headers)
    assert response.status_code == 204

    follow_up = client.get(f"/users/{cashier_user.id}", headers=admin_headers)
    assert follow_up.status_code == 404


def test_admin_cannot_delete_own_account(client, admin_headers, admin_user):
    response = client.delete(f"/users/{admin_user.id}", headers=admin_headers)
    assert response.status_code == 400


def test_manager_cannot_delete_users(client, manager_headers, cashier_user):
    response = client.delete(f"/users/{cashier_user.id}", headers=manager_headers)
    assert response.status_code == 403
