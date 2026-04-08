from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import numpy as np

from app import app

client = TestClient(app)


# 🔹 Test Home Route
def test_home():
    response = client.get("/")
    assert response.status_code == 200


# 🔹 Test Prediction (Mocked Model)
@patch("main.load_model_once")
def test_predict_success(mock_model_loader):

    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([1])
    mock_model.predict_proba.return_value = np.array([[0.1, 0.9]])

    mock_model_loader.return_value = mock_model

    payload = {
        "cgpa": 3.5,
        "internship": 1,
        "certification": 2,
        "projects": 3,
        "apptitude_score": 80,
        "softskill_rating": 4.5,
        "ExtracurricularActivities": 1,
        "placementT": 1,
        "SSC": 85,
        "HSC": 90
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["prediction"] == 1
    assert data["probability"] == [0.1, 0.9]


# 🔹 Test Validation Error (Pydantic handles this)
def test_predict_invalid_input():
    payload = {
        "cgpa": "invalid",  # ❌ wrong type
        "internship": 1,
        "certification": 2,
        "projects": 3,
        "apptitude_score": 80,
        "softskill_rating": 4.5,
        "ExtracurricularActivities": 1,
        "placementT": 1,
        "SSC": 85,
        "HSC": 90
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


# 🔹 Test Missing Field
def test_predict_missing_field():
    payload = {
        "cgpa": 3.5
        # missing other fields
    }

    response = client.post("/predict", json=payload)
    print('testing module')


    assert response.status_code == 422