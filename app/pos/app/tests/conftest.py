import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# The test suite must NEVER touch the real Postgres development database.
# Setting DATABASE_URL before importing `database`/`main` makes sure the
# app itself is wired up against SQLite for the whole test session.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ.setdefault("JWT_SECRET", "test-secret-key-do-not-use-in-production")

from database import Base, get_db  # noqa: E402
from main import app  # noqa: E402
from app.core.security import create_access_token, hash_password  # noqa: E402
from app.models.category import Category  # noqa: E402
from app.models.customer import Customer  # noqa: E402
from app.models.product import Product  # noqa: E402
from app.models.supplier import Supplier  # noqa: E402
from app.models.user import User  # noqa: E402

# A single, shared in-memory SQLite connection (StaticPool) so every
# Session created during a test - whether by a fixture or by a request
# routed through the FastAPI dependency override - sees the same data.
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def _fresh_database():
    """Build a brand-new schema before every test and tear it down after,
    so no state ever leaks between tests."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """A raw SQLAlchemy session for arranging/asserting data directly,
    bypassing the API."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """A TestClient wired to the isolated SQLite database instead of the
    application's normal (Postgres) dependency."""

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------


def _make_user(db_session, username, password, full_name, role, is_active=True):
    user = User(
        username=username,
        hashed_password=hash_password(password),
        full_name=full_name,
        role=role,
        is_active=is_active,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def _headers_for(user):
    token = create_access_token(user.id, user.role)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def make_user(db_session):
    """Factory fixture: make_user(username, password, full_name, role)."""

    def _factory(username, password, full_name, role, is_active=True):
        return _make_user(db_session, username, password, full_name, role, is_active)

    return _factory


@pytest.fixture
def auth_headers():
    """Factory fixture: auth_headers(user) -> {'Authorization': 'Bearer ...'}."""
    return _headers_for


@pytest.fixture
def admin_user(db_session):
    return _make_user(db_session, "admin_user", "AdminPass123!", "Admin User", "admin")


@pytest.fixture
def manager_user(db_session):
    return _make_user(db_session, "manager_user", "ManagerPass123!", "Manager User", "manager")


@pytest.fixture
def cashier_user(db_session):
    return _make_user(db_session, "cashier_user", "CashierPass123!", "Cashier User", "cashier")


@pytest.fixture
def admin_headers(admin_user):
    return _headers_for(admin_user)


@pytest.fixture
def manager_headers(manager_user):
    return _headers_for(manager_user)


@pytest.fixture
def cashier_headers(cashier_user):
    return _headers_for(cashier_user)


# ---------------------------------------------------------------------------
# Domain data helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_category(db_session):
    category = Category(category_name="Beverages", category_description="Drinks")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def sample_supplier(db_session):
    supplier = Supplier(
        company_name="Acme Distributors",
        contact_name="John Doe",
        supplier_phoneNumber="+254700000000",
        supplier_email="acme@example.com",
    )
    db_session.add(supplier)
    db_session.commit()
    db_session.refresh(supplier)
    return supplier


@pytest.fixture
def sample_product(db_session, sample_category, sample_supplier):
    product = Product(
        barcode="1234567890",
        product_name="Orange Juice",
        product_price=250.0,
        stock_quantity=20,
        category_id=sample_category.id,
        supplier_id=sample_supplier.supplier_id,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture
def sample_customer(db_session):
    customer = Customer(full_name="Jane Shopper", phone="+254711111111", loyalty_points=0)
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    return customer
