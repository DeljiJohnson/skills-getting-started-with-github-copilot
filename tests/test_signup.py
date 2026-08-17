"""
Tests for POST and DELETE /activities/{activity_name}/signup endpoints.

These tests verify signup and unregister functionality, including happy paths,
error cases (404, 400), and edge cases like re-signup after unregister.

All tests follow the AAA (Arrange-Act-Assert) pattern for clarity.
"""


# ============================================================================
# POST Signup - Happy Path Tests
# ============================================================================

def test_signup_valid_email_returns_200(client, reset_activities):
    """
    Arrange: Define a new valid email and activity
    Act: POST request to signup endpoint with valid data
    Assert: Verify status code is 200 and response contains success message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert email in response.json()["message"]


def test_signup_adds_participant_to_activity(client, reset_activities):
    """
    Arrange: Define a new valid email and activity
    Act: POST signup request, then GET activities to verify
    Assert: Verify participant is added to activity's participants list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    verify_response = client.get("/activities")
    activities = verify_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_decreases_available_spots(client, reset_activities):
    """
    Arrange: Get initial spot count, define new email
    Act: POST signup request
    Assert: Verify available spots decreased by 1
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_response = client.get("/activities")
    initial_activities = initial_response.json()
    initial_spots = initial_activities[activity_name]["max_participants"] - len(
        initial_activities[activity_name]["participants"]
    )
    
    # Act
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    verify_response = client.get("/activities")
    activities = verify_response.json()
    new_spots = activities[activity_name]["max_participants"] - len(
        activities[activity_name]["participants"]
    )
    assert new_spots == initial_spots - 1


# ============================================================================
# POST Signup - Error Cases
# ============================================================================

def test_signup_nonexistent_activity_returns_404(client, reset_activities):
    """
    Arrange: Define a non-existent activity name
    Act: POST signup request to non-existent activity
    Assert: Verify status code is 404 and error message indicates not found
    """
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_duplicate_email_returns_400(client, reset_activities):
    """
    Arrange: Use an email already signed up for an activity
    Act: POST signup request with duplicate email
    Assert: Verify status code is 400 and error indicates already signed up
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered in Chess Club
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


# ============================================================================
# DELETE Unregister - Happy Path Tests
# ============================================================================

def test_unregister_valid_email_returns_200(client, reset_activities):
    """
    Arrange: Define an email registered in an activity
    Act: DELETE request to unregister endpoint
    Assert: Verify status code is 200 and response contains success message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    assert email in response.json()["message"]


def test_unregister_removes_participant(client, reset_activities):
    """
    Arrange: Define an email registered in an activity
    Act: DELETE unregister request, then GET activities to verify
    Assert: Verify participant is removed from activity's participants list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act
    client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    verify_response = client.get("/activities")
    activities = verify_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_increases_available_spots(client, reset_activities):
    """
    Arrange: Get initial spot count, define email to unregister
    Act: DELETE unregister request
    Assert: Verify available spots increased by 1
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    initial_response = client.get("/activities")
    initial_activities = initial_response.json()
    initial_spots = initial_activities[activity_name]["max_participants"] - len(
        initial_activities[activity_name]["participants"]
    )
    
    # Act
    client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    verify_response = client.get("/activities")
    activities = verify_response.json()
    new_spots = activities[activity_name]["max_participants"] - len(
        activities[activity_name]["participants"]
    )
    assert new_spots == initial_spots + 1


# ============================================================================
# DELETE Unregister - Error Cases
# ============================================================================

def test_unregister_nonexistent_activity_returns_404(client, reset_activities):
    """
    Arrange: Define a non-existent activity name
    Act: DELETE unregister request to non-existent activity
    Assert: Verify status code is 404
    """
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404


def test_unregister_email_not_enrolled_returns_400(client, reset_activities):
    """
    Arrange: Use an email not registered for an activity
    Act: DELETE unregister request with non-enrolled email
    Assert: Verify status code is 400 and error indicates not signed up
    """
    # Arrange
    activity_name = "Chess Club"
    email = "notstudent@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()


# ============================================================================
# Edge Cases - Signup and Unregister Interactions
# ============================================================================

def test_can_resignup_after_unregister(client, reset_activities):
    """
    Arrange: Define email already signed up for activity
    Act: DELETE to unregister, then POST to re-signup
    Assert: Verify email is re-added to participants after both operations
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act - Unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Act - Re-signup
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert unregister_response.status_code == 200
    assert signup_response.status_code == 200
    verify_response = client.get("/activities")
    activities = verify_response.json()
    assert email in activities[activity_name]["participants"]


def test_unregister_last_participant_leaves_empty_list(client, reset_activities):
    """
    Arrange: Find activity with only one participant, define that email
    Act: DELETE to unregister the last participant
    Assert: Verify participants list is empty
    """
    # Arrange
    # First add one participant to an activity, then unregister them
    activity_name = "Chess Club"
    new_email = "oneperson@mergington.edu"
    
    # Add new participant to an activity
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Remove one of the original participants to be left with just new_email
    original_email = "michael@mergington.edu"
    client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": original_email}
    )
    client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": "daniel@mergington.edu"}
    )
    
    # Now unregister the new person (should leave empty list)
    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert
    assert response.status_code == 200
    verify_response = client.get("/activities")
    activities = verify_response.json()
    assert len(activities[activity_name]["participants"]) == 0


def test_signup_multiple_students_same_activity(client, reset_activities):
    """
    Arrange: Define multiple new emails for the same activity
    Act: POST signup requests for each email
    Assert: Verify all are added to participants list
    """
    # Arrange
    activity_name = "Chess Club"
    emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
    
    # Act
    for email in emails:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Assert
    verify_response = client.get("/activities")
    activities = verify_response.json()
    for email in emails:
        assert email in activities[activity_name]["participants"]


def test_signup_same_student_different_activities(client, reset_activities):
    """
    Arrange: Define one email and multiple activities
    Act: POST signup requests for same email to different activities
    Assert: Verify email is added to all activities
    """
    # Arrange
    email = "multiactivity@mergington.edu"
    activities_to_join = ["Chess Club", "Programming Class", "Art Studio"]
    
    # Act
    for activity_name in activities_to_join:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Assert
    verify_response = client.get("/activities")
    activities_data = verify_response.json()
    for activity_name in activities_to_join:
        assert email in activities_data[activity_name]["participants"]
