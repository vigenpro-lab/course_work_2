import json
import logging
from typing import Any, Dict, List

import pandas as pd
from pandas import DataFrame

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def read_xls_file(path: str) -> DataFrame:
    """
    Reads an Excel file and returns its contents as a DataFrame.

    Args:
        path (str): The path to the Excel file.

    Returns:
        DataFrame: The contents of the Excel file as a DataFrame.
    """
    logger.info("Data is being read from the table...")
    return pd.read_excel(path, engine="openpyxl")


def convert_data_frame_to_json(df: DataFrame) -> str:
    """
    Converts a DataFrame to a JSON string.

    Args:
        df (DataFrame): The DataFrame to convert.

    Returns:
        str: The JSON string representation of the DataFrame.
    """
    lst: List[Dict[str, Any]] = []
    for idx, row in df.iterrows():
        lst.append({
            "Дата операции": row["Дата операции"],
            "Дата платежа": row["Дата платежа"],
            "Номер карты": row["Номер карты"],
            "Статус": row["Статус"],
            "Сумма операции": row["Сумма операции"],
            "Валюта операции": row["Валюта операции"],
            "Сумма платежа": row["Сумма платежа"],
            "Валюта платежа": row["Валюта платежа"],
            "Кэшбэк": row["Кэшбэк"],
            "Категория": row["Категория"],
            "MCC": row["MCC"],
            "Описание": row["Описание"],
            "Бонусы (включая кэшбэк)": row["Бонусы (включая кэшбэк)"],
            "Округление на инвесткопилку": row["Округление на инвесткопилку"],
            "Сумма операции с округлением": row["Сумма операции с округлением"]
        })

    return json.dumps(lst, ensure_ascii=False, indent=4)
