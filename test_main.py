import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models import User

client = TestClient(app)

TEST_USER = {
    "email": "pytest1@example.com",
    "username": "pytestuser1",
    "password": "test123"
}

@pytest.fixture(autouse=True)
def clean_db():
    db = SessionLocal()
    db.query(User).filter(User.email.like("%pytest%")).delete()
    db.commit()
    db.close()
    yield
    db = SessionLocal()
    db.query(User).filter(User.email.like("%pytest%")).delete()
    db.commit()
    db.close()


# public endpoints
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()

def test_temperature_current():
    response = client.get("/temperature/current")
    assert response.status_code == 200
    assert "stations" in response.json()

def test_temperature_specific():
    response = client.get("/temperature/Kwun%20Tong")
    assert response.status_code == 200
    assert "temperature" in response.json()

def test_temperature_nonexistent_station():
    response = client.get("/temperature/HKU")
    assert response.status_code == 404
    data = response.json()
    assert "error" in response.json()["detail"]

def test_rainfall():
    response = client.get("/rainfall")
    assert response.status_code == 200
    assert "timestamp" in response.json()

def test_forecast():
    response = client.get("/forecast")
    assert response.status_code == 200
    assert "forecast" in response.json()

def test_forecast_with_days():
    response = client.get("/forecast?days=3")
    assert response.status_code == 200


#authentication
def test_register_user(clean_db):
    response = client.post("/users/register", json=TEST_USER)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == TEST_USER["email"]
    assert data["username"] == TEST_USER["username"]
    assert "id" in data

def test_register_duplicate_user():
    client.post("/users/register", json=TEST_USER)
    response = client.post("/users/register", json=TEST_USER)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]
    
def test_login_success():
    client.post("/users/register", json=TEST_USER)
    response = client.post("/login", json={
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    client.post("/users/register", json=TEST_USER)
    response = client.post("/login", json={
        "username": TEST_USER["username"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_login_nonexistent_user():
    response = client.post("/login", json={
        "username": "wronguser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


# protected endpoints
def test_endpoint_without_token():
    response = client.get("/protected")
    assert response.status_code == 401
    assert "authorization header" in response.json()["detail"].lower()

def test_endpoint_with_valid_token():
    client.post("/users/register", json=TEST_USER)
    login_response = client.post("/login", json={
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    })
    token = login_response.json()["access_token"]

    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["user_id"] is not None

def test_endpoint_with_invalid_token():
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer 348689dfkjh29"}
    )
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()

def test_get_all_users():
    client.post("/users/register", json=TEST_USER)
    login_response = client.post("/login", json={
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    })
    token = login_response.json()["access_token"]
    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_cache_status():
    response = client.get("/cache/status")
    assert response.status_code == 200
    assert "cached_items" in response.json()
    assert "cached_keys" in response.json()

def test_clear_cache():
    response = client.delete("/cache/clear")
    assert response.status_code == 200
    assert "message" in response.json()