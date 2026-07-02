"""XGBoost ML model wrapper for road risk prediction."""

import joblib
import numpy as np
import os


class TransitRiskModel:
    """Predicts road transit risk using a trained XGBoost model."""

    def __init__(self):
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "models", "xgboost_model.pkl"
        )
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            print(f"[OK] ML model loaded from {model_path}")
        else:
            self.model = None
            print("[WARN] No trained model found -- using rule-based fallback predictions")

    def predict(self, features: dict) -> dict:
        """Predict risk level from weather + terrain features.

        Features expected:
        - rainfall_24h (mm)
        - rainfall_forecast_24h (mm)
        - temperature (°C)
        - wind_speed (km/h)
        - humidity (%)
        - slope (degrees)
        - road_type (0=highway, 1=mountain)
        - month (1-12)
        - historical_blockages (per year)

        Returns:
            dict with risk_level (0,1,2), risk_label, confidence, probabilities
        """
        if self.model is None:
            return self._rule_based_predict(features)

        feature_array = np.array(
            [
                [
                    features["rainfall_24h"],
                    features["rainfall_forecast_24h"],
                    features["temperature"],
                    features["wind_speed"],
                    features["humidity"],
                    features["slope"],
                    features["road_type"],
                    features["month"],
                    features["historical_blockages"],
                ]
            ]
        )

        prediction = int(self.model.predict(feature_array)[0])
        probabilities = self.model.predict_proba(feature_array)[0]

        labels = {0: "Safe", 1: "Caution", 2: "Danger"}

        return {
            "risk_level": prediction,
            "risk_label": labels[prediction],
            "confidence": float(max(probabilities)),
            "probabilities": {
                "safe": float(probabilities[0]),
                "caution": float(probabilities[1]),
                "danger": float(probabilities[2]),
            },
        }

    def _rule_based_predict(self, features: dict) -> dict:
        """Fallback rule-based prediction when ML model is unavailable."""
        score = 0

        # Rainfall impact
        if features["rainfall_24h"] > 50:
            score += 3
        elif features["rainfall_24h"] > 25:
            score += 2
        elif features["rainfall_24h"] > 10:
            score += 1

        # Forecast rainfall
        if features["rainfall_forecast_24h"] > 40:
            score += 2
        elif features["rainfall_forecast_24h"] > 20:
            score += 1

        # Terrain slope
        if features["slope"] > 30:
            score += 2
        elif features["slope"] > 20:
            score += 1

        # Road type
        if features["road_type"] == 1:
            score += 1

        # Wind
        if features["wind_speed"] > 40:
            score += 1

        # Humidity
        if features["humidity"] > 85:
            score += 1

        # Historical blockages
        if features["historical_blockages"] > 10:
            score += 2
        elif features["historical_blockages"] > 5:
            score += 1

        # Monsoon season
        month = features["month"]
        if month in [6, 7, 8, 9]:
            score += 2
        elif month in [5, 10]:
            score += 1

        # Determine risk level
        if score >= 8:
            level = 2
        elif score >= 4:
            level = 1
        else:
            level = 0

        labels = {0: "Safe", 1: "Caution", 2: "Danger"}
        conf_map = {0: 0.82, 1: 0.70, 2: 0.85}

        return {
            "risk_level": level,
            "risk_label": labels[level],
            "confidence": conf_map[level],
            "probabilities": {
                "safe": 0.7 if level == 0 else (0.15 if level == 1 else 0.05),
                "caution": 0.2 if level == 0 else (0.65 if level == 1 else 0.15),
                "danger": 0.1 if level == 0 else (0.20 if level == 1 else 0.80),
            },
        }

    def get_risk_reasons(self, features: dict, risk_level: int) -> list:
        """Generate human-readable reasons for the risk assessment."""
        reasons = []

        # Rainfall reasons
        if features["rainfall_24h"] > 50:
            reasons.append(
                f"🌧️ Very heavy rainfall recorded ({features['rainfall_24h']:.1f}mm in 24h)"
            )
        elif features["rainfall_24h"] > 25:
            reasons.append(
                f"🌧️ Heavy rainfall recorded ({features['rainfall_24h']:.1f}mm in 24h)"
            )
        elif features["rainfall_24h"] > 10:
            reasons.append(
                f"🌦️ Moderate rainfall ({features['rainfall_24h']:.1f}mm in 24h)"
            )

        # Forecast reasons
        if features["rainfall_forecast_24h"] > 40:
            reasons.append(
                f"⛈️ Heavy rainfall forecast ({features['rainfall_forecast_24h']:.1f}mm expected)"
            )
        elif features["rainfall_forecast_24h"] > 20:
            reasons.append(
                f"🌧️ Moderate rainfall forecast ({features['rainfall_forecast_24h']:.1f}mm expected)"
            )

        # Terrain reasons
        if features["slope"] > 30:
            reasons.append(
                f"⛰️ Very steep terrain ({features['slope']:.0f}° slope) — high landslide risk"
            )
        elif features["slope"] > 20:
            reasons.append(
                f"🏔️ Steep terrain ({features['slope']:.0f}° slope)"
            )

        # Road type
        if features["road_type"] == 1:
            reasons.append("🛤️ Mountain road — narrower and more vulnerable")

        # Wind
        if features["wind_speed"] > 40:
            reasons.append(
                f"💨 High wind speed ({features['wind_speed']:.1f} km/h)"
            )

        # Humidity
        if features["humidity"] > 85:
            reasons.append(
                f"💧 Very high humidity ({features['humidity']:.0f}%) — reduced visibility"
            )

        # Monsoon season
        month = features["month"]
        if month in [6, 7, 8, 9]:
            month_names = {6: "June", 7: "July", 8: "August", 9: "September"}
            reasons.append(
                f"📅 Peak monsoon season ({month_names[month]}) — historically high risk"
            )

        # Historical blockages
        if features["historical_blockages"] > 10:
            reasons.append(
                f"⚠️ Frequent historical blockages ({int(features['historical_blockages'])}/year)"
            )
        elif features["historical_blockages"] > 5:
            reasons.append(
                f"📊 Moderate historical blockage frequency ({int(features['historical_blockages'])}/year)"
            )

        # Safe fallback
        if risk_level == 0 and not reasons:
            reasons.append("✅ Weather conditions are favorable")
            reasons.append("✅ Terrain is manageable")
            reasons.append("✅ No historical risk factors detected")

        return reasons
