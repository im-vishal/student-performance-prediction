# promote model

import os
import mlflow

from pathlib import Path
from src.common.utils import load_model_info
from src.exception import CustomException

def promote_model(model_name):
    # Set up DagsHub credentials for MLflow tracking
    dagshub_token = os.getenv("DAGSHUB_PAT")
    if not dagshub_token:
        raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    dagshub_url = "https://dagshub.com"
    repo_owner = 'im-vishal'
    repo_name = 'student-performance-prediction'

    # Set up MLflow tracking URI
    mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

    client = mlflow.MlflowClient()

    # model_name = "my_model"
    # Get the latest version in staging
    latest_version_staging = client.get_latest_versions(model_name, stages=["Staging"])[0].version

    # Archive the current production model
    prod_versions = client.get_latest_versions(model_name, stages=["Production"])
    for version in prod_versions:
        client.transition_model_version_stage(
            name=model_name,
            version=version.version,
            stage="Archived"
        )

    # Promote the new model to production
    client.transition_model_version_stage(
        name=model_name,
        version=latest_version_staging,
        stage="Production"
    )
    print(f"Model version {latest_version_staging} promoted to Production")

if __name__ == "__main__":
    try:
        model_info_path = Path('reports/experiment_info.json')
        model_info = load_model_info(model_info_path)
        
        model_name = model_info['model_name']
        promote_model(model_name)
    except Exception as e:
        raise CustomException(e)