import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import numpy as np
from starlette.responses import HTMLResponse

# IMPORTANT: patch model BEFORE importing app
with patch("app.load_model_once") as mock_loader:
    mock_model = MagicMock()
    mock_loader.return_value = mock_model

from app import app
client = TestClient(app)


class TestFastAPIApp(unittest.TestCase):

    # Test Home Route
    @patch("app.templates.TemplateResponse")
    def test_homepage(self, mock_template):
        mock_template.return_value = HTMLResponse(content="OK", status_code=200)
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    # Test Predict Endpoint
    @patch("app.model")   # patch global model directly
    def test_predict_endpoint(self, mock_model):

        # Mock model behavior
        mock_model.predict.return_value = np.array([1])
        mock_model.predict_proba.return_value = np.array([[0.2, 0.8]])

        form_data = {
            "cgpa": "7.6",
            "internship": "1",
            "certification": "2",
            "projects": "3",
            "apptitude_score": "67",
            "softskill_rating": "4.5",
            "ExtracurricularActivities": "1",
            "placementT": "1",
            "SSC": "60",
            "HSC": "50"
        }

        # ✅ Send as FORM DATA (not JSON)
        response = client.post("/predict", data=form_data)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["prediction"], 1)
        self.assertEqual(data["probability"], [0.2, 0.8])


if __name__ == "__main__":
    unittest.main()