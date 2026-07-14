import pytest
from app.model import TransitRiskModel

@pytest.fixture
def model():
    return TransitRiskModel()

def test_model_initialization(model):
    # Verify that the model object initializes without raising errors
    assert model is not None
    # We should have either session, legacy model, or rule-based fallback active
    # (at least fallback works)

def test_predict_structure(model):
    features = {
        "rainfall_24h": 0.0,
        "rainfall_forecast_24h": 0.0,
        "temperature": 25.0,
        "wind_speed": 10.0,
        "humidity": 70.0,
        "slope": 5.0,
        "road_type": 0,  # highway
        "month": 1,      # January
        "historical_blockages": 0.0
    }
    
    result = model.predict(features)
    assert isinstance(result, dict)
    assert "risk_level" in result
    assert "risk_label" in result
    assert "confidence" in result
    assert "probabilities" in result
    assert result["risk_level"] in [0, 1, 2]
    assert result["risk_label"] in ["Safe", "Caution", "Danger"]
    assert 0.0 <= result["confidence"] <= 1.0
    assert "safe" in result["probabilities"]
    assert "caution" in result["probabilities"]
    assert "danger" in result["probabilities"]

def test_rule_based_predict_safe(model):
    features = {
        "rainfall_24h": 0.0,
        "rainfall_forecast_24h": 0.0,
        "temperature": 25.0,
        "wind_speed": 10.0,
        "humidity": 70.0,
        "slope": 5.0,
        "road_type": 0,
        "month": 1,
        "historical_blockages": 0
    }
    # Score should be 0. Thus, level 0 (Safe).
    result = model._rule_based_predict(features)
    assert result["risk_level"] == 0
    assert result["risk_label"] == "Safe"

def test_rule_based_predict_danger(model):
    features = {
        "rainfall_24h": 60.0,            # +3
        "rainfall_forecast_24h": 50.0,   # +2
        "temperature": 25.0,
        "wind_speed": 50.0,              # +1
        "humidity": 90.0,                # +1
        "slope": 35.0,                   # +2
        "road_type": 1,                  # +1
        "month": 7,                      # +2 (Monsoon)
        "historical_blockages": 15       # +2
    }
    # Score should be: 3 + 2 + 1 + 1 + 2 + 1 + 2 + 2 = 14 (>= 8). Thus, level 2 (Danger).
    result = model._rule_based_predict(features)
    assert result["risk_level"] == 2
    assert result["risk_label"] == "Danger"

def test_get_risk_reasons_safe(model):
    features = {
        "rainfall_24h": 0.0,
        "rainfall_forecast_24h": 0.0,
        "temperature": 25.0,
        "wind_speed": 10.0,
        "humidity": 70.0,
        "slope": 5.0,
        "road_type": 0,
        "month": 1,
        "historical_blockages": 0
    }
    reasons = model.get_risk_reasons(features, risk_level=0)
    assert len(reasons) > 0
    assert any("Weather conditions are favorable" in r for r in reasons)

def test_get_risk_reasons_danger(model):
    features = {
        "rainfall_24h": 60.0,
        "rainfall_forecast_24h": 50.0,
        "temperature": 25.0,
        "wind_speed": 50.0,
        "humidity": 90.0,
        "slope": 35.0,
        "road_type": 1,
        "month": 7,
        "historical_blockages": 15
    }
    reasons = model.get_risk_reasons(features, risk_level=2)
    assert len(reasons) > 0
    # Verify reasons capture the extreme values
    assert any("Very heavy rainfall" in r for r in reasons)
    assert any("Heavy rainfall forecast" in r for r in reasons)
    assert any("Very steep terrain" in r for r in reasons)
    assert any("Mountain road" in r for r in reasons)
    assert any("High wind speed" in r for r in reasons)
    assert any("Very high humidity" in r for r in reasons)
    assert any("Peak monsoon season" in r for r in reasons)
    assert any("Frequent historical blockages" in r for r in reasons)
