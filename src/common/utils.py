import numpy as np
import pandas as pd
import yaml
import joblib

from src.exception import CustomException
from pathlib import Path
from src.logger import logging as logger

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
    
def evaluate_model(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, models: dict) -> dict:
    try:
        report = {}

        for name, model in models.items():
            model.fit(X_train, y_train)
            r2 = model.score(X_test, y_test)
            report[name] = r2

        return report
    except Exception as e:
        raise CustomException(e)