import numpy as np
import pandas as pd
import yaml
import joblib
import json
import dagshub
import mlflow
import os
import mlflow.sklearn

from src.exception import CustomException
from pathlib import Path
from src.logger import logging as logger

from sklearn.model_selection import GridSearchCV
from typing import Any

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


def load_data(data_path: Path | str) -> pd.DataFrame:
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(data_path)
        logger.debug('Data loaded from %s', data_path)
        return df
    except Exception as e:
        raise CustomException(e)

def load_params(params_path: Path) -> dict:
    """Load parameters from a YAML file."""
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logger.debug('Parameters retrieved from %s', params_path)
        return params
    except Exception as e:
        raise CustomException(e)


def save_data(data: pd.DataFrame, filename: str, data_path: Path) -> None:
    """Save the train and test datasets."""
    try:
        data.to_csv(data_path / filename, index=False)
        logger.debug('Train and test data saved to %s', data_path)
    except Exception as e:
        raise CustomException(e)

def save_object(file_path: Path, obj: object, file_name: str) -> None:
    """Save the joblib object."""
    try:
        file_path.mkdir(parents=True, exist_ok=True)

        joblib.dump(obj, file_path / file_name)
        logger.debug('Object saved to %s with name %s', file_path, file_name)
    except Exception as e:
        raise CustomException(e)
    
def evaluate_models(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, models: dict) -> dict:
    """Evaluate the model"""
    try:
        report = {}

        for name, model in models.items():
            mlflow.autolog()
            mlflow.set_experiment(name)
            with mlflow.start_run(run_name=name) as run:
                if name == "CatBoosting Regressor":
                    model.fit(X_train, y_train, silent=True)
                else:
                    model.fit(X_train, y_train)
                r2 = model.score(X_test, y_test)
                report[name] = r2

                home_dir = Path(__file__).parent.parent.parent
                metrics_path = home_dir / "reports/metrics.json"
                # Save model info
                save_metrics(report, metrics_path)
        return report
    except Exception as e:
        raise CustomException(e)
    

def tune_hyperparameters(X_train, y_train, X_test, y_test, model, param, model_name):
    try:
        mlflow.autolog()
        mlflow.set_experiment("grid_search")
        gs = GridSearchCV(model, param, cv=5, n_jobs=-1)
        with mlflow.start_run(run_name=(model_name + "grid")) as parent:
            gs.fit(X_train, y_train)
            for i in range(len(gs.cv_results_['params'])):
                with mlflow.start_run(nested=True) as child:
                    mlflow.log_params(gs.cv_results_['params'][i])
                    mlflow.log_metric("r2", gs.cv_results_['mean_test_score'][i])
        mlflow.autolog()
        mlflow.set_experiment("grid_search")
        model.set_params(**gs.best_params_)
        with mlflow.start_run(run_name="best-model") as parent:
            model.fit(X_train, y_train)
            r2 = model.score(X_test, y_test)
            save_model_info(parent.info.run_id, "model", "reports/experiment_info.json", model_name)
            mlflow.set_tag('model', model_name)

            return r2, model
    
    except Exception as e:
        raise CustomException(e)
    

def load_object(file_name: Path) -> Any:
    """load the joblib object"""
    try:
        return joblib.load(file_name)
    except Exception as e:
        raise CustomException(e)
    
def save_metrics(metrics: dict, file_path: Path) -> None:
    """Save the evaluation metrics to a JSON file."""
    try:
        with open(file_path, 'w') as file:
            json.dump(metrics, file, indent=4)
        logger.info('Metrics saved to %s', file_path)
    except Exception as e:
        raise CustomException(e)
    
def save_model_info(run_id: str, model_path: str, file_path: str, model_name: str) -> None:
    """Save the model run ID and path to a JSON file."""
    try:
        model_info = {'run_id': run_id, 'model_path': model_path, 'model_name': model_name}
        with open(file_path, 'w') as file:
            json.dump(model_info, file, indent=4)
        logger.info('Model info saved to %s', file_path)
    except Exception as e:
        raise CustomException(e)
    