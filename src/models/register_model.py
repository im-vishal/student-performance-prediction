import json
import mlflow
import dagshub
import warnings
import os

from src.logger import logging as logger
from src.exception import CustomException
from src.common.utils import load_model_info
from pathlib import Path

warnings.filterwarnings('ignore')

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

# dagshub.init(repo_owner=repo_owner, repo_name=repo_name, mlflow=True)


def register_model(model_name: str, model_info: dict):
    """Register the model to the MLflow Model Registry."""
    try:
        model_uri = f"runs:/{model_info['run_id']}/{model_info['model_path']}"
        
        # Register the model
        model_version = mlflow.register_model(model_uri, model_name)
        
        # Transition the model to "Staging" stage
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name=model_name,
            version=model_version.version,
            stage="Staging"
        )
        
        logger.debug(f'Model {model_name} version {model_version.version} registered and transitioned to Staging.')
    except Exception as e:
        raise CustomException(e)

def main():
    try:
        model_info_path = Path('reports/experiment_info.json')
        model_info = load_model_info(model_info_path)
        
        model_name = model_info['model_name']
        # print(model_name)
        # print(f"{model_info = }")
        register_model(model_name, model_info)
    except Exception as e:
        raise CustomException(e)

if __name__ == '__main__':
    main()