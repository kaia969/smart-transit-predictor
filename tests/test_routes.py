from app.routes import get_cities, get_routes, get_route, get_available_routes_for_city, CITIES, ROUTES

def test_get_cities():
    cities = get_cities()
    assert isinstance(cities, list)
    assert len(cities) == len(CITIES)
    for city in cities:
        assert "name" in city
        assert "lat" in city
        assert "lng" in city
        assert "state" in city
        assert "elevation" in city
        assert city["name"] in CITIES

def test_get_routes():
    routes = get_routes()
    assert isinstance(routes, list)
    assert len(routes) == len(ROUTES)
    for route in routes:
        assert "id" in route
        assert "from" in route
        assert "to" in route
        assert "distance_km" in route
        assert "estimated_time" in route
        assert "segments" in route

def test_get_route_direct():
    # Aizawl to Silchar is a direct route in ROUTES
    route = get_route("Aizawl", "Silchar")
    assert route is not None
    assert route["id"] == "aizawl-silchar"
    assert route["from"] == "Aizawl"
    assert route["to"] == "Silchar"
    assert len(route["segments"]) == 3
    # Check that first segment matches source
    assert route["segments"][0]["from"]["name"] == "Aizawl"
    assert route["segments"][-1]["to"]["name"] == "Silchar"

def test_get_route_reversed():
    # Silchar to Aizawl is reversed
    route = get_route("Silchar", "Aizawl")
    assert route is not None
    assert route["id"] == "aizawl-silchar-reversed"
    assert route["from"] == "Silchar"
    assert route["to"] == "Aizawl"
    assert len(route["segments"]) == 3
    # Check segment reversal
    assert route["segments"][0]["from"]["name"] == "Silchar"
    assert route["segments"][-1]["to"]["name"] == "Aizawl"

def test_get_route_not_found():
    route = get_route("NonexistentCityA", "NonexistentCityB")
    assert route is None

def test_get_available_routes_for_city():
    # Let's check Aizawl
    destinations = get_available_routes_for_city("Aizawl")
    assert isinstance(destinations, list)
    # Aizawl connects to Silchar, Guwahati, etc.
    assert "Silchar" in destinations
    assert "Guwahati" in destinations

    # Check a city that has no connections (if any) or check nonexistent city
    assert get_available_routes_for_city("NonexistentCity") == []
