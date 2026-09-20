def test_read_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200

    json_data = response.json()
    assert json_data["status"] == "success"
    assert json_data["message"] == "Supermarket POS API is active"


def test_docs_endpoint_accessible(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_unknown_route_returns_404(client):
    response = client.get("/this-route-does-not-exist")
    assert response.status_code == 404
