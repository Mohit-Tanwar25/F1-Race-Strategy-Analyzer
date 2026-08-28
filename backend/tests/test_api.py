import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import Base, engine, SessionLocal
from app.services.data_provider.real_f1_provider import RealF1DataProvider
from app.services.ingestion import ingest_race_data


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    provider = RealF1DataProvider()
    ingest_race_data(db, provider, season=2024, round_number=1)
    db.close()


def test_root_endpoint():
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "online"


def test_get_seasons():
    client = TestClient(app)
    resp = client.get("/api/seasons")
    assert resp.status_code == 200
    assert 2024 in resp.json()


def test_get_races():
    client = TestClient(app)
    resp = client.get("/api/seasons/2024/races")
    assert resp.status_code == 200
    races = resp.json()
    assert len(races) > 0


def test_get_race_detail_and_strategies():
    client = TestClient(app)
    # Get race list to find first race id
    races = client.get("/api/seasons/2024/races").json()
    race_id = races[0]["id"]

    # 1. Race Detail
    r_resp = client.get(f"/api/races/{race_id}")
    assert r_resp.status_code == 200
    assert r_resp.json()["name"] == "Bahrain Grand Prix"

    # 2. Strategies
    s_resp = client.get(f"/api/races/{race_id}/strategies")
    assert s_resp.status_code == 200
    strategies = s_resp.json()
    assert len(strategies) > 0
    assert len(strategies[0]["stints"]) > 0

    # 3. Degradation
    d_resp = client.get(f"/api/races/{race_id}/analysis/degradation")
    assert d_resp.status_code == 200
    assert len(d_resp.json()["drivers"]) > 0

    # 4. Undercuts & Overcuts
    u_resp = client.get(f"/api/races/{race_id}/analysis/undercuts")
    assert u_resp.status_code == 200

    o_resp = client.get(f"/api/races/{race_id}/analysis/overcuts")
    assert o_resp.status_code == 200


def test_invalid_race_id():
    client = TestClient(app)
    resp = client.get("/api/races/999999")
    assert resp.status_code == 404
