"""System-level endpoints: the IoT barcode webhook and its websocket fan-out."""


def test_iot_scan_broadcasts_to_connected_clients(client):
    with client.websocket_connect("/ws/checkout") as websocket:
        response = client.post("/api/iot-scan/9999999999")

        assert response.status_code == 200
        assert response.json() == {"status": "broadcasted", "barcode": "9999999999"}

        message = websocket.receive_text()
        assert message == "9999999999"


def test_iot_scan_with_no_listeners_still_succeeds(client):
    response = client.post("/api/iot-scan/1111111111")

    assert response.status_code == 200
    assert response.json() == {"status": "broadcasted", "barcode": "1111111111"}
