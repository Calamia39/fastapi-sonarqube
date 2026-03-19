"""
Tests for FastAPI application
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app, calculate_sum, divide_numbers

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World", "status": "ok"}

def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "fastapi-app"

def test_get_users():
    """Test get users endpoint"""
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert len(data["users"]) == 2

def test_calculate_sum():
    """Test calculate sum function"""
    assert calculate_sum(2, 3) == 5
    assert calculate_sum(-1, 1) == 0
    assert calculate_sum(0, 0) == 0

def test_divide_numbers():
    """Test divide numbers function"""
    assert divide_numbers(10, 2) == 5
    assert divide_numbers(9, 3) == 3
    
def test_divide_by_zero():
    """Test divide by zero raises exception"""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide_numbers(10, 0)