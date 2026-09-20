"""Integration tests for /products/* (CRUD + barcode scanning)."""
import io

from PIL import Image


def _png_bytes():
    buffer = io.BytesIO()
    Image.new("RGB", (10, 10), color="white").save(buffer, format="PNG")
    return buffer.getvalue()


def test_manager_can_create_product(client, manager_headers, sample_category, sample_supplier):
    response = client.post(
        "/products/",
        json={
            "barcode": "9990001",
            "product_name": "Bread",
            "product_price": 55.0,
            "stock_quantity": 30,
            "category_id": sample_category.id,
            "supplier_id": sample_supplier.supplier_id,
        },
        headers=manager_headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["product_name"] == "Bread"
    assert body["stock_quantity"] == 30


def test_cashier_cannot_create_product(client, cashier_headers, sample_category, sample_supplier):
    response = client.post(
        "/products/",
        json={
            "product_name": "Bread",
            "product_price": 55.0,
            "stock_quantity": 30,
            "category_id": sample_category.id,
            "supplier_id": sample_supplier.supplier_id,
        },
        headers=cashier_headers,
    )
    assert response.status_code == 403


def test_create_product_rejects_negative_price(client, manager_headers, sample_category, sample_supplier):
    response = client.post(
        "/products/",
        json={
            "product_name": "Bad Product",
            "product_price": -1.0,
            "stock_quantity": 10,
            "category_id": sample_category.id,
            "supplier_id": sample_supplier.supplier_id,
        },
        headers=manager_headers,
    )
    assert response.status_code == 422


def test_create_product_rejects_negative_stock(client, manager_headers, sample_category, sample_supplier):
    response = client.post(
        "/products/",
        json={
            "product_name": "Bad Product",
            "product_price": 10.0,
            "stock_quantity": -5,
            "category_id": sample_category.id,
            "supplier_id": sample_supplier.supplier_id,
        },
        headers=manager_headers,
    )
    assert response.status_code == 422


def test_list_products(client, cashier_headers, sample_product):
    response = client.get("/products/", headers=cashier_headers)

    assert response.status_code == 200
    names = [p["product_name"] for p in response.json()]
    assert "Orange Juice" in names


def test_get_product_by_id(client, cashier_headers, sample_product):
    response = client.get(f"/products/{sample_product.product_id}", headers=cashier_headers)

    assert response.status_code == 200
    assert response.json()["product_name"] == "Orange Juice"


def test_get_product_not_found(client, cashier_headers):
    response = client.get("/products/999999", headers=cashier_headers)
    assert response.status_code == 404


def test_update_product(client, manager_headers, sample_product):
    response = client.put(
        f"/products/{sample_product.product_id}",
        json={"product_price": 300.0},
        headers=manager_headers,
    )

    assert response.status_code == 200
    assert response.json()["product_price"] == 300.0


def test_update_product_not_found(client, manager_headers):
    response = client.put(
        "/products/999999",
        json={"product_price": 300.0},
        headers=manager_headers,
    )
    assert response.status_code == 404


def test_cashier_cannot_update_product(client, cashier_headers, sample_product):
    response = client.put(
        f"/products/{sample_product.product_id}",
        json={"product_price": 300.0},
        headers=cashier_headers,
    )
    assert response.status_code == 403


def test_delete_product(client, manager_headers, sample_product):
    response = client.delete(f"/products/{sample_product.product_id}", headers=manager_headers)
    assert response.status_code == 204

    follow_up = client.get(f"/products/{sample_product.product_id}", headers=manager_headers)
    assert follow_up.status_code == 404


def test_delete_product_not_found(client, manager_headers):
    response = client.delete("/products/999999", headers=manager_headers)
    assert response.status_code == 404


def test_scan_product_by_barcode_success(client, cashier_headers, sample_product):
    response = client.get(f"/products/scan/{sample_product.barcode}", headers=cashier_headers)

    assert response.status_code == 200
    assert response.json()["product_name"] == "Orange Juice"


def test_scan_product_by_barcode_not_found(client, cashier_headers):
    response = client.get("/products/scan/does-not-exist", headers=cashier_headers)
    assert response.status_code == 404


def test_scan_product_out_of_stock(client, cashier_headers, db_session, sample_product):
    sample_product.stock_quantity = 0
    db_session.add(sample_product)
    db_session.commit()

    response = client.get(f"/products/scan/{sample_product.barcode}", headers=cashier_headers)
    assert response.status_code == 400
    assert "out of stock" in response.json()["detail"]


def test_scan_product_via_camera_success(client, cashier_headers, sample_product, monkeypatch):
    class FakeBarcodeResult:
        text = sample_product.barcode

    monkeypatch.setattr(
        "app.routers.product_routers.pyrxing.read_barcodes",
        lambda img: [FakeBarcodeResult()],
    )

    response = client.post(
        "/products/scan/camera",
        files={"file": ("frame.png", _png_bytes(), "image/png")},
        headers=cashier_headers,
    )

    assert response.status_code == 200
    assert response.json()["product_name"] == "Orange Juice"


def test_scan_product_via_camera_invalid_image(client, cashier_headers):
    response = client.post(
        "/products/scan/camera",
        files={"file": ("frame.png", b"not-a-real-image", "image/png")},
        headers=cashier_headers,
    )

    assert response.status_code == 400


def test_scan_product_via_camera_no_barcode_detected(client, cashier_headers, monkeypatch):
    monkeypatch.setattr(
        "app.routers.product_routers.pyrxing.read_barcodes",
        lambda img: [],
    )

    response = client.post(
        "/products/scan/camera",
        files={"file": ("frame.png", _png_bytes(), "image/png")},
        headers=cashier_headers,
    )

    assert response.status_code == 422
