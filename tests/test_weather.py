import pytest
from unittest.mock import patch, MagicMock
from app.weather import fetch_weather, fetch_weather_for_route_segments

@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_weather_success_extended(mock_get):
    # Mock successful response for the extended range API call
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "daily": {
            "precipitation_sum": [10.0, 15.0, 20.0],
            "temperature_2m_max": [28.0, 27.0, 26.0],
            "temperature_2m_min": [20.0, 19.0, 18.0],
            "windspeed_10m_max": [12.0, 14.0, 16.0]
        }
    }
    mock_get.return_value = mock_response

    result = await fetch_weather(26.14, 91.73, "2026-07-20")
    
    assert result["source"] == "open-meteo"
    assert result["rainfall_24h"] == 10.0
    assert result["rainfall_forecast_24h"] == 20.0
    assert result["temperature"] == 23.0  # (27 + 19)/2
    assert result["wind_speed"] == 14.0
    assert result["humidity"] == 75

@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_weather_fallback_to_single_day(mock_get):
    # Mock extended range failing (returning 400) and single day succeeding
    mock_response_fail = MagicMock()
    mock_response_fail.status_code = 400
    
    mock_response_success = MagicMock()
    mock_response_success.status_code = 200
    mock_response_success.json.return_value = {
        "daily": {
            "precipitation_sum": [5.0],
            "temperature_2m_max": [30.0],
            "temperature_2m_min": [20.0],
            "windspeed_10m_max": [8.0],
            "relative_humidity_2m_mean": [80.0]
        }
    }
    
    mock_get.side_effect = [mock_response_fail, mock_response_success]

    result = await fetch_weather(26.14, 91.73, "2026-07-20")
    
    assert result["source"] == "open-meteo"
    assert result["rainfall_24h"] == 5.0
    assert result["rainfall_forecast_24h"] == 5.0
    assert result["temperature"] == 25.0  # (30+20)/2
    assert result["wind_speed"] == 8.0
    assert result["humidity"] == 80.0

@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_weather_exception_fallback_to_estimate(mock_get):
    # Mock exceptions on both tries to trigger default rules
    mock_get.side_effect = Exception("API connection error")

    # Monsoon date (July)
    result_monsoon = await fetch_weather(26.14, 91.73, "2026-07-20")
    assert result_monsoon["source"] == "estimated"
    assert result_monsoon["rainfall_24h"] == 35
    assert result_monsoon["humidity"] == 85

    # Non-monsoon date (January)
    result_dry = await fetch_weather(26.14, 91.73, "2026-01-20")
    assert result_dry["source"] == "estimated"
    assert result_dry["rainfall_24h"] == 5
    assert result_dry["humidity"] == 60

@pytest.mark.asyncio
@patch("app.weather.fetch_weather")
async def test_fetch_weather_for_route_segments(mock_fetch):
    mock_fetch.return_value = {"mocked": True}
    
    segments = [
        {
            "from": {"lat": 20.0, "lng": 90.0},
            "to": {"lat": 22.0, "lng": 92.0}
        },
        {
            "from": {"lat": 22.0, "lng": 92.0},
            "to": {"lat": 24.0, "lng": 94.0}
        }
    ]
    
    results = await fetch_weather_for_route_segments(segments, "2026-07-20")
    assert len(results) == 2
    assert results[0] == {"mocked": True}
    assert results[1] == {"mocked": True}
    
    # Check mock calls were made with segment midpoints
    mock_fetch.assert_any_call(21.0, 91.0, "2026-07-20")
    mock_fetch.assert_any_call(23.0, 93.0, "2026-07-20")
