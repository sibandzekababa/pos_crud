import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def product_service(mock_db_session):
    service = ProductService(db=mock_db_session)
    service.repository = MagicMock(spec=ProductRepository)
    return service

def test_get_product_success(product_service):
    mock_product = {"id": 101, "name": "Laptop", "price": 999.99}
    product_service.repository.get_by_id.return_value = mock_product

    result = product_service.get_product(101)

    assert result == mock_product
    product_service.repository.get_by_id.assert_called_once_with(101)

def test_get_product_not_found(product_service):
    product_service.repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        product_service.get_product(999)
    
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Product not found"

def test_get_all_products(product_service):
    mock_products = [
        {"id": 101, "name": "Laptop", "price": 999.99},
        {"id": 102, "name": "Mouse", "price": 25.00},
        {"id": 1, "name": "Pencil", "price": 4.50}
    ]
    product_service.repository.get_all.return_value = mock_products

    result = product_service.get_all_products()

    assert result == mock_products
    product_service.repository.get_all.assert_called_once()

def test_create_product(product_service):
    input_data = {"name": "Keyboard", "price": 45.00}
    created_product = {"id": 103, "name": "Keyboard", "price": 45.00}
    product_service.repository.create.return_value = created_product

    result = product_service.create_product(input_data)

    assert result == created_product
    product_service.repository.create.assert_called_once_with(input_data)

def test_scan_product_success(product_service):
    class MockProduct:
        product_name = "Juice"
        stock_quantity = 15

    mock_product = MockProduct()
    product_service.repository.get_by_barcode.return_value = mock_product

    result = product_service.scan_product("11223344")

    assert result == mock_product
    product_service.repository.get_by_barcode.assert_called_once_with("11223344")

def test_scan_product_not_found(product_service):
    product_service.repository.get_by_barcode.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        product_service.scan_product("99999999")
    
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in exc_info.value.detail

def test_scan_product_out_of_stock(product_service):
    class MockProduct:
        product_name = "Juice"
        stock_quantity = 0

    mock_product = MockProduct()
    product_service.repository.get_by_barcode.return_value = mock_product

    with pytest.raises(HTTPException) as exc_info:
        product_service.scan_product("11223344")
    
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "out of stock" in exc_info.value.detail

def test_scan_product_via_camera_success(monkeypatch, product_service):
    class MockBarcodeResult:
        text = "11223344"

    class MockProduct:
        product_name = "Orange Juice"
        stock_quantity = 50

    monkeypatch.setattr("pyrxing.read_barcodes", lambda img: [MockBarcodeResult()])
    product_service.repository.get_by_barcode.return_value = MockProduct()

    result = product_service.scan_product("11223344")
    assert result.product_name == "Orange Juice"
    assert result.stock_quantity == 50
    assert product_service.repository.get_by_barcode.called
