import mlflow
from mlflow.entities import ViewType


models = {
    "Random Forest": 1,
    "Ridge": 1,
    "Decision Tree": 1,
    "Gradient Boosting": 1,
    "Linear Regression": 1,
    "KNN Regressor": 1,
    "XGB Regressor": 1,
    "CatBoosting Regressor": 1,
    "AdaBoost Regressor": 1,
    "grid-search": 1
}

for model, _ in models.items():

    exp = mlflow.get_experiment_by_name(model)

    if exp:
        mlflow.delete_experiment(exp.experiment_id)