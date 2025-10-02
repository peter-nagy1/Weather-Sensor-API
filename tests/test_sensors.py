from freezegun import freeze_time

# Positive 1
@freeze_time("2025-10-02")
def test_post_sensor_data(client):
    sensor_id = 1
    data = {
        "metric": "temperature",
        "value": 23.5,
        "timestamp": "2025-10-02T12:00:00"
    }

    response = client.post(f"/sensors/{sensor_id}/data", json=data)
    assert response.status_code == 200
    data = response.json()
    assert data["sensor_id"] == sensor_id
    assert data["metric"] == "temperature"
    assert data["value"] == 23.5
    assert data["timestamp"] == "2025-10-02T12:00:00"

# Positive 2
@freeze_time("2025-10-02")
def test_post_sensor_data2(client):
    sensor_id = 2
    data = {
        "metric": "humidity",
        "value": 60,
        "timestamp": "2025-10-02T12:05:00"
    }

    response = client.post(f"/sensors/{sensor_id}/data", json=data)
    assert response.status_code == 200
    data = response.json()
    assert data["sensor_id"] == sensor_id
    assert data["metric"] == "humidity"
    assert data["value"] == 60
    assert data["timestamp"] == "2025-10-02T12:05:00"

# Negative 1
@freeze_time("2025-10-02")
def test_post_invalid_sensor_data(client):
    sensor_id = 1
    data = {
        "metric": "temperature",
        "value": "invalid_value",  # Invalid value type
        "timestamp": "2025-10-02T12:00:00"
    }

    response = client.post(f"/sensors/{sensor_id}/data", json=data)
    assert response.status_code == 422  # Unprocessable Entity

# Negative 2
@freeze_time("2025-10-02")
def test_post_sensor_missing_value_field(client):
    sensor_id = 1
    data = {
        "metric": "temperature",
        # Missing 'value' field
        "timestamp": "2025-10-02T12:00:00"
    }

    response = client.post(f"/sensors/{sensor_id}/data", json=data)
    assert response.status_code == 422  # Unprocessable Entity