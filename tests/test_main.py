import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    # Check that it serves index.html (contains some HTML structure)
    assert "<html" in response.text.lower() or "<!doctype" in response.text.lower()

def test_api_cities():
    response = client.get("/api/cities")
    assert response.status_code == 200
    data = response.json()
    assert "cities" in data
    assert len(data["cities"]) > 0
    assert data["cities"][0]["name"] == "Aizawl"

def test_api_routes():
    response = client.get("/api/routes")
    assert response.status_code == 200
    data = response.json()
    assert "routes" in data
    assert len(data["routes"]) > 0

def test_api_destinations_success():
    response = client.get("/api/destinations/Aizawl")
    assert response.status_code == 200
    data = response.json()
    assert "destinations" in data
    assert "Silchar" in data["destinations"]

def test_api_destinations_not_found():
    response = client.get("/api/destinations/NonexistentCity")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

@patch("app.main.fetch_weather_for_route_segments", new_callable=AsyncMock)
def test_api_predict_success(mock_fetch_weather):
    # Mock weather returned for segment (our route between Aizawl and Silchar has 3 segments)
    mock_weather = {
        "rainfall_24h": 5.0,
        "rainfall_forecast_24h": 5.0,
        "temperature": 25.0,
        "wind_speed": 10.0,
        "humidity": 70.0,
        "source": "open-meteo",
        "date": "2026-07-20"
    }
    mock_fetch_weather.return_value = [mock_weather, mock_weather, mock_weather]

    payload = {
        "from_city": "Aizawl",
        "to_city": "Silchar",
        "date": "2026-07-20"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Assert prediction structure
    assert "risk_level" in data
    assert "risk_label" in data
    assert "confidence" in data
    assert "reasons" in data
    assert "segments" in data
    assert "weather" in data
    assert "route_info" in data
    
    # Route info check
    assert data["route_info"]["from"] == "Aizawl"
    assert data["route_info"]["to"] == "Silchar"
    assert len(data["segments"]) == 3

def test_api_predict_invalid_route():
    payload = {
        "from_city": "Aizawl",
        "to_city": "Gangtok",  # No direct route defined between Aizawl and Gangtok
        "date": "2026-07-20"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 404
    assert "detail" in response.json()

def test_api_predict_invalid_date():
    payload = {
        "from_city": "Aizawl",
        "to_city": "Silchar",
        "date": "invalid-date-format"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 400
    assert "detail" in response.json()
