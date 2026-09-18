import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_list_sessions_returns_races_for_year():
    response = client.get("/sessions", params={"year": 2023})

    assert response.status_code == 200
    events = response.json()
    assert any(e["event"] == "Italian Grand Prix" for e in events)
    # pre-season testing (round 0) should be excluded
    assert all(e["round"] > 0 for e in events)


def test_list_drivers_ordered_by_finishing_position():
    response = client.get("/session/2023/Monza/drivers")

    assert response.status_code == 200
    drivers = response.json()["drivers"]
    assert drivers[0] == "VER"
    assert "TSU" in drivers


def test_stints_endpoint_matches_known_pit_stop():
    response = client.get("/session/2023/Monza/stints")

    assert response.status_code == 200
    data = response.json()
    ver_stints = [s for s in data["stints"] if s["driver"] == "VER"]
    assert len(ver_stints) == 2
    assert ver_stints[0]["compound"] == "MEDIUM"
    assert ver_stints[1]["compound"] == "HARD"


def test_pace_endpoint_two_drivers_returns_crossovers():
    response = client.get(
        "/session/2023/Monza/pace", params={"drivers": "VER,PER"}
    )

    assert response.status_code == 200
    data = response.json()
    assert set(data["series"].keys()) == {"VER", "PER"}
    assert data["series"]["VER"]["pit_laps"] == [20]
    assert len(data["crossovers"]) > 0


def test_pace_endpoint_requires_drivers():
    response = client.get("/session/2023/Monza/pace", params={"drivers": ""})

    assert response.status_code == 400


def test_pitstops_endpoint_filtered_by_driver():
    response = client.get(
        "/session/2023/Monza/pitstops", params={"driver": "ver"}
    )

    assert response.status_code == 200
    stops = response.json()["stops"]
    assert len(stops) == 1
    assert stops[0]["lap"] == 20
    assert stops[0]["driver"] == "VER"


def test_unknown_event_returns_404():
    response = client.get("/session/2099/NotARealPlace/stints")

    assert response.status_code == 404
