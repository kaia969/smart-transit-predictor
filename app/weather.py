"""Weather data fetcher using Open-Meteo API (free, no API key needed)."""

import httpx
from datetime import datetime, timedelta
import asyncio

OPEN_METEO_BASE = "https://api.open-meteo.com/v1/forecast"

async def fetch_weather(lat: float, lng: float, date: str) -> dict:
    """Fetch weather data for a location and date.
    
    Args:
        lat: Latitude
        lng: Longitude  
        date: Date string in YYYY-MM-DD format
    
    Returns:
        dict with rainfall_24h, rainfall_forecast_24h, temperature, wind_speed, humidity
    """
    try:
        params = {
            "latitude": lat,
            "longitude": lng,
            "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min,windspeed_10m_max,relative_humidity_2m_mean",  
            "timezone": "Asia/Kolkata",
            "start_date": date,
            "end_date": date,
        }
        
        # Also try to get the day before for "last 24h" data
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        yesterday = (date_obj - timedelta(days=1)).strftime("%Y-%m-%d")
        tomorrow = (date_obj + timedelta(days=1)).strftime("%Y-%m-%d")
        
        params_extended = {
            "latitude": lat,
            "longitude": lng,
            "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min,windspeed_10m_max",
            "timezone": "Asia/Kolkata",
            "start_date": yesterday,
            "end_date": tomorrow,
        }
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Try extended range first
            try:
                response = await client.get(OPEN_METEO_BASE, params=params_extended)
                if response.status_code == 200:
                    data = response.json()
                    daily = data.get("daily", {})
                    
                    precip = daily.get("precipitation_sum", [0, 0, 0])
                    temp_max = daily.get("temperature_2m_max", [25, 25, 25])
                    temp_min = daily.get("temperature_2m_min", [18, 18, 18])
                    wind = daily.get("windspeed_10m_max", [10, 10, 10])
                    
                    # Index: 0=yesterday, 1=today, 2=tomorrow
                    rainfall_24h = precip[0] if len(precip) > 0 else 0
                    rainfall_forecast = precip[2] if len(precip) > 2 else precip[1] if len(precip) > 1 else 0
                    temperature = (temp_max[1] + temp_min[1]) / 2 if len(temp_max) > 1 else 25
                    wind_speed = wind[1] if len(wind) > 1 else 10
                    
                    return {
                        "rainfall_24h": rainfall_24h or 0,
                        "rainfall_forecast_24h": rainfall_forecast or 0,
                        "temperature": temperature or 25,
                        "wind_speed": wind_speed or 10,
                        "humidity": 75,  # Default if not available in extended
                        "source": "open-meteo",
                        "date": date
                    }
            except Exception:
                pass
            
            # Fallback to single day
            response = await client.get(OPEN_METEO_BASE, params=params)
            if response.status_code == 200:
                data = response.json()
                daily = data.get("daily", {})
                
                precip = daily.get("precipitation_sum", [0])
                temp_max = daily.get("temperature_2m_max", [25])
                temp_min = daily.get("temperature_2m_min", [18])
                wind = daily.get("windspeed_10m_max", [10])
                humidity_vals = daily.get("relative_humidity_2m_mean", [75])
                
                return {
                    "rainfall_24h": precip[0] if precip[0] else 0,
                    "rainfall_forecast_24h": precip[0] if precip[0] else 0,
                    "temperature": ((temp_max[0] or 25) + (temp_min[0] or 18)) / 2,
                    "wind_speed": wind[0] if wind[0] else 10,
                    "humidity": humidity_vals[0] if humidity_vals[0] else 75,
                    "source": "open-meteo",
                    "date": date
                }
    except Exception as e:
        print(f"Weather API error: {e}")
    
    # Return defaults if API fails
    month = int(date.split("-")[1])
    is_monsoon = month in [6, 7, 8, 9]
    return {
        "rainfall_24h": 35 if is_monsoon else 5,
        "rainfall_forecast_24h": 30 if is_monsoon else 3,
        "temperature": 22 if is_monsoon else 18,
        "wind_speed": 20 if is_monsoon else 8,
        "humidity": 85 if is_monsoon else 60,
        "source": "estimated",
        "date": date
    }

async def fetch_weather_for_route_segments(segments: list, date: str) -> list:
    """Fetch weather for the midpoint of each route segment."""
    tasks = []
    for seg in segments:
        mid_lat = (seg["from"]["lat"] + seg["to"]["lat"]) / 2
        mid_lng = (seg["from"]["lng"] + seg["to"]["lng"]) / 2
        tasks.append(fetch_weather(mid_lat, mid_lng, date))
    
    results = await asyncio.gather(*tasks)
    return results
