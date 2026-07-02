"""
Smart Transit Predictor — XGBoost Model Training Script

Generates synthetic training data based on realistic NE India weather/terrain patterns,
trains an XGBoost classifier, and saves the model to models/xgboost_model.pkl.

Run once: python train_model.py
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier
import joblib
import os


def generate_synthetic_data(n_samples=6000):
    """Generate realistic synthetic training data for NE India road risk prediction."""
    np.random.seed(42)

    data = []

    for _ in range(n_samples):
        # Random month (weighted toward monsoon for more balanced data)
        month_weights = [0.04, 0.04, 0.05, 0.05, 0.08, 0.15, 0.18, 0.16, 0.12, 0.06, 0.04, 0.03]
        month = np.random.choice(range(1, 13), p=month_weights)

        is_monsoon = month in [6, 7, 8, 9]
        is_pre_monsoon = month in [5, 10]

        # Rainfall — higher during monsoon
        if is_monsoon:
            rainfall_24h = np.random.exponential(35) + np.random.uniform(0, 20)
        elif is_pre_monsoon:
            rainfall_24h = np.random.exponential(15) + np.random.uniform(0, 10)
        else:
            rainfall_24h = np.random.exponential(5)
        rainfall_24h = min(rainfall_24h, 150)

        # Forecast rainfall — correlated with current rainfall
        rainfall_forecast = rainfall_24h * np.random.uniform(0.5, 1.5) + np.random.normal(0, 5)
        rainfall_forecast = max(0, min(rainfall_forecast, 120))

        # Temperature — varies by season and elevation
        if is_monsoon:
            temperature = np.random.normal(22, 4)
        else:
            temperature = np.random.normal(18, 6)
        temperature = max(5, min(temperature, 38))

        # Wind speed
        if is_monsoon:
            wind_speed = np.random.exponential(18) + 5
        else:
            wind_speed = np.random.exponential(10) + 2
        wind_speed = min(wind_speed, 70)

        # Humidity
        if is_monsoon:
            humidity = np.random.normal(88, 8)
        elif is_pre_monsoon:
            humidity = np.random.normal(75, 10)
        else:
            humidity = np.random.normal(60, 12)
        humidity = max(30, min(humidity, 100))

        # Terrain features
        slope = np.random.choice(
            [8, 10, 12, 15, 18, 22, 25, 28, 30, 32, 35, 38],
            p=[0.08, 0.08, 0.08, 0.10, 0.10, 0.10, 0.10, 0.08, 0.08, 0.08, 0.06, 0.06],
        )

        road_type = 1 if slope > 20 else np.random.choice([0, 1], p=[0.7, 0.3])

        historical_blockages = np.random.choice(
            range(0, 21),
            p=[
                0.05, 0.05, 0.08, 0.08, 0.07, 0.07, 0.07, 0.06, 0.06, 0.06,
                0.05, 0.05, 0.04, 0.04, 0.04, 0.03, 0.03, 0.03, 0.02, 0.01, 0.01,
            ],
        )

        # --- Assign risk label based on realistic rules ---
        danger_score = 0

        # Rainfall impact (strongest predictor)
        if rainfall_24h > 70:
            danger_score += 5
        elif rainfall_24h > 50:
            danger_score += 3.5
        elif rainfall_24h > 30:
            danger_score += 2
        elif rainfall_24h > 15:
            danger_score += 1

        # Forecast rainfall
        if rainfall_forecast > 50:
            danger_score += 2.5
        elif rainfall_forecast > 30:
            danger_score += 1.5
        elif rainfall_forecast > 15:
            danger_score += 0.5

        # Slope (critical factor)
        if slope > 35:
            danger_score += 3
        elif slope > 28:
            danger_score += 2
        elif slope > 20:
            danger_score += 1
        elif slope > 12:
            danger_score += 0.5

        # Road type
        if road_type == 1:
            danger_score += 1

        # Wind
        if wind_speed > 45:
            danger_score += 1.5
        elif wind_speed > 30:
            danger_score += 0.5

        # Humidity
        if humidity > 90:
            danger_score += 1
        elif humidity > 80:
            danger_score += 0.5

        # Season
        if is_monsoon:
            danger_score += 1.5
        elif is_pre_monsoon:
            danger_score += 0.5

        # Historical blockages
        if historical_blockages > 14:
            danger_score += 2.5
        elif historical_blockages > 10:
            danger_score += 1.5
        elif historical_blockages > 5:
            danger_score += 0.5

        # Interaction effects
        if rainfall_24h > 40 and slope > 25:
            danger_score += 2
        if is_monsoon and slope > 30 and rainfall_24h > 20:
            danger_score += 1.5
        if historical_blockages > 10 and rainfall_24h > 30:
            danger_score += 1

        # Determine label
        if danger_score >= 9:
            label = 2  # Danger
        elif danger_score >= 4.5:
            label = 1  # Caution
        else:
            label = 0  # Safe

        # Add noise (10% random flips for realism)
        if np.random.random() < 0.10:
            if label == 0:
                label = np.random.choice([0, 1], p=[0.5, 0.5])
            elif label == 1:
                label = np.random.choice([0, 1, 2], p=[0.2, 0.5, 0.3])
            elif label == 2:
                label = np.random.choice([1, 2], p=[0.3, 0.7])

        data.append(
            {
                "rainfall_24h": round(rainfall_24h, 1),
                "rainfall_forecast_24h": round(rainfall_forecast, 1),
                "temperature": round(temperature, 1),
                "wind_speed": round(wind_speed, 1),
                "humidity": round(humidity, 1),
                "slope": slope,
                "road_type": road_type,
                "month": month,
                "historical_blockages": historical_blockages,
                "risk_level": label,
            }
        )

    return pd.DataFrame(data)


def train_model():
    """Train XGBoost classifier and save the model."""
    print("=" * 60)
    print(">> Smart Transit Predictor - Model Training")
    print("=" * 60)

    # Generate synthetic data
    print("\n[*] Generating synthetic training data...")
    df = generate_synthetic_data(6000)
    print(f"   Generated {len(df)} samples")
    print(f"   Class distribution:")
    for level, label in {0: "Safe", 1: "Caution", 2: "Danger"}.items():
        count = len(df[df["risk_level"] == level])
        print(f"     {label}: {count} ({count/len(df)*100:.1f}%)")

    # Prepare features and labels
    feature_columns = [
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

    X = df[feature_columns].values
    y = df["risk_level"].values

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\n[*] Train/test split: {len(X_train)} train / {len(X_test)} test")

    # Train XGBoost
    print("\n[*] Training XGBoost classifier...")
    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        objective="multi:softprob",
        num_class=3,
        eval_metric="mlogloss",
        random_state=42,
        tree_method="hist",
    )

    model.fit(
        X_train,
        y_train,
        eval_set=[(X_test, y_test)],
        verbose=False,
    )

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n[OK] Training complete!")
    print(f"   Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)")
    print(f"\n[*] Classification Report:")
    print(
        classification_report(
            y_test, y_pred, target_names=["Safe", "Caution", "Danger"]
        )
    )

    # Feature importance
    print("[*] Feature Importance:")
    importances = model.feature_importances_
    for feat, imp in sorted(
        zip(feature_columns, importances), key=lambda x: x[1], reverse=True
    ):
        bar = "#" * int(imp * 50)
        print(f"   {feat:<25} {imp:.4f} {bar}")

    # Save model
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, "xgboost_model.pkl")
    joblib.dump(model, model_path)
    print(f"\n[SAVED] Model saved to: {model_path}")

    # Also save the training data for reference
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    training_data_path = os.path.join(data_dir, "training_data.csv")
    df.to_csv(training_data_path, index=False)
    print(f"[SAVED] Training data saved to: {training_data_path}")

    print("\n" + "=" * 60)
    print("[DONE] Model training complete! You can now start the server:")
    print("   python -m uvicorn app.main:app --reload")
    print("=" * 60)

    return model, accuracy


if __name__ == "__main__":
    train_model()
