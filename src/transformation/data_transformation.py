from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging as logger
from src.common.utils import save_object, load_data
import warnings
warnings.filterwarnings("ignore")


def data_transformer() -> ColumnTransformer:
    """
    This function creates a data transformation object
    """
    
    try:
        num_cols = ["writing_score", "reading_score"]
        cat_cols = ["gender", "race_ethnicity",
                   "parental_level_of_education",
                   "lunch",
                   "test_preparation_course"]
        
        num_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler(with_mean=False))
                # ("scaler", StandardScaler())
            ]
        )
        # Setting mean=False means mean is set to 0 and standardization will be zero centric instead of mean (actual mean of the data) centric. By default it is set to True.

        cat_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder", OneHotEncoder()),
                ("scaler", StandardScaler(with_mean=False))
            ]
        )

        logger.info(f"Numerical columns: {num_cols}")
        logger.info(f"Categorical columns: {cat_cols}")

        preprocessor = ColumnTransformer(
            [
                ("num_pipeline", num_pipeline, num_cols),
                ("cat_pipeline", cat_pipeline, cat_cols)
            ]
        )

        return preprocessor

    except Exception as e:
        raise CustomException(e)
    

def initiate_data_transformation(train_df: pd.DataFrame, test_df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, ColumnTransformer]:
    """
    This function is responsible for tranforming into trainable objects
    """
    try:
        logger.info("Obtaining preprocessing object")
        preprocessing_obj = data_transformer()

        target_col = "math_score"

        input_feature_train_df = train_df.drop(columns=[target_col])
        target_feature_train_df = train_df[target_col]

        input_feature_test_df = test_df.drop(columns=[target_col])
        target_feature_test_df = test_df[target_col]

        logger.info(f"Applying preprocessing object on train df and test df.")

        input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
        input_feature_test_arr = preprocessing_obj.fit_transform(input_feature_test_df)

        train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
        test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]


        return (train_arr, test_arr, preprocessing_obj)
    
    except Exception as e:
        raise CustomException(e)
    
def save_data_transformation_outs() -> None:
    """
    This function is to save all the objects created while data transforming
    """
    try:
        home_dir = Path(__file__).parent.parent.parent

        processed_data_path = home_dir / "data/processed"
        interim_data_path = home_dir / "data/interim"
        processed_data_path.mkdir(parents=True, exist_ok=True)

        train_df = load_data(interim_data_path / "train.csv")
        test_df = load_data(interim_data_path / "test.csv")

        train_arr, test_arr, preprocessing_obj = initiate_data_transformation(train_df, test_df)

        save_object(processed_data_path, train_arr, "train_arr.joblib")
        save_object(processed_data_path, test_arr, "test_arr.joblib")
        save_object(processed_data_path, preprocessing_obj, "preprocessor.joblib")

        logger.info(f"Saved processed objects")

    except Exception as e:
        raise CustomException(e)
    


def main() -> None:
    """main function to call other functions"""
    save_data_transformation_outs()


if __name__ == "__main__":
    main()