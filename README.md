<<<<<<< HEAD
<<<<<<< HEAD
# 🛡️ Smart Transit Predictor — Northeast India

> **AI-Powered Road Safety Prediction System for Northeast India**
> 
> Uses Machine Learning (XGBoost) + Real-Time Weather Data to predict road risk levels across all 8 states of Northeast India.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green?logo=fastapi)
![XGBoost](https://img.shields.io/badge/XGBoost-2.1+-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🤔 The Problem

Northeast India — Mizoram, Manipur, Assam, Meghalaya, Nagaland, Arunachal Pradesh, Tripura, and Sikkim — has some of the most dangerous roads in India. Every year:

- 🏔️ **Landslides** block highways for days
- 🌧️ **Heavy rainfall** makes roads dangerous
- ❌ **Travelers have no way to know** if a route is safe before they leave

**Imagine:** You're traveling from Aizawl to Silchar and halfway through, a landslide blocks the road. No one warned you!

**Our app solves this** — you enter your route and date, and the app tells you the risk level based on weather and terrain data.

---

## 👀 What the User Sees

A stunning dark-themed website where you:

1. ✅ Select a **starting city** (e.g., Aizawl)
2. ✅ Select a **destination city** (e.g., Guwahati)
3. ✅ Select a **travel date**
4. ✅ Click **"Check Route Safety"**
5. ✅ Get:
   - A **risk score** (🟢 Safe / 🟡 Caution / 🔴 Danger)
   - An **interactive map** showing the route with color-coded risk
   - **Reasons** for the risk (e.g., "Heavy rainfall expected + steep terrain")
   - **Weather data** (rainfall, temperature, wind, humidity)
   - **Segment breakdown** showing risk for each section of the route

---

## 🗺️ Coverage — All 8 NE States

### 13 Cities

| State | City | Elevation |
|-------|------|-----------|
| Arunachal Pradesh | Itanagar | 440m |
| Assam | Guwahati, Silchar, Tezpur, Jorhat, Dibrugarh | 35-116m |
| Manipur | Imphal | 786m |
| Meghalaya | Shillong | 1496m |
| Mizoram | Aizawl | 1132m |
| Nagaland | Kohima, Dimapur | 260-1444m |
| Sikkim | Gangtok | 1650m |
| Tripura | Agartala | 16m |

### 18 Routes, 53 Segments

| Route | Distance | Risk Factors |
|-------|----------|-------------|
| Aizawl → Silchar | 180 km | Heavy rainfall, steep terrain |
| Aizawl → Guwahati | 480 km | Landslide prone, long route |
| Imphal → Guwahati | 450 km | NH-2 landslide zones, very steep |
| Shillong → Guwahati | 100 km | Fog, steep curves |
| Agartala → Silchar | 170 km | Flooding prone, river crossings |
| Imphal → Silchar | 200 km | Mountain roads, heavy rainfall |
| Dimapur → Kohima | 74 km | Extremely steep ascent |
| Kohima → Imphal | 135 km | NH-2 most dangerous stretch |
| Guwahati → Tezpur | 180 km | Brahmaputra flood plain |
| Guwahati → Jorhat | 310 km | Flood-prone, Kaziranga zone |
| Jorhat → Dibrugarh | 130 km | River flooding, seasonal fog |
| Tezpur → Itanagar | 280 km | Mountain roads, landslide zones |
| Dibrugarh → Itanagar | 480 km | Remote mountains, limited rescue |
| Guwahati → Gangtok | 560 km | Mountain passes, Teesta valley |
| Silchar → Shillong | 330 km | Jaintia Hills, heavy rainfall |
| Agartala → Guwahati | 590 km | Very long, multiple states |
| Jorhat → Kohima | 190 km | Mountain ascent, narrow roads |
| Dimapur → Jorhat | 150 km | Naga Hills foothills |

---

## 🧠 How It Works

### Step 1 — Weather Data (Open-Meteo API)
We fetch **real-time weather** data for each route segment:
- Rainfall (last 24h + forecast)
- Temperature
- Wind speed
- Humidity

Uses [Open-Meteo API](https://open-meteo.com/) — **completely free, no API key needed**.

### Step 2 — Terrain Data
We store terrain info for each route segment:
- **Slope/elevation** — steeper = riskier
- **Road type** — highway (0) vs mountain road (1)
- **Historical blockages** — how often this route was blocked before

### Step 3 — Machine Learning (XGBoost)
An **XGBoost classifier** trained on 6,000+ samples predicts risk:

**Input Features (9 total):**
| Feature | Description |
|---------|-------------|
| `rainfall_24h` | Rainfall in last 24 hours (mm) |
| `rainfall_forecast_24h` | Expected rainfall next 24h (mm) |
| `temperature` | Temperature (°C) |
| `wind_speed` | Wind speed (km/h) |
| `humidity` | Humidity (%) |
| `slope` | Terrain slope (degrees) |
| `road_type` | 0 = highway, 1 = mountain |
| `month` | Month (monsoon = riskier) |
| `historical_blockages` | Blockages per year |

**Output:**
| Level | Label | Meaning |
|-------|-------|---------|
| 0 | 🟢 Safe | Good to travel |
| 1 | 🟡 Caution | Travel with care |
| 2 | 🔴 Danger | Avoid if possible |

### Step 4 — Map Visualization (Leaflet.js)
Interactive map with:
- Color-coded route polylines (green/yellow/red)
- City markers with tooltips
- Click on segments for risk details
- Auto-zoom to fit the selected route

### Step 5 — Web Application (FastAPI)
FastAPI backend that:
- Receives route + date request
- Fetches weather data in parallel (async)
- Runs ML prediction per segment
- Returns risk score + reasons + map data

---

## 🏗️ Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │────▶│   FastAPI    │────▶│  Open-Meteo  │
│  (HTML/JS)   │◀────│   Backend    │◀────│  Weather API │
│  Leaflet.js  │     │              │     └──────────────┘
└──────────────┘     │   app/       │
                     │   main.py    │     ┌──────────────┐
                     │   weather.py │────▶│   XGBoost    │
                     │   routes.py  │◀────│   ML Model   │
                     │   model.py   │     └──────────────┘
                     └──────────────┘
```

---

## 📁 Project Structure

```
smart-transit-predictor/
├── app/
│   ├── __init__.py           # Package init
│   ├── main.py               # FastAPI backend (5 API endpoints)
│   ├── model.py              # XGBoost model wrapper + rule-based fallback
│   ├── routes.py             # 13 cities, 18 routes, 53 segments
│   └── weather.py            # Open-Meteo async weather client
├── data/
│   ├── terrain.csv           # Terrain data (slope, elevation, road type)
│   ├── incidents.csv         # 50 historical road blockage incidents
│   └── training_data.csv     # 6000 synthetic training samples (auto-generated)
├── frontend/
│   ├── index.html            # Premium dark-themed single-page app
│   ├── style.css             # Glassmorphism + animations (1100+ lines)
│   └── script.js             # Leaflet.js map + API integration (490+ lines)
├── models/
│   └── xgboost_model.pkl     # Trained XGBoost classifier
├── train_model.py            # Model training script
├── test_api.py               # API test script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone or navigate to the project
cd smart-transit-predictor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the ML model (one-time, ~5 seconds)
python train_model.py

# 4. Start the server
python -m uvicorn app.main:app --reload --port 8000

# 5. Open in browser
# http://localhost:8000
```

### Quick Test
```bash
python test_api.py
```

---

## 🛠️ Technologies Used

| Technology | Purpose | Why |
|-----------|---------|-----|
| **FastAPI** | Backend web framework | Faster than Flask, async support, auto API docs |
| **XGBoost** | ML prediction model | Best algorithm for tabular classification |
| **Open-Meteo API** | Weather data | Free, no API key, covers all of NE India |
| **Leaflet.js** | Interactive maps | Lightweight, powerful, great tile support |
| **Pydantic** | Data validation | Auto request/response validation |
| **httpx** | HTTP client | Async support for parallel weather fetching |
| **scikit-learn** | ML utilities | Train/test split, metrics, reporting |
| **pandas** | Data processing | Cleans and organizes training data |
| **HTML/CSS/JS** | Frontend | Premium glassmorphism dark theme |

---

## 📊 ML Model Performance

```
Accuracy: 91.4%

              precision    recall  f1-score   support
        Safe       0.95      0.93      0.94       395
     Caution       0.89      0.89      0.89       455
      Danger       0.91      0.93      0.92       350

Feature Importance:
  rainfall_24h              34.5%  ██████████████████
  road_type                 15.4%  ████████
  slope                     12.4%  ██████
  historical_blockages      10.9%  █████
  rainfall_forecast_24h      8.9%  ████
  humidity                   6.3%  ███
  month                      5.1%  ██
  wind_speed                 3.9%  █
  temperature                2.6%  █
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the frontend |
| `GET` | `/api/cities` | Returns all 13 cities with coordinates |
| `GET` | `/api/routes` | Returns all 18 routes with segments |
| `GET` | `/api/destinations/{city}` | Returns reachable cities from a given city |
| `POST` | `/api/predict` | Predicts risk for a route + date |

### Predict Request
```json
{
  "from_city": "Aizawl",
  "to_city": "Silchar",
  "date": "2026-07-15"
}
```

### Predict Response
```json
{
  "risk_level": 2,
  "risk_label": "Danger",
  "confidence": 0.987,
  "reasons": [
    "🌧️ Heavy rainfall recorded (45.2mm in 24h)",
    "⛰️ Very steep terrain (32° slope)",
    "🛤️ Mountain road — narrower and more vulnerable",
    "📅 Peak monsoon season (July)"
  ],
  "segments": [...],
  "weather": {
    "rainfall_24h": 45.2,
    "temperature": 22.5,
    "wind_speed": 35.0,
    "humidity": 92.0
  },
  "route_info": {
    "from": "Aizawl",
    "to": "Silchar",
    "distance_km": 180,
    "estimated_time": "6-7 hours"
  }
}
```

---

## 🎯 Why This Project Stands Out

| Typical Student Project | This Project |
|------------------------|-------------|
| Movie recommender / Iris classifier | Solves a real problem for NE India |
| Uses toy datasets | Uses real weather data from APIs |
| Simple model only | Full ML pipeline + feature engineering |
| No visualization | Interactive map with risk visualization |
| Basic UI | Premium dark theme with glassmorphism |
| Single file | Proper project structure with 12+ files |
| No API | Full REST API with FastAPI |
| No deployment ready | Production-ready code |

---

## 📈 Future Improvements

- [ ] Add more cities and routes
- [ ] Real historical blockage data from NHAI/BRO
- [ ] User accounts + trip history
- [ ] Push notifications for route alerts
- [ ] Mobile responsive PWA
- [ ] Multi-language support (Hindi, Mizo, Manipuri)
- [ ] Integration with Google Maps API for real-time traffic
- [ ] Deploy on Render / Railway / AWS

---

## 👨‍💻 Author

Built with ❤️ for the people of Northeast India.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
=======
# Smart_Transit_Predictor
it helps to check road safety
>>>>>>> cfaf0cd2f678e6deeeda50890d41c35d56227ca2
=======
<<<<<<< HEAD
# 🛡️ Smart Transit Predictor — Northeast India

> **AI-Powered Road Safety Prediction System for Northeast India**
> 
> Uses Machine Learning (XGBoost) + Real-Time Weather Data to predict road risk levels across all 8 states of Northeast India.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green?logo=fastapi)
![XGBoost](https://img.shields.io/badge/XGBoost-2.1+-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🤔 The Problem

Northeast India — Mizoram, Manipur, Assam, Meghalaya, Nagaland, Arunachal Pradesh, Tripura, and Sikkim — has some of the most dangerous roads in India. Every year:

- 🏔️ **Landslides** block highways for days
- 🌧️ **Heavy rainfall** makes roads dangerous
- ❌ **Travelers have no way to know** if a route is safe before they leave

**Imagine:** You're traveling from Aizawl to Silchar and halfway through, a landslide blocks the road. No one warned you!

**Our app solves this** — you enter your route and date, and the app tells you the risk level based on weather and terrain data.

---

## 👀 What the User Sees

A stunning dark-themed website where you:

1. ✅ Select a **starting city** (e.g., Aizawl)
2. ✅ Select a **destination city** (e.g., Guwahati)
3. ✅ Select a **travel date**
4. ✅ Click **"Check Route Safety"**
5. ✅ Get:
   - A **risk score** (🟢 Safe / 🟡 Caution / 🔴 Danger)
   - An **interactive map** showing the route with color-coded risk
   - **Reasons** for the risk (e.g., "Heavy rainfall expected + steep terrain")
   - **Weather data** (rainfall, temperature, wind, humidity)
   - **Segment breakdown** showing risk for each section of the route

---

## 🗺️ Coverage — All 8 NE States

### 13 Cities

| State | City | Elevation |
|-------|------|-----------|
| Arunachal Pradesh | Itanagar | 440m |
| Assam | Guwahati, Silchar, Tezpur, Jorhat, Dibrugarh | 35-116m |
| Manipur | Imphal | 786m |
| Meghalaya | Shillong | 1496m |
| Mizoram | Aizawl | 1132m |
| Nagaland | Kohima, Dimapur | 260-1444m |
| Sikkim | Gangtok | 1650m |
| Tripura | Agartala | 16m |

### 18 Routes, 53 Segments

| Route | Distance | Risk Factors |
|-------|----------|-------------|
| Aizawl → Silchar | 180 km | Heavy rainfall, steep terrain |
| Aizawl → Guwahati | 480 km | Landslide prone, long route |
| Imphal → Guwahati | 450 km | NH-2 landslide zones, very steep |
| Shillong → Guwahati | 100 km | Fog, steep curves |
| Agartala → Silchar | 170 km | Flooding prone, river crossings |
| Imphal → Silchar | 200 km | Mountain roads, heavy rainfall |
| Dimapur → Kohima | 74 km | Extremely steep ascent |
| Kohima → Imphal | 135 km | NH-2 most dangerous stretch |
| Guwahati → Tezpur | 180 km | Brahmaputra flood plain |
| Guwahati → Jorhat | 310 km | Flood-prone, Kaziranga zone |
| Jorhat → Dibrugarh | 130 km | River flooding, seasonal fog |
| Tezpur → Itanagar | 280 km | Mountain roads, landslide zones |
| Dibrugarh → Itanagar | 480 km | Remote mountains, limited rescue |
| Guwahati → Gangtok | 560 km | Mountain passes, Teesta valley |
| Silchar → Shillong | 330 km | Jaintia Hills, heavy rainfall |
| Agartala → Guwahati | 590 km | Very long, multiple states |
| Jorhat → Kohima | 190 km | Mountain ascent, narrow roads |
| Dimapur → Jorhat | 150 km | Naga Hills foothills |

---

## 🧠 How It Works

### Step 1 — Weather Data (Open-Meteo API)
We fetch **real-time weather** data for each route segment:
- Rainfall (last 24h + forecast)
- Temperature
- Wind speed
- Humidity

Uses [Open-Meteo API](https://open-meteo.com/) — **completely free, no API key needed**.

### Step 2 — Terrain Data
We store terrain info for each route segment:
- **Slope/elevation** — steeper = riskier
- **Road type** — highway (0) vs mountain road (1)
- **Historical blockages** — how often this route was blocked before

### Step 3 — Machine Learning (XGBoost)
An **XGBoost classifier** trained on 6,000+ samples predicts risk:

**Input Features (9 total):**
| Feature | Description |
|---------|-------------|
| `rainfall_24h` | Rainfall in last 24 hours (mm) |
| `rainfall_forecast_24h` | Expected rainfall next 24h (mm) |
| `temperature` | Temperature (°C) |
| `wind_speed` | Wind speed (km/h) |
| `humidity` | Humidity (%) |
| `slope` | Terrain slope (degrees) |
| `road_type` | 0 = highway, 1 = mountain |
| `month` | Month (monsoon = riskier) |
| `historical_blockages` | Blockages per year |

**Output:**
| Level | Label | Meaning |
|-------|-------|---------|
| 0 | 🟢 Safe | Good to travel |
| 1 | 🟡 Caution | Travel with care |
| 2 | 🔴 Danger | Avoid if possible |

### Step 4 — Map Visualization (Leaflet.js)
Interactive map with:
- Color-coded route polylines (green/yellow/red)
- City markers with tooltips
- Click on segments for risk details
- Auto-zoom to fit the selected route

### Step 5 — Web Application (FastAPI)
FastAPI backend that:
- Receives route + date request
- Fetches weather data in parallel (async)
- Runs ML prediction per segment
- Returns risk score + reasons + map data

---

## 🏗️ Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │────▶│   FastAPI    │────▶│  Open-Meteo  │
│  (HTML/JS)   │◀────│   Backend    │◀────│  Weather API │
│  Leaflet.js  │     │              │     └──────────────┘
└──────────────┘     │   app/       │
                     │   main.py    │     ┌──────────────┐
                     │   weather.py │────▶│   XGBoost    │
                     │   routes.py  │◀────│   ML Model   │
                     │   model.py   │     └──────────────┘
                     └──────────────┘
```

---

## 📁 Project Structure

```
smart-transit-predictor/
├── app/
│   ├── __init__.py           # Package init
│   ├── main.py               # FastAPI backend (5 API endpoints)
│   ├── model.py              # XGBoost model wrapper + rule-based fallback
│   ├── routes.py             # 13 cities, 18 routes, 53 segments
│   └── weather.py            # Open-Meteo async weather client
├── data/
│   ├── terrain.csv           # Terrain data (slope, elevation, road type)
│   ├── incidents.csv         # 50 historical road blockage incidents
│   └── training_data.csv     # 6000 synthetic training samples (auto-generated)
├── frontend/
│   ├── index.html            # Premium dark-themed single-page app
│   ├── style.css             # Glassmorphism + animations (1100+ lines)
│   └── script.js             # Leaflet.js map + API integration (490+ lines)
├── models/
│   └── xgboost_model.pkl     # Trained XGBoost classifier
├── train_model.py            # Model training script
├── test_api.py               # API test script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone or navigate to the project
cd smart-transit-predictor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the ML model (one-time, ~5 seconds)
python train_model.py

# 4. Start the server
python -m uvicorn app.main:app --reload --port 8000

# 5. Open in browser
# http://localhost:8000
```

### Quick Test
```bash
python test_api.py
```

---

## 🛠️ Technologies Used

| Technology | Purpose | Why |
|-----------|---------|-----|
| **FastAPI** | Backend web framework | Faster than Flask, async support, auto API docs |
| **XGBoost** | ML prediction model | Best algorithm for tabular classification |
| **Open-Meteo API** | Weather data | Free, no API key, covers all of NE India |
| **Leaflet.js** | Interactive maps | Lightweight, powerful, great tile support |
| **Pydantic** | Data validation | Auto request/response validation |
| **httpx** | HTTP client | Async support for parallel weather fetching |
| **scikit-learn** | ML utilities | Train/test split, metrics, reporting |
| **pandas** | Data processing | Cleans and organizes training data |
| **HTML/CSS/JS** | Frontend | Premium glassmorphism dark theme |

---

## 📊 ML Model Performance

```
Accuracy: 91.4%

              precision    recall  f1-score   support
        Safe       0.95      0.93      0.94       395
     Caution       0.89      0.89      0.89       455
      Danger       0.91      0.93      0.92       350

Feature Importance:
  rainfall_24h              34.5%  ██████████████████
  road_type                 15.4%  ████████
  slope                     12.4%  ██████
  historical_blockages      10.9%  █████
  rainfall_forecast_24h      8.9%  ████
  humidity                   6.3%  ███
  month                      5.1%  ██
  wind_speed                 3.9%  █
  temperature                2.6%  █
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the frontend |
| `GET` | `/api/cities` | Returns all 13 cities with coordinates |
| `GET` | `/api/routes` | Returns all 18 routes with segments |
| `GET` | `/api/destinations/{city}` | Returns reachable cities from a given city |
| `POST` | `/api/predict` | Predicts risk for a route + date |

### Predict Request
```json
{
  "from_city": "Aizawl",
  "to_city": "Silchar",
  "date": "2026-07-15"
}
```

### Predict Response
```json
{
  "risk_level": 2,
  "risk_label": "Danger",
  "confidence": 0.987,
  "reasons": [
    "🌧️ Heavy rainfall recorded (45.2mm in 24h)",
    "⛰️ Very steep terrain (32° slope)",
    "🛤️ Mountain road — narrower and more vulnerable",
    "📅 Peak monsoon season (July)"
  ],
  "segments": [...],
  "weather": {
    "rainfall_24h": 45.2,
    "temperature": 22.5,
    "wind_speed": 35.0,
    "humidity": 92.0
  },
  "route_info": {
    "from": "Aizawl",
    "to": "Silchar",
    "distance_km": 180,
    "estimated_time": "6-7 hours"
  }
}
```

---

## 🎯 Why This Project Stands Out

| Typical Student Project | This Project |
|------------------------|-------------|
| Movie recommender / Iris classifier | Solves a real problem for NE India |
| Uses toy datasets | Uses real weather data from APIs |
| Simple model only | Full ML pipeline + feature engineering |
| No visualization | Interactive map with risk visualization |
| Basic UI | Premium dark theme with glassmorphism |
| Single file | Proper project structure with 12+ files |
| No API | Full REST API with FastAPI |
| No deployment ready | Production-ready code |

---

## 📈 Future Improvements

- [ ] Add more cities and routes
- [ ] Real historical blockage data from NHAI/BRO
- [ ] User accounts + trip history
- [ ] Push notifications for route alerts
- [ ] Mobile responsive PWA
- [ ] Multi-language support (Hindi, Mizo, Manipuri)
- [ ] Integration with Google Maps API for real-time traffic
- [ ] Deploy on Render / Railway / AWS

---

## 👨‍💻 Author

Built with ❤️ for the people of Northeast India.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
=======
# Smart_Transit_Predictor
it helps to check road safety
>>>>>>> cfaf0cd2f678e6deeeda50890d41c35d56227ca2
>>>>>>> f746594448f505398c8161e288483a2b917433de
#   s m a r t - t r a n s i t - p r e d i c t o r  
 