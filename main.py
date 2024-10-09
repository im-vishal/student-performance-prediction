from fastapi import FastAPI
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Literal
import uvicorn
import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
import dagshub
import warnings

from src.common.utils import load_object

warnings.filterwarnings("ignore")

app = FastAPI(
    title="Score Prediction",
    description="This API will do student score prediction."
)

dagshub_url = "https://dagshub.com"
repo_owner = 'im-vishal'
repo_name = 'student-performance-prediction'

# Set up MLflow tracking URI
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

dagshub.init(repo_owner=repo_owner, repo_name=repo_name, mlflow=True)

# Load preprocessor and model globally
preprocessor = load_object(Path("data/processed/preprocessor.joblib"))

# load model from model registry
def get_latest_model_version(model_name):
    client = mlflow.MlflowClient()
    latest_version = client.get_latest_versions(model_name, stages=["Production"])
    if not latest_version:
        latest_version = client.get_latest_versions(model_name, stages=["None"])
    return latest_version[0].version if latest_version else None

model_name = "Ridge"
model_version = get_latest_model_version(model_name)

model_uri = f'models:/{model_name}/{model_version}'
print(f"{model_uri = }")
model = mlflow.pyfunc.load_model(model_uri)


@app.get('/')
def index():
    return "Welcome to API for student score prediction."



# Pydantic model for input validation
class PredictionRequest(BaseModel):
    gender: Literal['male', 'female'] = Field(..., description="Gender of the person")
    race_ethnicity: Literal['group A', 'group B', 'group C', 'group D', 'group E'] = Field(..., description="Ethnicity group")
    parental_level_of_education: Literal["associate's degree", "bachelor's degree", "high school", "master's degree", "some college", "some high school"] = Field(..., description="Parental education level")
    lunch: Literal["free/reduced", "standard"] = Field(..., description="Type of lunch provided")
    test_preparation_course: Literal["none", "completed"] = Field(..., description="Test preparation course status")
    reading_score: int = Field(..., description="Score in reading test")
    writing_score: int = Field(..., description="Score in writing test")

# Function to preprocess and predict
def predict(preprocessor, model, input_data: dict):
    input_df = pd.DataFrame([input_data])

    transformed_data = preprocessor.transform(input_df)

    predictions = model.predict(transformed_data)

    return predictions

# Prediction Endpoint
@app.post('/predict')
async def predict_score(received_data: PredictionRequest):
    input_data = received_data.model_dump()

    results = predict(preprocessor, model, input_data)

    return {"prediction": float(results[0])}

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)