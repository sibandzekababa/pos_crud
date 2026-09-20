import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.services.auth_service import authenticate, create_user, make_login_response
from app.models.user import User

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_user(monkeypatch):
    user = User()
    user.id = 1
    user.username = "jane_cashier"
    user.hashed_password = "mocked_hashed_string"
    user.full_name = "Jane Doe"
    user.role = "cashier"
    user.is_active = True
    
    monkeypatch.setattr("app.services.auth_service.verify_password", lambda plain, hashed: plain == "CorrectPassword123")
    monkeypatch.setattr("app.services.auth_service.hash_password", lambda plain: "mocked_hashed_string")
    monkeypatch.setattr("app.services.auth_service.create_access_token", lambda uid, role: "mock_jwt_token_xyz")
    
    return user

def test_authenticate_success(mock_db_session, mock_user):
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

    authenticated_user = authenticate(mock_db_session, "jane_cashier", "CorrectPassword123")

    assert authenticated_user == mock_user

def test_authenticate_invalid_password(mock_db_session, mock_user):
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

    with pytest.raises(HTTPException) as exc_info:
        authenticate(mock_db_session, "jane_cashier", "WrongPassword")
    
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid username" in exc_info.value.detail

def test_authenticate_user_inactive(mock_db_session, mock_user):
    mock_user.is_active = False
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

    with pytest.raises(HTTPException) as exc_info:
        authenticate(mock_db_session, "jane_cashier", "CorrectPassword123")
        
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert "account is inactive" in exc_info.value.detail

def test_create_user_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    new_user = create_user(mock_db_session, "new_manager", "Pass1234!", "Alice Smith", "Manager")

    assert new_user.username == "new_manager"
    assert new_user.role == "manager"
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()

def test_create_user_already_registered(mock_db_session, mock_user):
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

    with pytest.raises(HTTPException) as exc_info:
        create_user(mock_db_session, "jane_cashier", "Pass1234!", "Jane Doe", "cashier")
        
    assert exc_info.value.status_code == 409
    assert "already registered" in exc_info.value.detail

def test_make_login_response(mock_user):
    response = make_login_response(mock_user)

    assert response["access_token"] == "mock_jwt_token_xyz"
    assert response["token_type"] == "bearer"
    assert response["user"] == mock_user
