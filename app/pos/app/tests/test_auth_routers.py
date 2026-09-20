"""Integration tests for /auth/* endpoints."""


def test_register_first_user_becomes_admin(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "first_owner",
            "password": "OwnerPass123!",
            "full_name": "First Owner",
            "role": "cashier",  # ignored - bootstrap user is always admin
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "first_owner"
    assert body["role"] == "admin"
    assert body["is_active"] is True


def test_register_is_disabled_once_a_user_exists(client, cashier_user):
    response = client.post(
        "/auth/register",
        json={
            "username": "second_user",
            "password": "SecondPass123!",
            "full_name": "Second User",
        },
    )

    assert response.status_code == 403
    assert "disabled" in response.json()["detail"]


def test_register_rejects_short_password(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "short_pw",
            "password": "short",
            "full_name": "Short Password",
        },
    )

    assert response.status_code == 422


def test_register_rejects_missing_fields(client):
    response = client.post("/auth/register", json={"username": "incomplete"})

    assert response.status_code == 422


def test_login_success_returns_token_and_user(client, cashier_user):
    response = client.post(
        "/auth/login",
        data={"username": "cashier_user", "password": "CashierPass123!"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["user"]["username"] == "cashier_user"
    assert body["user"]["role"] == "cashier"


def test_login_rejects_wrong_password(client, cashier_user):
    response = client.post(
        "/auth/login",
        data={"username": "cashier_user", "password": "WrongPassword!"},
    )

    assert response.status_code == 401


def test_login_rejects_unknown_username(client):
    response = client.post(
        "/auth/login",
        data={"username": "ghost", "password": "whatever123"},
    )

    assert response.status_code == 401


def test_login_rejects_inactive_user(client, make_user):
    make_user("sleepy", "SleepyPass123!", "Sleepy User", "cashier", is_active=False)

    response = client.post(
        "/auth/login",
        data={"username": "sleepy", "password": "SleepyPass123!"},
    )

    assert response.status_code == 403


def test_me_requires_authentication(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_returns_current_user(client, cashier_user, auth_headers):
    response = client.get("/auth/me", headers=auth_headers(cashier_user))

    assert response.status_code == 200
    assert response.json()["username"] == "cashier_user"


def test_admin_can_create_staff_user(client, admin_headers):
    response = client.post(
        "/auth/users",
        json={
            "username": "new_manager",
            "password": "NewManagerPass123!",
            "full_name": "New Manager",
            "role": "manager",
        },
        headers=admin_headers,
    )

    assert response.status_code == 201
    assert response.json()["role"] == "manager"


def test_manager_cannot_create_admin_via_auth_users(client, manager_headers):
    response = client.post(
        "/auth/users",
        json={
            "username": "sneaky_admin",
            "password": "SneakyPass123!",
            "full_name": "Sneaky Admin",
            "role": "admin",
        },
        headers=manager_headers,
    )

    assert response.status_code == 403


def test_cashier_cannot_create_staff_user(client, cashier_headers):
    response = client.post(
        "/auth/users",
        json={
            "username": "another_cashier",
            "password": "AnotherPass123!",
            "full_name": "Another Cashier",
            "role": "cashier",
        },
        headers=cashier_headers,
    )

    assert response.status_code == 403


def test_create_staff_user_rejects_duplicate_username(client, admin_headers, cashier_user):
    response = client.post(
        "/auth/users",
        json={
            "username": "cashier_user",
            "password": "AnotherPass123!",
            "full_name": "Duplicate",
            "role": "cashier",
        },
        headers=admin_headers,
    )

    assert response.status_code == 409
