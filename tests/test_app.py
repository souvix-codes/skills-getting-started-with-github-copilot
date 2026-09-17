from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_root_redirects_to_static_index():
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_details():
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == activities
    assert "Chess Club" in response.json()
    assert "description" in response.json()["Chess Club"]
    assert "participants" in response.json()["Chess Club"]


def test_signup_adds_participant_to_activity():
    # Arrange
    activity_name = f"Test Activity {uuid4()}"
    email = f"student-{uuid4()}@mergington.edu"
    activities[activity_name] = {
        "description": "A temporary test activity",
        "schedule": "Mondays, 3:00 PM",
        "max_participants": 10,
        "participants": [],
    }

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]
    del activities[activity_name]


def test_signup_for_unknown_activity_returns_404():
    # Arrange
    activity_name = f"Missing Activity {uuid4()}"
    email = f"student-{uuid4()}@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_duplicate_signup_returns_400():
    # Arrange
    activity_name = f"Test Activity {uuid4()}"
    email = f"student-{uuid4()}@mergington.edu"
    activities[activity_name] = {
        "description": "A temporary test activity",
        "schedule": "Tuesdays, 3:00 PM",
        "max_participants": 10,
        "participants": [email],
    }

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert activities[activity_name]["participants"] == [email]
    del activities[activity_name]