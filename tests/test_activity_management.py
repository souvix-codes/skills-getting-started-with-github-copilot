from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_unregister_participant_from_activity():
    # Arrange
    activity_name = f"Test Activity {uuid4()}"
    email = f"student-{uuid4()}@mergington.edu"

    activities[activity_name] = {
        "description": "A temporary test activity",
        "schedule": "Mondays, 3:00 PM",
        "max_participants": 10,
        "participants": [email],
    }

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]
    del activities[activity_name]


def test_unregister_missing_participant_returns_404():
    # Arrange
    activity_name = f"Test Activity {uuid4()}"
    missing_email = f"missing-{uuid4()}@mergington.edu"

    activities[activity_name] = {
        "description": "Another temporary test activity",
        "schedule": "Wednesdays, 4:00 PM",
        "max_participants": 10,
        "participants": [],
    }

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={missing_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == f"Participant {missing_email} not found in {activity_name}"
    del activities[activity_name]


def test_unregister_from_unknown_activity_returns_404():
    # Arrange
    activity_name = f"Missing Activity {uuid4()}"
    email = f"student-{uuid4()}@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
