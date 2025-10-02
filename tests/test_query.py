from freezegun import freeze_time

# Positive 1
@freeze_time("2025-10-02")
def test_query_data(client):
    sensor_id = 1
    data = {
        "metric": "temperature",
        "value": 20,
        "timestamp": "2025-10-02T12:00:00"
    }
    response = client.post(f"/sensors/{sensor_id}/data", json=data)

    sensor_id = 1
    data = {
        "metric": "temperature",
        "value": 25,
        "timestamp": "2025-09-28T12:00:00"
    }
    response = client.post(f"/sensors/{sensor_id}/data", json=data)

    sensor_id = 2
    data = {
        "metric": "temperature",
        "value": 40,
        "timestamp": "2025-09-28T12:00:00"
    }
    response = client.post(f"/sensors/{sensor_id}/data", json=data)

    response = client.get("/query?metrics=temperature&statistic=avg&date_range=10")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert results[0]["metric"] == "temperature"
    assert "avg" in results[0]
    assert results[0]["avg"] == 22.5  # Average of 20 and 25
    assert results[1]["avg"] == 40

# Positive 2
@freeze_time("2025-10-02")
def test_query_data2(client):
    sensor_id = 1
    data = {
        "metric": "temperature",
        "value": 30,
        "timestamp": "2025-10-02T12:00:00"
    }
    response = client.post(f"/sensors/{sensor_id}/data", json=data)

    sensor_id = 1
    data = {
        "metric": "temperature",
        "value": 40,
        "timestamp": "2025-10-02T13:00:00"
    }
    response = client.post(f"/sensors/{sensor_id}/data", json=data)

    sensor_id = 1
    data = {
        "metric": "temperature",
        "value": 50,
        "timestamp": "2025-09-02T13:00:00"
    }
    response = client.post(f"/sensors/{sensor_id}/data", json=data)

    response = client.get("/query?sensors=1&metrics=temperature&statistic=max&date_range=10")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    for result in results:
        assert result["metric"] == "temperature"
        assert "max" in result
        assert result["max"] == 40  # Maximum of 30 and 40

# Positive 3
@freeze_time("2025-10-02")
def test_query_data3(client):
    sensor_id = 1
    data = {
        "metric": "temperature",
        "value": 25,
        "timestamp": "2025-10-02T12:00:00"
    }
    response = client.post(f"/sensors/{sensor_id}/data", json=data)

    sensor_id = 2
    data = {
        "metric": "humidity",
        "value": 65,
        "timestamp": "2025-10-02T13:00:00"
    }
    response = client.post(f"/sensors/{sensor_id}/data", json=data)

    sensor_id = 3
    data = {
        "metric": "wind_speed",
        "value": 10,
        "timestamp": "2025-10-02T13:00:00"
    }
    response = client.post(f"/sensors/{sensor_id}/data", json=data)

    response = client.get("/query?statistic=sum&date_range=10")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    metrics_found = set()
    for result in results:
        assert "sum" in result
        metrics_found.add(result["metric"])
    assert "temperature" in metrics_found
    assert "humidity" in metrics_found
    assert "wind_speed" in metrics_found

# Negative 1
def test_query_invalid_statistic(client):
    response = client.get("/query?sensors=1&metrics=temperature&statistic=invalid_stat&date_range=10")
    assert response.status_code == 422  # Unprocessable Entity

# Negative 2
def test_query_invalid_date_range(client):
    response = client.get("/query?sensors=1&metrics=temperature&statistic=avg&date_range=60")
    assert response.status_code == 400
    assert response.json()["detail"] == "date_range must be between 1 and 30"

# Neutral 1
def test_query_invalid_sensors_and_metrics(client):
    response = client.get("/query?sensors=999&metrics=unknown_metric&statistic=avg&date_range=10")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 0  # No data should be returned