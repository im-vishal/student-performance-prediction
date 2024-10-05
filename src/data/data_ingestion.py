import yaml
from pathlib import Path
from src.logger import logging as logger
from src.exception import CustomException
from src.common.utils import (load_data, load_params, save_data)

from sklearn.model_selection import train_test_split

    
def split_data():
        home_dir = Path(__file__).parent.parent.parent

        params_path = home_dir / "params.yaml"
        params = load_params(params_path)
        test_size = params['data_ingestion']['test_size']


        raw_data_url = "https://raw.githubusercontent.com/im-vishal/artifacts/refs/heads/main/student.csv"
        raw_data_path = home_dir / "data/raw"
        raw_data_path.mkdir(parents=True, exist_ok=True)

        df = load_data(raw_data_url)
        save_data(df, "student.csv", raw_data_path)

        train_data, test_data = train_test_split(df, test_size=test_size, random_state=42)

        data_split_dir = home_dir / "data/interim"
        data_split_dir.mkdir(parents=True, exist_ok=True)
        save_data(train_data, "train.csv", data_split_dir)
        save_data(test_data, "test.csv", data_split_dir)


def main():
    try:
         split_data()
    except Exception as e:
        raise CustomException(e)

if __name__ == '__main__':
    main()