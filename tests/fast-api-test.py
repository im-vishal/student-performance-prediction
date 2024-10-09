import unittest
import os
import mlflow
from fastapi.testclient import TestClient
from main import app

# Set up Dagshub credentials for MLflow tracking
dagshub_token = os.getenv('DAGSHUB_PAT')
if not dagshub_token:
    raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

dagshub_url = "https://dagshub.com"
repo_owner = 'im-vishal'
repo_name = 'student-performance-prediction'

# Set up MLflow tracking URI
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

class FastAPITests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a TestClient instance for testing the FastAPI app
        cls.client = TestClient(app)

    # Test the home page (index endpoint)
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '"Welcome to API for student score prediction."')

    # Test the prediction endpoint
    def test_predict_score(self):
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

        # Make a POST request to /predict with mock data
        response = self.client.post('/predict', json=mock_input_data)

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the prediction value
        self.assertIn("prediction", response.json())
        self.assertIsInstance(response.json()["prediction"], float)

if __name__ == '__main__':
    unittest.main()
