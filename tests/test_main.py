import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_create_trajectory():
    response = client.post(
        "/trajectory/", params={"x": 1.0, "y": 2.0, "timestamp": 1234567890.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], int)


def test_get_trajectories():
    # First, create a trajectory point
    client.post("/trajectory/", params={"x": 1.0, "y": 2.0, "timestamp": 1234567890.0})

    # Then, get all trajectories
    response = client.get("/trajectory/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "x" in data[0]
    assert "y" in data[0]
    assert "timestamp" in data[0]


def test_delete_trajectories():
    # First, create a trajectory point
    client.post("/trajectory/", params={"x": 1.0, "y": 2.0, "timestamp": 1234567890.0})

    # Then, delete all trajectories
    response = client.delete("/trajectory/")
    assert response.status_code == 200
    assert response.json() == {"message": "All trajectory points deleted successfully."}

    # Verify that all trajectories are deleted
    response = client.get("/trajectory/")
    assert response.status_code == 200
    assert response.json() == []


def test_plan_rectangular_trajectory():
    response = client.post(
        "/plan/rectangular/",
        params={"width": 5.0, "height": 5.0, "step_size": 0.25},
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "points_generated" in data
    assert "obstacles_processed" in data
    assert data["message"] == "Trajectory planned and stored successfully"
    assert data["obstacles_processed"] == 0

    # Verify that trajectories are stored
    response = client.get("/trajectory/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_plan_rectangular_trajectory_with_obstacles():
    obstacles = [(1.0, 1.0, 0.5, 0.5)]
    response = client.post(
        "/plan/rectangular/",
        params={"width": 5.0, "height": 5.0, "step_size": 0.25, "obstacles": obstacles},
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "points_generated" in data
    assert "obstacles_processed" in data
    assert data["message"] == "Trajectory planned and stored successfully"
    assert data["obstacles_processed"] == 1

    # Verify that trajectories are stored
    response = client.get("/trajectory/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
