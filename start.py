"""
Smart Transit Predictor - One-Click Bootstrap & Start Script

Usage:
    python start.py          # Install deps + start server
    python start.py --port 3000   # Custom port
    python start.py --no-open     # Don't auto-open browser

This script handles EVERYTHING:
  1. Checks Python version (>= 3.10)
  2. Installs dependencies automatically (if missing)
  3. Verifies the ONNX model exists
  4. Starts the FastAPI server
  5. Opens the browser automatically
"""

import subprocess
import sys
import os
import time
import importlib
import argparse

# ──────────────── Constants ────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS_FILE = os.path.join(BASE_DIR, "requirements.txt")
ONNX_MODEL_PATH = os.path.join(BASE_DIR, "models", "transit_risk_model.onnx")
PKL_MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_model.pkl")
MIN_PYTHON = (3, 10)


def print_banner():
    print()
    print("=" * 60)
    print("  SMART TRANSIT PREDICTOR - Northeast India")
    print("  AI-Powered Road Safety Prediction System")
    print("=" * 60)
    print()


def check_python_version():
    """Ensure Python >= 3.10."""
    print("[1/4] Checking Python version...")
    current = sys.version_info[:2]
    if current < MIN_PYTHON:
        print(f"  [FAIL] Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required, "
              f"found {current[0]}.{current[1]}")
        print(f"  Download from: https://www.python.org/downloads/")
        sys.exit(1)
    print(f"  [OK] Python {current[0]}.{current[1]}")


def check_and_install_dependencies():
    """Check if required packages are installed, install if missing."""
    print("\n[2/4] Checking dependencies...")

    # Core packages to verify
    required_packages = {
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "onnxruntime": "onnxruntime",
        "pandas": "pandas",
        "numpy": "numpy",
        "httpx": "httpx",
    }

    missing = []
    for import_name, pip_name in required_packages.items():
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing.append(pip_name)

    if not missing:
        print("  [OK] All dependencies already installed")
        return

    print(f"  Missing packages: {', '.join(missing)}")
    print(f"  Installing from {REQUIREMENTS_FILE}...")

    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE, "-q"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"  [FAIL] pip install failed:")
        print(f"  {result.stderr}")
        print()
        print("  Try running manually:")
        print(f"    pip install -r {REQUIREMENTS_FILE}")
        sys.exit(1)

    print("  [OK] Dependencies installed successfully")


def check_model():
    """Verify the ONNX model exists."""
    print("\n[3/4] Checking AI model...")

    if os.path.exists(ONNX_MODEL_PATH):
        size_kb = os.path.getsize(ONNX_MODEL_PATH) / 1024
        print(f"  [OK] ONNX model found ({size_kb:.0f} KB)")
        return True

    if os.path.exists(PKL_MODEL_PATH):
        size_kb = os.path.getsize(PKL_MODEL_PATH) / 1024
        print(f"  [OK] Legacy XGBoost model found ({size_kb:.0f} KB)")
        print(f"  TIP: Run 'python export_onnx.py' to convert to portable ONNX format")
        return True

    print("  [WARN] No trained model found!")
    print("  The app will use rule-based predictions (less accurate)")
    print("  To train a model, run:")
    print("    pip install -r requirements-dev.txt")
    print("    python train_model.py")
    print("    python export_onnx.py")
    return False


def start_server(port=8000, open_browser=True):
    """Start the FastAPI server."""
    print(f"\n[4/4] Starting server on port {port}...")
    url = f"http://localhost:{port}"
    print(f"  URL: {url}")
    print()
    print("  Press Ctrl+C to stop the server")
    print("-" * 60)
    print()

    # Open browser after a short delay
    if open_browser:
        import threading

        def _open_browser():
            time.sleep(2)
            try:
                import webbrowser
                webbrowser.open(url)
            except Exception:
                pass

        threading.Thread(target=_open_browser, daemon=True).start()

    # Start uvicorn
    try:
        subprocess.run(
            [
                sys.executable, "-m", "uvicorn",
                "app.main:app",
                "--host", "0.0.0.0",
                "--port", str(port),
                "--reload",
            ],
            cwd=BASE_DIR,
        )
    except KeyboardInterrupt:
        print("\n\n[STOPPED] Server shut down gracefully.")


def main():
    parser = argparse.ArgumentParser(
        description="Smart Transit Predictor - Bootstrap & Start"
    )
    parser.add_argument(
        "--port", type=int, default=8000,
        help="Port to run the server on (default: 8000)"
    )
    parser.add_argument(
        "--no-open", action="store_true",
        help="Don't auto-open the browser"
    )
    args = parser.parse_args()

    print_banner()
    check_python_version()
    check_and_install_dependencies()
    check_model()
    start_server(port=args.port, open_browser=not args.no_open)


if __name__ == "__main__":
    main()
