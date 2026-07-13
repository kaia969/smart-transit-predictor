"""Convert trained XGBoost model to portable ONNX format.

Run this ONCE after training. The ONNX file ships with the repo
so fresh systems never need XGBoost installed.

Usage:
    pip install -r requirements-dev.txt
    python export_onnx.py
"""

import joblib
import numpy as np
import os
import sys


def export_to_onnx():
    print("=" * 60)
    print("ONNX Model Export - Smart Transit Predictor")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    pkl_path = os.path.join(base_dir, "models", "xgboost_model.pkl")
    onnx_path = os.path.join(base_dir, "models", "transit_risk_model.onnx")

    # Step 1: Load XGBoost model
    print("\n[1/4] Loading XGBoost model...")
    if not os.path.exists(pkl_path):
        print(f"  [FAIL] Model not found at: {pkl_path}")
        print("  Run 'python train_model.py' first.")
        sys.exit(1)
    model = joblib.load(pkl_path)
    print(f"  Loaded from: {pkl_path}")

    # Step 2: Convert to ONNX
    print("\n[2/4] Converting to ONNX format...")
    try:
        from onnxmltools import convert_xgboost
        from onnxmltools.convert.common.data_types import FloatTensorType

        initial_type = [("features", FloatTensorType([None, 9]))]
        onnx_model = convert_xgboost(
            model, initial_types=initial_type, target_opset=15
        )
    except ImportError:
        print("  [FAIL] onnxmltools not installed.")
        print("  Run: pip install -r requirements-dev.txt")
        sys.exit(1)

    # Step 3: Save ONNX
    print("\n[3/4] Saving ONNX model...")
    os.makedirs(os.path.dirname(onnx_path), exist_ok=True)
    with open(onnx_path, "wb") as f:
        f.write(onnx_model.SerializeToString())
    print(f"  Saved to: {onnx_path}")

    # Step 4: Verify
    print("\n[4/4] Verifying ONNX model...")
    import onnxruntime as ort

    session = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name

    # Test: moderate rain, steep slope, monsoon month
    test_input = np.array(
        [[35.0, 25.0, 22.0, 15.0, 80.0, 30.0, 1.0, 7.0, 10.0]],
        dtype=np.float32,
    )

    results = session.run(None, {input_name: test_input})
    onnx_pred = int(results[0][0])

    # Also predict with original
    original_pred = int(model.predict(test_input)[0])

    labels = {0: "Safe", 1: "Caution", 2: "Danger"}
    print(f"  XGBoost prediction: {labels.get(original_pred, original_pred)}")
    print(f"  ONNX prediction:    {labels.get(onnx_pred, onnx_pred)}")

    if original_pred == onnx_pred:
        print("  [OK] Predictions match!")
    else:
        print("  [WARN] Predictions differ - check conversion")

    # File sizes
    pkl_size = os.path.getsize(pkl_path) / 1024
    onnx_size = os.path.getsize(onnx_path) / 1024
    print(f"\n  PKL size:  {pkl_size:.0f} KB")
    print(f"  ONNX size: {onnx_size:.0f} KB")

    print("\n" + "=" * 60)
    print("[DONE] ONNX export complete!")
    print("You can now commit models/transit_risk_model.onnx to your repo.")
    print("Fresh systems only need 'pip install -r requirements.txt'")
    print("=" * 60)


if __name__ == "__main__":
    export_to_onnx()
