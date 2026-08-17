"""
Tests for GET /activities endpoint.

These tests verify that the activities listing endpoint returns the correct
data structure, includes all activities, and properly formats participant lists.

All tests follow the AAA (Arrange-Act-Assert) pattern for clarity.
"""


def test_get_activities_returns_200(client, reset_activities):
    """
    Arrange: Setup done by fixtures (client and reset_activities)
    Act: Make GET request to /activities
    Assert: Verify status code is 200 (success)
    """
    # Arrange
    # (fixtures provide setup)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200


def test_get_activities_returns_dict(client, reset_activities):
    """
    Arrange: Setup done by fixtures
    Act: Make GET request to /activities
    Assert: Verify response is a dictionary (JSON object)
    """
    # Arrange
    # (fixtures provide setup)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert isinstance(response.json(), dict)


def test_get_activities_includes_all_required_fields(client, reset_activities):
    """
    Arrange: Setup done by fixtures
    Act: Make GET request to /activities
    Assert: Verify each activity has all required fields
    """
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert len(activities) > 0, "Should return at least one activity"
    for activity_name, activity_data in activities.items():
        for field in required_fields:
            assert field in activity_data, f"Field '{field}' missing from {activity_name}"


def test_get_activities_participants_is_list(client, reset_activities):
    """
    Arrange: Setup done by fixtures
    Act: Make GET request to /activities
    Assert: Verify participants field is always a list
    """
    # Arrange
    # (fixtures provide setup)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(
            activity_data["participants"], list
        ), f"Participants for {activity_name} should be a list"


def test_get_activities_participants_are_emails(client, reset_activities):
    """
    Arrange: Setup done by fixtures
    Act: Make GET request to /activities
    Assert: Verify each participant is a string containing @ symbol (email format)
    """
    # Arrange
    # (fixtures provide setup)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str), f"Participant {participant} should be string"
            assert "@" in participant, f"Participant {participant} should contain @ (email format)"


def test_get_activities_includes_all_nine_activities(client, reset_activities):
    """
    Arrange: Define expected activities
    Act: Make GET request to /activities
    Assert: Verify all 9 seeded activities are present
    """
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Music Band",
        "Debate Club",
        "Science Club"
    ]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert len(activities) == 9, f"Expected 9 activities, got {len(activities)}"
    for activity_name in expected_activities:
        assert activity_name in activities, f"Expected activity '{activity_name}' not found"


def test_get_activities_participants_list_can_be_empty(client, reset_activities):
    """
    Arrange: Setup done by fixtures
    Act: Make GET request to /activities
    Assert: Verify that participants is a list (empty or populated)
    """
    # Arrange
    # (fixtures provide setup)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_data in activities.values():
        assert isinstance(activity_data["participants"], list)
        # Participants can be empty or populated
        assert all(isinstance(p, str) for p in activity_data["participants"])


def test_get_activities_max_participants_is_integer(client, reset_activities):
    """
    Arrange: Setup done by fixtures
    Act: Make GET request to /activities
    Assert: Verify max_participants is an integer
    """
    # Arrange
    # (fixtures provide setup)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(
            activity_data["max_participants"], int
        ), f"max_participants for {activity_name} should be integer"
        assert activity_data["max_participants"] > 0


def test_get_activities_schedule_is_string(client, reset_activities):
    """
    Arrange: Setup done by fixtures
    Act: Make GET request to /activities
    Assert: Verify schedule field contains a non-empty string
    """
    # Arrange
    # (fixtures provide setup)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(
            activity_data["schedule"], str
        ), f"schedule for {activity_name} should be string"
        assert len(activity_data["schedule"]) > 0, f"schedule for {activity_name} should not be empty"
