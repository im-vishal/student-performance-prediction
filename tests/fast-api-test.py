import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

class FastAPITests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a TestClient instance for testing the FastAPI app
        cls.client = TestClient(app)

    # @patch('main.load_object')  # Mock load_object to prevent DAGSHUB_PAT issue
    @patch('main.mlflow.pyfunc.load_model')  # Mock MLflow model loading
    def test_home_page(self, mock_load_model):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '"Welcome to API for student score prediction."')

    # @patch('main.load_object')  # Mock load_object
    @patch('main.mlflow.pyfunc.load_model')  # Mock MLflow model loading
    def test_predict_score(self, mock_load_model):
        # Mock input data
        mock_input_data = {
            "gender": "male",
            "race_ethnicity": "group A",
            "parental_level_of_education": "high school",
            "lunch": "standard",
            "test_preparation_course": "completed",
            "reading_score": 75,
            "writing_score": 80
        }

        # Mock the prediction return value
        mock_load_model.return_value.predict.return_value = [88.0]

        # Make a POST request to /predict with mock data
        response = self.client.post('/predict', json=mock_input_data)

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the prediction value
        self.assertIn("prediction", response.json())
        self.assertIsInstance(response.json()["prediction"], float)

if __name__ == '__main__':
    unittest.main()
