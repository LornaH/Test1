"""Backend FastAPI tests for the Mergington High School API."""


def test_get_activities_returns_expected_data(client):
    """Arrange-Act-Assert: GET /activities returns valid activity data."""
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities

    activity = activities["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_signup_registers_new_participant(client):
    """Arrange-Act-Assert: signup registers a new participant."""
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    activities = client.get("/activities").json()
    participants = [p.lower().strip() for p in activities[activity_name]["participants"]]
    assert email.lower() in participants


def test_duplicate_signup_returns_400(client):
    """Arrange-Act-Assert: duplicate signup returns 400."""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_remove_participant(client):
    """Arrange-Act-Assert: delete removes an existing participant."""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

    participants = client.get("/activities").json()[activity_name]["participants"]
    assert email.lower() not in [p.lower() for p in participants]


def test_remove_nonexistent_participant_returns_404(client):
    """Arrange-Act-Assert: deleting a missing participant returns 404."""
    activity_name = "Chess Club"
    email = "unknown@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
