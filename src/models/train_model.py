import numpy as np
import warnings

from pathlib import Path

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging as logger


from src.common.utils import save_object, evaluate_models, load_params, tune_hyperparameters, load_object

warnings.filterwarnings("ignore")

def initiate_model_trainer(train_arr: np.ndarray, test_arr: np.ndarray, params_path: Path) -> tuple:
    try:
        logger.info("Split train & test data")

        X_train, y_train, X_test, y_test = (
            train_arr[:, :-1],
            train_arr[:, -1],
            test_arr[:, :-1],
            test_arr[:, -1]
        )
        models = {
            "Random Forest": RandomForestRegressor(),
            "Ridge": Ridge(),
            "Decision Tree": DecisionTreeRegressor(),
            "Gradient Boosting": GradientBoostingRegressor(),
            "KNN Regressor": KNeighborsRegressor(),
            "XGB Regressor": XGBRegressor(),
            "CatBoosting Regressor": CatBoostRegressor(),
            "AdaBoost Regressor": AdaBoostRegressor()
        }

        # Evaluating models
        model_report: dict = evaluate_models(X_train, y_train, X_test, y_test, models)

        # print(model_report)
        logger.info(f"model_report: {model_report}")

        best_model = max(model_report, key=model_report.get)
        best_model_score = model_report[best_model]
        # print(best_model)
        logger.info(f"The best model is: {best_model}")
        best_model_obj = models[best_model]

        if best_model_score < 0.6:
            logger.info("No best model found.")
            raise CustomException("No best model found")
        else:
            logger.info(f"Best Model: {best_model} | R2 Score: {best_model_score}")

        # read hyperparameters from yaml file
        params = load_params(params_path)
        params_models = params['model_tuning']['models']

        # Tune hyperparameters of the best model
        if params_models[best_model]:
            r2, best_model_tuned = tune_hyperparameters(X_train, y_train, X_test, y_test, best_model_obj, params_models[best_model], best_model)

            if r2 > best_model_score:
                best_model_obj = best_model_tuned
                best_model_score = r2
                logger.info(f"Hyperparameter for {best_model} tuned | R2 Score: {best_model_score}")
            else:
                logger.info(f"Tuning didn't help, R2 Score for {best_model} is: {best_model_score}")
            
        return (best_model_obj, best_model_score)
    
    except Exception as e:
        raise CustomException(e)
    

def save_best_model() -> None:
    try:
        home_dir = Path(__file__).parent.parent.parent
        params_path = home_dir / "params.yaml"
        processed_path = home_dir / "data/processed"

        train_arr = load_object(processed_path / "train_arr.joblib")
        test_arr = load_object(processed_path / "test_arr.joblib")

        best_model, best_score = initiate_model_trainer(train_arr, test_arr, params_path)

        model_path = home_dir / "data/models"
        model_path.mkdir(parents=True, exist_ok=True)

        save_object(model_path, best_model, "best_model.joblib")
    except Exception as e:
        raise CustomException(e)


def main() -> None:
    """main function to call other functions"""
    save_best_model()


if __name__ == "__main__":
    main()