import requests
import pytest

# Base URL of the API deployed on Cloud Run
BASE_URL = "https://flask-api-34181851867.us-central1.run.app"

def test_data_endpoint():
    """
    Test the /data endpoint to ensure it returns the expected data.
    """
    # Send a GET request to the /data endpoint
    response = requests.get(f"{BASE_URL}/data")
    
    # Assert that the response status code is 200
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    # Assert that the response is JSON
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")
    
    # Assert that the response contains the 'data' key
    assert "data" in data, "'data' key not found in response"
    
    # Assert that the data contains the expected fields
    for item in data["data"]:
        assert "user_id" in item, "'user_id' not found in item"
        assert "email" in item, "'email' not found in item"
        assert "name" in item, "'name' not found in item"

if __name__ == "__main__":
    pytest.main()
