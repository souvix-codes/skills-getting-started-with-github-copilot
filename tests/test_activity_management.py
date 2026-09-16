from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = f"Test Activity {uuid4()}"
    email = f"student-{uuid4()}@mergington.edu"

    activities[activity_name] = {
        "description": "A temporary test activity",
        "schedule": "Mondays, 3:00 PM",
        "max_participants": 10,
        "participants": [email],
    }

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    activity_name = f"Test Activity {uuid4()}"
    missing_email = f"missing-{uuid4()}@mergington.edu"

    activities[activity_name] = {
        "description": "Another temporary test activity",
        "schedule": "Wednesdays, 4:00 PM",
        "max_participants": 10,
        "participants": [],
    }

    response = client.delete(f"/activities/{activity_name}/participants?email={missing_email}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Participant {missing_email} not found in {activity_name}"
