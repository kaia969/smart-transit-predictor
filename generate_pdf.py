"""Generate a professional PDF report for the Smart Transit Predictor project."""
from fpdf import FPDF
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "Smart_Transit_Predictor_Report.pdf")


class ProjectReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, "Smart Transit Predictor - Project Report", align="C")
            self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(30, 60, 120)
        self.ln(4)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(30, 60, 120)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(50, 80, 140)
        self.ln(2)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.cell(6)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 6, 6, "- " + text)

    def bold_text(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def code_block(self, text):
        self.set_fill_color(240, 240, 245)
        self.set_font("Courier", "", 9)
        self.set_text_color(50, 50, 50)
        x = self.get_x()
        w = self.w - 2 * self.l_margin
        lines = text.split("\n")
        block_h = len(lines) * 5 + 6
        if self.get_y() + block_h > self.h - 25:
            self.add_page()
        y_start = self.get_y()
        self.rect(x, y_start, w, block_h, "F")
        self.ln(3)
        for line in lines:
            self.cell(4)
            self.cell(0, 5, line, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        self.set_font("Helvetica", "", 10)

    def add_table(self, headers, rows, col_widths=None):
        if col_widths is None:
            w = (self.w - 2 * self.l_margin) / len(headers)
            col_widths = [w] * len(headers)

        # Check if table fits on page
        needed_h = (len(rows) + 1) * 8 + 4
        if self.get_y() + needed_h > self.h - 25:
            self.add_page()

        # Header
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(30, 60, 120)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 8, h, border=1, fill=True, align="C")
        self.ln()

        # Rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        fill = False
        for row in rows:
            if self.get_y() + 8 > self.h - 25:
                self.add_page()
                # Re-draw header
                self.set_font("Helvetica", "B", 9)
                self.set_fill_color(30, 60, 120)
                self.set_text_color(255, 255, 255)
                for i, h in enumerate(headers):
                    self.cell(col_widths[i], 8, h, border=1, fill=True, align="C")
                self.ln()
                self.set_font("Helvetica", "", 9)
                self.set_text_color(40, 40, 40)
                fill = False

            if fill:
                self.set_fill_color(245, 245, 250)
            else:
                self.set_fill_color(255, 255, 255)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 8, str(cell), border=1, fill=True, align="C")
            self.ln()
            fill = not fill
        self.ln(4)


def build_report():
    pdf = ProjectReport()
    pdf.alias_nb_pages()

    # ── COVER PAGE ──
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(30, 60, 120)
    pdf.cell(0, 16, "Smart Transit Predictor", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, "Northeast India", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_draw_color(30, 60, 120)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, "AI-Powered Road Safety Prediction System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Machine Learning + Real-Time Weather Data", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.cell(0, 8, "Covering All 8 States | 13 Cities | 18 Routes", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Technologies: FastAPI | XGBoost | Leaflet.js | Open-Meteo API", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Language: Python 3.10+ | HTML/CSS/JavaScript", align="C", new_x="LMARGIN", new_y="NEXT")

    # ── TABLE OF CONTENTS ──
    pdf.add_page()
    pdf.section_title("Table of Contents")
    toc = [
        "1. Problem Statement",
        "2. Features & User Experience",
        "3. Coverage - All 8 NE States",
        "4. How It Works (Architecture)",
        "5. Technology Stack",
        "6. Project Structure",
        "7. ML Model Performance",
        "8. API Documentation",
        "9. Setup & Installation",
        "10. Why This Project Stands Out",
        "11. Future Improvements",
    ]
    for item in toc:
        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 9, item, new_x="LMARGIN", new_y="NEXT")

    # ── 1. PROBLEM STATEMENT ──
    pdf.add_page()
    pdf.section_title("1. Problem Statement")
    pdf.body_text(
        "Northeast India - Mizoram, Manipur, Assam, Meghalaya, Nagaland, "
        "Arunachal Pradesh, Tripura, and Sikkim - has some of the most "
        "difficult and dangerous roads in India. Every year:"
    )
    pdf.bullet("Landslides block highways for days during the monsoon season")
    pdf.bullet("Heavy rainfall makes roads dangerous and unpredictable")
    pdf.bullet("Travelers have no way to know if a route is safe before they leave")
    pdf.ln(4)
    pdf.bold_text("The Scenario:")
    pdf.body_text(
        "Imagine you are traveling from Aizawl to Silchar and halfway through "
        "the journey, a landslide blocks the road. No one warned you! You are "
        "stranded on a remote mountain road with no cell service and no help."
    )
    pdf.bold_text("Our Solution:")
    pdf.body_text(
        "This app solves this problem. You enter your route and travel date, "
        "and the app tells you the risk level of that road based on real-time "
        "weather data and terrain analysis using Machine Learning."
    )

    # ── 2. FEATURES ──
    pdf.add_page()
    pdf.section_title("2. Features & User Experience")
    pdf.sub_title("What the User Sees")
    pdf.body_text("A stunning dark-themed website where you:")
    pdf.bullet("Select a starting city (e.g., Aizawl)")
    pdf.bullet("Select a destination city (e.g., Guwahati)")
    pdf.bullet("Select a travel date")
    pdf.bullet('Click "Check Route Safety"')
    pdf.ln(4)
    pdf.bold_text("Results Include:")
    pdf.bullet("Risk Score - Safe (green), Caution (yellow), or Danger (red)")
    pdf.bullet("Interactive Map - route with color-coded risk segments")
    pdf.bullet('Risk Reasons - e.g., "Heavy rainfall expected + steep terrain"')
    pdf.bullet("Weather Data - rainfall, temperature, wind speed, humidity")
    pdf.bullet("Segment Breakdown - risk level for each section of the route")
    pdf.bullet("Confidence Score - ML model's prediction confidence percentage")
    pdf.ln(4)
    pdf.sub_title("Design Features")
    pdf.bullet("Premium dark theme with glassmorphism effects")
    pdf.bullet("Smooth animations and micro-interactions")
    pdf.bullet("Responsive layout for all screen sizes")
    pdf.bullet("Interactive Leaflet.js map with OpenStreetMap tiles")
    pdf.bullet("Real-time weather data from Open-Meteo API")

    # ── 3. COVERAGE ──
    pdf.add_page()
    pdf.section_title("3. Coverage - All 8 Northeast States")
    pdf.sub_title("13 Cities")
    pdf.add_table(
        ["State", "City", "Elevation"],
        [
            ["Arunachal Pradesh", "Itanagar", "440m"],
            ["Assam", "Guwahati", "55m"],
            ["Assam", "Silchar", "35m"],
            ["Assam", "Tezpur", "48m"],
            ["Assam", "Jorhat", "116m"],
            ["Assam", "Dibrugarh", "108m"],
            ["Manipur", "Imphal", "786m"],
            ["Meghalaya", "Shillong", "1496m"],
            ["Mizoram", "Aizawl", "1132m"],
            ["Nagaland", "Kohima", "1444m"],
            ["Nagaland", "Dimapur", "260m"],
            ["Sikkim", "Gangtok", "1650m"],
            ["Tripura", "Agartala", "16m"],
        ],
        [63, 63, 63],
    )

    pdf.sub_title("18 Routes (53 Segments)")
    pdf.add_table(
        ["Route", "Distance", "Key Risk"],
        [
            ["Aizawl - Silchar", "180 km", "Heavy rainfall, steep"],
            ["Aizawl - Guwahati", "480 km", "Landslide prone"],
            ["Imphal - Guwahati", "450 km", "NH-2 landslide zones"],
            ["Shillong - Guwahati", "100 km", "Fog, steep curves"],
            ["Agartala - Silchar", "170 km", "Flooding prone"],
            ["Imphal - Silchar", "200 km", "Mountain roads"],
            ["Dimapur - Kohima", "74 km", "Extremely steep"],
            ["Kohima - Imphal", "135 km", "Most dangerous NH-2"],
            ["Guwahati - Tezpur", "180 km", "Brahmaputra floods"],
            ["Guwahati - Jorhat", "310 km", "Kaziranga zone"],
            ["Jorhat - Dibrugarh", "130 km", "River flooding"],
            ["Tezpur - Itanagar", "280 km", "Mountain, landslide"],
            ["Dibrugarh - Itanagar", "480 km", "Remote mountains"],
            ["Guwahati - Gangtok", "560 km", "Mountain passes"],
            ["Silchar - Shillong", "330 km", "Jaintia Hills"],
            ["Agartala - Guwahati", "590 km", "Very long route"],
            ["Jorhat - Kohima", "190 km", "Mountain ascent"],
            ["Dimapur - Jorhat", "150 km", "Naga Hills"],
        ],
        [63, 35, 91],
    )

    # ── 4. HOW IT WORKS ──
    pdf.add_page()
    pdf.section_title("4. How It Works (Architecture)")

    pdf.sub_title("Step 1: Weather Data (Open-Meteo API)")
    pdf.body_text(
        "We fetch real-time weather data for each route segment's midpoint "
        "coordinates. This includes rainfall (last 24h + forecast), temperature, "
        "wind speed, and humidity. The Open-Meteo API is completely free and "
        "requires no API key."
    )

    pdf.sub_title("Step 2: Terrain Data")
    pdf.body_text(
        "We store terrain information for each of the 53 route segments, including "
        "slope angle, maximum elevation, road type (highway vs mountain road), "
        "and historical blockage frequency."
    )

    pdf.sub_title("Step 3: Machine Learning (XGBoost)")
    pdf.body_text(
        "An XGBoost classifier trained on 6,000+ synthetic samples predicts "
        "risk using 9 input features. The model outputs one of three classes: "
        "Safe (0), Caution (1), or Danger (2), along with confidence probabilities."
    )
    pdf.ln(2)
    pdf.bold_text("Input Features:")
    pdf.add_table(
        ["Feature", "Description", "Range"],
        [
            ["rainfall_24h", "Rainfall in last 24 hours", "0-120 mm"],
            ["rainfall_forecast_24h", "Expected rainfall next 24h", "0-100 mm"],
            ["temperature", "Temperature", "5-35 C"],
            ["wind_speed", "Wind speed", "0-60 km/h"],
            ["humidity", "Humidity percentage", "40-100%"],
            ["slope", "Terrain slope angle", "5-45 degrees"],
            ["road_type", "Highway(0) / Mountain(1)", "0 or 1"],
            ["month", "Month of travel", "1-12"],
            ["historical_blockages", "Blockages per year", "0-20"],
        ],
        [55, 75, 60],
    )

    pdf.sub_title("Step 4: Map Visualization (Leaflet.js)")
    pdf.body_text(
        "An interactive map renders the selected route with color-coded polylines: "
        "green for Safe, yellow for Caution, and red/dashed for Danger. City "
        "markers with permanent tooltips are displayed. Users can click on "
        "segments to see risk details."
    )

    pdf.sub_title("Step 5: Web Application (FastAPI)")
    pdf.body_text(
        "The FastAPI backend receives the route and date, fetches weather data "
        "for all segments in parallel using async/await, runs the ML prediction "
        "for each segment, and returns a comprehensive JSON response with risk "
        "scores, reasons, weather data, and route information."
    )

    # Architecture diagram as text
    pdf.ln(2)
    pdf.bold_text("System Architecture:")
    pdf.code_block(
        "Frontend (HTML/JS/Leaflet.js)\n"
        "       |\n"
        "       v\n"
        "FastAPI Backend (app/main.py)\n"
        "    |              |\n"
        "    v              v\n"
        "Open-Meteo     XGBoost Model\n"
        "Weather API    (models/xgboost_model.pkl)\n"
        "    |              |\n"
        "    v              v\n"
        " Weather +    Risk Prediction\n"
        "  Terrain  -->  + Reasons"
    )

    # ── 5. TECH STACK ──
    pdf.add_page()
    pdf.section_title("5. Technology Stack")
    pdf.add_table(
        ["Technology", "Purpose", "Why Chosen"],
        [
            ["FastAPI", "Backend framework", "Async, fast, auto docs"],
            ["XGBoost", "ML prediction", "Best for tabular data"],
            ["Open-Meteo", "Weather data", "Free, no API key"],
            ["Leaflet.js", "Interactive maps", "Lightweight, powerful"],
            ["scikit-learn", "ML utilities", "Metrics, train/test"],
            ["httpx", "HTTP client", "Async support"],
            ["pandas", "Data processing", "CSV handling"],
            ["HTML/CSS/JS", "Frontend", "Premium dark theme"],
        ],
        [40, 48, 101],
    )

    # ── 6. PROJECT STRUCTURE ──
    pdf.section_title("6. Project Structure")
    pdf.code_block(
        "smart-transit-predictor/\n"
        "|-- app/\n"
        "|   |-- __init__.py          (Package init)\n"
        "|   |-- main.py              (FastAPI - 5 endpoints)\n"
        "|   |-- model.py             (XGBoost model wrapper)\n"
        "|   |-- routes.py            (13 cities, 18 routes)\n"
        "|   |-- weather.py           (Open-Meteo async client)\n"
        "|-- data/\n"
        "|   |-- terrain.csv          (Terrain data)\n"
        "|   |-- incidents.csv        (50 historical incidents)\n"
        "|   |-- training_data.csv    (6000 training samples)\n"
        "|-- frontend/\n"
        "|   |-- index.html           (Premium dark-themed SPA)\n"
        "|   |-- style.css            (Glassmorphism, 1100+ lines)\n"
        "|   |-- script.js            (Map + API, 490+ lines)\n"
        "|-- models/\n"
        "|   |-- xgboost_model.pkl    (Trained XGBoost)\n"
        "|-- train_model.py           (Training script)\n"
        "|-- test_api.py              (API test script)\n"
        "|-- requirements.txt         (Dependencies)\n"
        "|-- README.md                (Documentation)"
    )

    # ── 7. ML MODEL ──
    pdf.add_page()
    pdf.section_title("7. ML Model Performance")
    pdf.bold_text("Overall Accuracy: 91.4%")
    pdf.ln(2)
    pdf.sub_title("Classification Report")
    pdf.add_table(
        ["Class", "Precision", "Recall", "F1-Score", "Support"],
        [
            ["Safe", "0.95", "0.93", "0.94", "395"],
            ["Caution", "0.89", "0.89", "0.89", "455"],
            ["Danger", "0.91", "0.93", "0.92", "350"],
        ],
        [38, 38, 38, 38, 38],
    )

    pdf.sub_title("Feature Importance")
    pdf.add_table(
        ["Feature", "Importance", "Percentage"],
        [
            ["rainfall_24h", "0.3454", "34.5%"],
            ["road_type", "0.1538", "15.4%"],
            ["slope", "0.1244", "12.4%"],
            ["historical_blockages", "0.1090", "10.9%"],
            ["rainfall_forecast_24h", "0.0886", "8.9%"],
            ["humidity", "0.0626", "6.3%"],
            ["month", "0.0512", "5.1%"],
            ["wind_speed", "0.0391", "3.9%"],
            ["temperature", "0.0259", "2.6%"],
        ],
        [63, 63, 63],
    )

    pdf.sub_title("Training Details")
    pdf.bullet("Training samples: 6,000 (synthetically generated)")
    pdf.bullet("Train/test split: 80/20 (4800 train / 1200 test)")
    pdf.bullet("Algorithm: XGBoost (n_estimators=200, max_depth=6)")
    pdf.bullet("Objective: multi:softprob (3-class classification)")
    pdf.bullet("Class distribution: Safe 32.9%, Caution 37.9%, Danger 29.2%")

    # ── 8. API DOCS ──
    pdf.add_page()
    pdf.section_title("8. API Documentation")
    pdf.add_table(
        ["Method", "Endpoint", "Description"],
        [
            ["GET", "/", "Serves the frontend"],
            ["GET", "/api/cities", "All 13 cities with coordinates"],
            ["GET", "/api/routes", "All 18 routes with segments"],
            ["GET", "/api/destinations/{city}", "Reachable cities"],
            ["POST", "/api/predict", "Predict risk for route + date"],
        ],
        [25, 65, 99],
    )

    pdf.sub_title("Predict Request (POST /api/predict)")
    pdf.code_block(
        '{\n'
        '  "from_city": "Aizawl",\n'
        '  "to_city": "Silchar",\n'
        '  "date": "2026-07-15"\n'
        '}'
    )

    pdf.sub_title("Predict Response")
    pdf.code_block(
        '{\n'
        '  "risk_level": 2,\n'
        '  "risk_label": "Danger",\n'
        '  "confidence": 0.987,\n'
        '  "reasons": [\n'
        '    "Heavy rainfall (45.2mm in 24h)",\n'
        '    "Very steep terrain (32 deg slope)",\n'
        '    "Peak monsoon season (July)"\n'
        '  ],\n'
        '  "segments": [...],\n'
        '  "weather": {\n'
        '    "rainfall_24h": 45.2,\n'
        '    "temperature": 22.5,\n'
        '    "wind_speed": 35.0,\n'
        '    "humidity": 92.0\n'
        '  }\n'
        '}'
    )

    # ── 9. SETUP ──
    pdf.add_page()
    pdf.section_title("9. Setup & Installation")
    pdf.sub_title("Prerequisites")
    pdf.bullet("Python 3.10 or higher")
    pdf.bullet("pip (Python package manager)")
    pdf.bullet("Internet connection (for weather API)")
    pdf.ln(4)
    pdf.sub_title("Installation Steps")
    pdf.bold_text("Step 1: Navigate to the project")
    pdf.code_block("cd smart-transit-predictor")
    pdf.bold_text("Step 2: Install dependencies")
    pdf.code_block("pip install -r requirements.txt")
    pdf.bold_text("Step 3: Train the ML model (one-time, ~5 seconds)")
    pdf.code_block("python train_model.py")
    pdf.bold_text("Step 4: Start the web server")
    pdf.code_block("python -m uvicorn app.main:app --reload --port 8000")
    pdf.bold_text("Step 5: Open in browser")
    pdf.code_block("http://localhost:8000")

    # ── 10. WHY STANDS OUT ──
    pdf.add_page()
    pdf.section_title("10. Why This Project Stands Out")
    pdf.add_table(
        ["Typical Student Project", "This Project"],
        [
            ["Movie recommender", "Solves a REAL problem"],
            ["Uses toy datasets", "Uses real weather API data"],
            ["Simple model only", "Full ML pipeline"],
            ["No visualization", "Interactive map"],
            ["Basic UI", "Premium glassmorphism dark theme"],
            ["Single file", "12+ files, proper structure"],
            ["No API", "Full REST API with FastAPI"],
            ["Not deployment ready", "Production-ready code"],
        ],
        [95, 95],
    )

    # ── 11. FUTURE ──
    pdf.section_title("11. Future Improvements")
    pdf.bullet("Add more cities and routes across NE India")
    pdf.bullet("Integrate real historical blockage data from NHAI/BRO")
    pdf.bullet("User accounts and trip history tracking")
    pdf.bullet("Push notifications for route alerts")
    pdf.bullet("Mobile responsive Progressive Web App (PWA)")
    pdf.bullet("Multi-language support (Hindi, Mizo, Manipuri)")
    pdf.bullet("Integration with Google Maps API for real-time traffic")
    pdf.bullet("Deploy on Render / Railway / AWS for public access")
    pdf.bullet("Add more ML features: soil moisture, seismic activity")
    pdf.bullet("Crowdsourced road condition reports from travelers")

    # ── SAVE ──
    pdf.output(OUTPUT_PATH)
    print(f"PDF saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_report()
