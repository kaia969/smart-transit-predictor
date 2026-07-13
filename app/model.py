"""ONNX-based ML model wrapper for road risk prediction.

Uses ONNX Runtime for portable, plug-and-play inference.
No need to install XGBoost or retrain on new systems.
Falls back to rule-based prediction if ONNX model is missing.
"""

import numpy as np
import os


class TransitRiskModel:
    """Predicts road transit risk using an ONNX model (portable, no retraining)."""

    FEATURE_NAMES = [
        "rainfall_24h",
        "rainfall_forecast_24h",
        "temperature",
        "wind_speed",
        "humidity",
        "slope",
        "road_type",
        "month",
        "historical_blockages",
    ]

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        onnx_path = os.path.join(base_dir, "models", "transit_risk_model.onnx")
        pkl_path = os.path.join(base_dir, "models", "xgboost_model.pkl")

        self.session = None
        self.input_name = None
        self._legacy_model = None

        # Priority 1: ONNX model (portable, recommended)
        if os.path.exists(onnx_path):
            try:
                import onnxruntime as ort

                self.session = ort.InferenceSession(
                    onnx_path,
                    providers=["CPUExecutionProvider"],
                )
                self.input_name = self.session.get_inputs()[0].name
                print(f"[OK] ONNX model loaded from {onnx_path}")
                return
            except Exception as e:
                print(f"[WARN] Failed to load ONNX model: {e}")
                self.session = None

        # Priority 2: Legacy XGBoost pkl (backward compatible)
        if os.path.exists(pkl_path):
            try:
                import joblib

                self._legacy_model = joblib.load(pkl_path)
                print(f"[OK] Legacy XGBoost model loaded from {pkl_path}")
                return
            except Exception as e:
                print(f"[WARN] Failed to load legacy model: {e}")
                self._legacy_model = None

        # Priority 3: Rule-based fallback
        print("[WARN] No trained model found -- using rule-based fallback predictions")

    def predict(self, features: dict) -> dict:
        """Predict risk level from weather + terrain features.

        Features expected:
        - rainfall_24h (mm)
        - rainfall_forecast_24h (mm)
        - temperature (deg C)
        - wind_speed (km/h)
        - humidity (%)
        - slope (degrees)
        - road_type (0=highway, 1=mountain)
        - month (1-12)
        - historical_blockages (per year)

        Returns:
            dict with risk_level (0,1,2), risk_label, confidence, probabilities
        """
        # ONNX inference
        if self.session is not None:
            return self._onnx_predict(features)

        # Legacy XGBoost inference
        if self._legacy_model is not None:
            return self._legacy_predict(features)

        # Rule-based fallback
        return self._rule_based_predict(features)

    def _onnx_predict(self, features: dict) -> dict:
        """Predict using ONNX Runtime (primary, portable)."""
        feature_array = np.array(
            [[features[name] for name in self.FEATURE_NAMES]],
            dtype=np.float32,
        )

        results = self.session.run(None, {self.input_name: feature_array})

        prediction = int(results[0][0])

        # ONNX probability output varies by converter:
        # - Could be list of dicts: [{0: p0, 1: p1, 2: p2}]
        # - Could be numpy array: [[p0, p1, p2]]
        raw_probs = results[1][0]
        if isinstance(raw_probs, dict):
            probabilities = [float(raw_probs.get(i, 0.0)) for i in range(3)]
        elif isinstance(raw_probs, np.ndarray):
            probabilities = [float(raw_probs[i]) for i in range(3)]
        elif isinstance(raw_probs, (list, tuple)):
            probabilities = [float(p) for p in raw_probs[:3]]
        else:
            probabilities = [0.33, 0.34, 0.33]

        labels = {0: "Safe", 1: "Caution", 2: "Danger"}

        return {
            "risk_level": prediction,
            "risk_label": labels[prediction],
            "confidence": float(max(probabilities)),
            "probabilities": {
                "safe": probabilities[0],
                "caution": probabilities[1],
                "danger": probabilities[2],
            },
        }

    def _legacy_predict(self, features: dict) -> dict:
        """Predict using legacy XGBoost pkl model (backward compatible)."""
        feature_array = np.array(
            [[features[name] for name in self.FEATURE_NAMES]]
        )

        prediction = int(self._legacy_model.predict(feature_array)[0])
        probabilities = self._legacy_model.predict_proba(feature_array)[0]

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
        """Fallback rule-based prediction when no ML model is available."""
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
                f"\U0001f327\ufe0f Very heavy rainfall recorded ({features['rainfall_24h']:.1f}mm in 24h)"
            )
        elif features["rainfall_24h"] > 25:
            reasons.append(
                f"\U0001f327\ufe0f Heavy rainfall recorded ({features['rainfall_24h']:.1f}mm in 24h)"
            )
        elif features["rainfall_24h"] > 10:
            reasons.append(
                f"\U0001f326\ufe0f Moderate rainfall ({features['rainfall_24h']:.1f}mm in 24h)"
            )

        # Forecast reasons
        if features["rainfall_forecast_24h"] > 40:
            reasons.append(
                f"\u26c8\ufe0f Heavy rainfall forecast ({features['rainfall_forecast_24h']:.1f}mm expected)"
            )
        elif features["rainfall_forecast_24h"] > 20:
            reasons.append(
                f"\U0001f327\ufe0f Moderate rainfall forecast ({features['rainfall_forecast_24h']:.1f}mm expected)"
            )

        # Terrain reasons
        if features["slope"] > 30:
            reasons.append(
                f"\u26f0\ufe0f Very steep terrain ({features['slope']:.0f}\u00b0 slope) \u2014 high landslide risk"
            )
        elif features["slope"] > 20:
            reasons.append(
                f"\U0001f3d4\ufe0f Steep terrain ({features['slope']:.0f}\u00b0 slope)"
            )

        # Road type
        if features["road_type"] == 1:
            reasons.append("\U0001f6e4\ufe0f Mountain road \u2014 narrower and more vulnerable")

        # Wind
        if features["wind_speed"] > 40:
            reasons.append(
                f"\U0001f4a8 High wind speed ({features['wind_speed']:.1f} km/h)"
            )

        # Humidity
        if features["humidity"] > 85:
            reasons.append(
                f"\U0001f4a7 Very high humidity ({features['humidity']:.0f}%) \u2014 reduced visibility"
            )

        # Monsoon season
        month = features["month"]
        if month in [6, 7, 8, 9]:
            month_names = {6: "June", 7: "July", 8: "August", 9: "September"}
            reasons.append(
                f"\U0001f4c5 Peak monsoon season ({month_names[month]}) \u2014 historically high risk"
            )

        # Historical blockages
        if features["historical_blockages"] > 10:
            reasons.append(
                f"\u26a0\ufe0f Frequent historical blockages ({int(features['historical_blockages'])}/year)"
            )
        elif features["historical_blockages"] > 5:
            reasons.append(
                f"\U0001f4ca Moderate historical blockage frequency ({int(features['historical_blockages'])}/year)"
            )

        # Safe fallback
        if risk_level == 0 and not reasons:
            reasons.append("\u2705 Weather conditions are favorable")
            reasons.append("\u2705 Terrain is manageable")
            reasons.append("\u2705 No historical risk factors detected")

        return reasons
