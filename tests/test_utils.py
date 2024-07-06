import json
import os
import tempfile
from typing import Dict, List
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.utils import convert_data_frame_to_json, read_xls_file


@pytest.fixture
def sample_excel_file() -> str:
    """
    Fixture to provide a temporary Excel file path with sample data.

    Returns:
        str: File path to the temporary Excel file.
    """
    data = {
        "Дата операции": ["2023-01-01", "2023-01-02"],
        "Дата платежа": ["2023-01-02", "2023-01-03"],
        "Номер карты": ["1234", "5678"],
        "Статус": ["Completed", "Pending"],
        "Сумма операции": [100.0, 200.0],
        "Валюта операции": ["USD", "EUR"],
        "Сумма платежа": [99.0, 198.0],
        "Валюта платежа": ["USD", "EUR"],
        "Кэшбэк": [5.0, 10.0],
        "Категория": ["Groceries", "Electronics"],
        "MCC": ["1234", "5678"],
        "Описание": ["Grocery shopping", "Buying electronics"],
        "Бонусы (включая кэшбэк)": [2.0, 4.0],
        "Округление на инвесткопилку": [1.0, 2.0],
        "Сумма операции с округлением": [101.0, 202.0]
    }
    df = pd.DataFrame(data)
    _, path = tempfile.mkstemp(suffix=".xlsx")
    df.to_excel(path, index=False, engine="openpyxl")
    yield path
    os.remove(path)


@pytest.mark.parametrize("input_data, expected_output", [
    ("testdata.xlsx", [
        {
            "Дата операции": "2023-01-01",
            "Дата платежа": "2023-01-02",
            "Номер карты": 1234,
            "Статус": "Completed",
            "Сумма операции": 100,
            "Валюта операции": "USD",
            "Сумма платежа": 99,
            "Валюта платежа": "USD",
            "Кэшбэк": 5,
            "Категория": "Groceries",
            "MCC": 1234,
            "Описание": "Grocery shopping",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 1,
            "Сумма операции с округлением": 101
        },
        {
            "Дата операции": "2023-01-02",
            "Дата платежа": "2023-01-03",
            "Номер карты": 5678,
            "Статус": "Pending",
            "Сумма операции": 200,
            "Валюта операции": "EUR",
            "Сумма платежа": 198,
            "Валюта платежа": "EUR",
            "Кэшбэк": 10,
            "Категория": "Electronics",
            "MCC": 5678,
            "Описание": "Buying electronics",
            "Бонусы (включая кэшбэк)": 4,
            "Округление на инвесткопилку": 2,
            "Сумма операции с округлением": 202
        }
    ])
])
def test_read_xls_file(sample_excel_file: str, input_data: str, expected_output: List[Dict[str, any]]) -> None:
    """
    Test function for `read_xls_file` with parameterized inputs and expected outputs.

    Args:
        sample_excel_file (str): Path to the sample Excel file.
        input_data (str): Placeholder for the parameterized input data (not used directly).
        expected_output (List[Dict[str, any]]): List of dictionaries representing expected JSON objects.

    Raises:
        AssertionError: If the actual output JSON does not match the expected JSON.
    """
    mock_logger = MagicMock()

    with patch('src.utils.logger', mock_logger):
        result = read_xls_file(sample_excel_file)
        mock_logger.info.assert_called_once_with("Data is being read from the table...")

        converted_json = convert_data_frame_to_json(result)

        parsed_json = json.loads(converted_json)
        assert len(parsed_json) == len(expected_output)

        for actual, expected in zip(parsed_json, expected_output):
            assert actual == expected
