from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from pandas import DataFrame

from src.utils import read_xls_file
from src.views import get_card_data, get_currency, get_data, get_stock_currency, get_time_of_day, top_transaction


@pytest.fixture
def sample_dataframe() -> DataFrame:
    """
    Fixture that provides a sample DataFrame loaded from an Excel file.
    """
    data = read_xls_file("data/operations.xlsx")
    return data


@pytest.fixture
def mock_requests_get() -> Mock:
    """
    Fixture that mocks the requests.get function.
    """
    with patch("requests.get") as mock_get:
        yield mock_get


def test_get_time_of_day():
    """
    Test for get_time_of_day function.
    """
    morning_time = datetime(2024, 1, 1, 7, 0, 0)  # 7:00 AM
    assert get_time_of_day(str(morning_time)) == "Доброе утро!"


def test_get_card_data(sample_dataframe: DataFrame):
    """
    Test for get_card_data function.
    """
    expected_output = [
        {'last_digits': '*2245', 'total_spent': -15166.97, 'cashback': 326.0},
        {'last_digits': '*5433', 'total_spent': -8700.27, 'cashback': 138.0},
        {'last_digits': 'Unknown', 'total_spent': -22145.37, 'cashback': 5.0}
    ]
    assert get_card_data(sample_dataframe) == expected_output


def test_top_transaction(sample_dataframe: DataFrame):
    """
    Test for top_transaction function.
    """
    expected_output = [
        {'date': '07.06.2024', 'amount': 5000.0, 'category': 'Переводы', 'description': 'Перевод между счетами'},
        {'date': '05.06.2024', 'amount': 4170.0, 'category': 'Переводы', 'description': 'Андрей А.'},
        {'date': '29.06.2024', 'amount': 3000.0, 'category': 'Переводы', 'description': 'Андрей А.'},
        {'date': '15.06.2024', 'amount': 1300.0, 'category': 'Переводы', 'description': 'Виген К.'},
        {'date': '21.06.2024', 'amount': 1000.0, 'category': 'Переводы', 'description': 'Андрей А.'}
    ]
    assert top_transaction(sample_dataframe) == expected_output


def test_get_currency(mock_requests_get: Mock):
    """
    Test for get_currency function.
    """
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"RUB": 70.0}}
    mock_requests_get.return_value = mock_response

    currency_data = get_currency()
    assert currency_data == [{'currency': 'USD', 'rate': 70.0},
                             {'currency': 'EUR', 'rate': 70.0},
                             {'currency': 'RUB', 'rate': 70.0}]


def test_get_stock_currency():
    """
    Test for get_stock_currency function.
    """
    with patch("yfinance.Ticker") as MockTicker:
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = DataFrame({"High": [200]})
        MockTicker.return_value = mock_ticker_instance

        stock_data = get_stock_currency()
        assert stock_data == [
            {'stock': 'AAPL', 'price': 200.0},
            {'stock': 'AMZN', 'price': 200.0},
            {'stock': 'GOOGL', 'price': 200.0},
            {'stock': 'MSFT', 'price': 200.0},
            {'stock': 'TSLA', 'price': 200.0}
        ]


def test_get_data(sample_dataframe: DataFrame):
    """
    Test for get_data function.
    """
    result = get_data(sample_dataframe)
    assert isinstance(result, dict)
    assert 'greeting' in result
    assert 'cards' in result
    assert 'top_transactions' in result
    assert 'currency_rates' in result
    assert 'stock_prices' in result
    assert isinstance(result['greeting'], str)
    assert isinstance(result['cards'], list)
    assert isinstance(result['top_transactions'], list)
    assert isinstance(result['currency_rates'], list)
    assert isinstance(result['stock_prices'], list)


def test_read_xls_file():
    """
    Test for read_xls_file function.
    """
    df = read_xls_file("data/operations.xlsx")
    assert isinstance(df, DataFrame)


if __name__ == "__main__":
    pytest.main()
