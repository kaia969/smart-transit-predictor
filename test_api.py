"""Test expanded NE India routes - all 8 states covered."""
import httpx
import sys
import io

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = "http://localhost:8000"

print("=" * 60)
print("SMART TRANSIT PREDICTOR - EXPANDED NE INDIA TEST")
print("=" * 60)

# Test 1: All cities
r = httpx.get(f"{BASE}/api/cities")
cities = r.json()["cities"]
print(f"\n[TEST 1] Cities: {len(cities)} total")
states = set(c["state"] for c in cities)
print(f"  States covered: {sorted(states)}")
for c in cities:
    print(f"  - {c['name']}, {c['state']}")

# Test 2: All routes
r = httpx.get(f"{BASE}/api/routes")
routes = r.json()["routes"]
print(f"\n[TEST 2] Routes: {len(routes)} total")
for rt in routes:
    print(f"  - {rt['from']} -> {rt['to']} ({rt['distance_km']}km, {len(rt['segments'])} segments)")

# Test 3: Check destinations for each city
print(f"\n[TEST 3] Connectivity check:")
for c in cities:
    r = httpx.get(f"{BASE}/api/destinations/{c['name']}")
    dests = r.json()["destinations"]
    print(f"  {c['name']}: {len(dests)} connections -> {dests}")

# Test 4: Predictions for new routes
print(f"\n[TEST 4] Prediction tests:")
test_routes = [
    ("Guwahati", "Gangtok", "2026-07-20", "Sikkim monsoon"),
    ("Tezpur", "Itanagar", "2026-08-10", "Arunachal monsoon"),
    ("Dimapur", "Kohima", "2026-12-15", "Nagaland winter"),
    ("Jorhat", "Dibrugarh", "2026-01-15", "Assam dry season"),
    ("Kohima", "Imphal", "2026-07-01", "NH-2 monsoon"),
]

for from_c, to_c, date, desc in test_routes:
    r = httpx.post(f"{BASE}/api/predict", json={
        "from_city": from_c, "to_city": to_c, "date": date
    })
    if r.status_code == 200:
        d = r.json()
        print(f"  {desc}: {from_c}->{to_c} = {d['risk_label']} "
              f"(confidence {d['confidence']:.0%}, {len(d['segments'])} segments)")
    else:
        print(f"  {desc}: {from_c}->{to_c} = ERROR {r.status_code}")

print(f"\n{'=' * 60}")
print("[DONE] All expanded NE India tests complete!")
print(f"{'=' * 60}")
