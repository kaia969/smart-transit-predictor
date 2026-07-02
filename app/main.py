"""Smart Transit Predictor — FastAPI Backend"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import os

from .routes import get_cities, get_routes, get_route, get_available_routes_for_city
from .weather import fetch_weather_for_route_segments
from .model import TransitRiskModel

app = FastAPI(
    title="Smart Transit Predictor",
    description="Road risk prediction for Northeast India",
    version="1.0.0"
)

# Serve frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Initialize ML model
model = TransitRiskModel()


class PredictRequest(BaseModel):
    from_city: str
    to_city: str
    date: str  # YYYY-MM-DD


@app.get("/")
async def root():
    return FileResponse(os.path.join(frontend_dir, "index.html"))


@app.get("/api/cities")
async def api_cities():
    return {"cities": get_cities()}


@app.get("/api/routes")
async def api_routes():
    return {"routes": get_routes()}


@app.get("/api/destinations/{city_name}")
async def api_destinations(city_name: str):
    destinations = get_available_routes_for_city(city_name)
    if not destinations:
        raise HTTPException(status_code=404, detail=f"No routes found for {city_name}")
    return {"destinations": destinations}


@app.post("/api/predict")
async def api_predict(request: PredictRequest):
    # Validate route exists
    route = get_route(request.from_city, request.to_city)
    if not route:
        raise HTTPException(
            status_code=404,
            detail=f"No route found between {request.from_city} and {request.to_city}"
        )
    
    # Validate date format
    try:
        date_obj = datetime.strptime(request.date, "%Y-%m-%d")
        month = date_obj.month
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # Fetch weather for each segment
    segments = route["segments"]
    weather_data = await fetch_weather_for_route_segments(segments, request.date)
    
    # Predict risk for each segment
    segment_results = []
    overall_risk_level = 0
    overall_confidence = 0.0
    all_reasons = []
    
    for i, (seg, weather) in enumerate(zip(segments, weather_data)):
        features = {
            "rainfall_24h": weather["rainfall_24h"],
            "rainfall_forecast_24h": weather["rainfall_forecast_24h"],
            "temperature": weather["temperature"],
            "wind_speed": weather["wind_speed"],
            "humidity": weather["humidity"],
            "slope": seg["slope"],
            "road_type": seg["road_type"],
            "month": month,
            "historical_blockages": seg["historical_blockages"]
        }
        
        prediction = model.predict(features)
        reasons = model.get_risk_reasons(features, prediction["risk_level"])
        
        segment_results.append({
            "from": seg["from"],
            "to": seg["to"],
            "risk_level": prediction["risk_level"],
            "risk_label": prediction["risk_label"],
            "confidence": prediction["confidence"],
            "length_km": seg["length_km"],
            "weather": weather,
            "reasons": reasons
        })
        
        # Overall risk = max of all segments
        if prediction["risk_level"] > overall_risk_level:
            overall_risk_level = prediction["risk_level"]
            overall_confidence = prediction["confidence"]
        
        # Collect unique reasons
        for reason in reasons:
            if reason not in all_reasons:
                all_reasons.append(reason)
    
    labels = {0: "Safe", 1: "Caution", 2: "Danger"}
    
    # If no segment was worse than safe, use max confidence from any segment
    if overall_confidence == 0.0 and segment_results:
        overall_confidence = max(s["confidence"] for s in segment_results)
    
    # Calculate average weather along route
    avg_weather = {
        "rainfall_24h": sum(w["rainfall_24h"] for w in weather_data) / len(weather_data),
        "rainfall_forecast_24h": sum(w["rainfall_forecast_24h"] for w in weather_data) / len(weather_data),
        "temperature": sum(w["temperature"] for w in weather_data) / len(weather_data),
        "wind_speed": sum(w["wind_speed"] for w in weather_data) / len(weather_data),
        "humidity": sum(w["humidity"] for w in weather_data) / len(weather_data),
    }
    
    return {
        "risk_level": overall_risk_level,
        "risk_label": labels[overall_risk_level],
        "confidence": overall_confidence,
        "reasons": all_reasons,
        "segments": segment_results,
        "weather": avg_weather,
        "route_info": {
            "from": route["from"],
            "to": route["to"],
            "distance_km": route["distance_km"],
            "estimated_time": route["estimated_time"],
            "risk_factors": route["risk_factors"]
        }
    }
