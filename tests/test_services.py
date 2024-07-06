from typing import Generator
from unittest.mock import Mock, patch

import pytest

from src.services import search_by_request


@pytest.fixture
def mock_convert_data_frame_to_json() -> Generator[Mock, None, None]:
    """
    Fixture to mock the convert_data_frame_to_json function.

    Yields:
        Mock: A mock object for convert_data_frame_to_json.
    """
    with patch('src.services.convert_data_frame_to_json') as mock_convert:
        yield mock_convert


@pytest.fixture
def mock_read_xls_file() -> Generator[Mock, None, None]:
    """
    Fixture to mock the read_xls_file function.

    Yields:
        Mock: A mock object for read_xls_file.
    """
    with patch('src.services.read_xls_file') as mock_read:
        yield mock_read


def test_search_by_request_match(mock_convert_data_frame_to_json: Mock, mock_read_xls_file: Mock) -> None:
    """
    Test the search_by_request function when there is a match for the search text.

    Args:
        mock_convert_data_frame_to_json (Mock): Mock for convert_data_frame_to_json.
        mock_read_xls_file (Mock): Mock for read_xls_file.
    """
    mock_convert_data_frame_to_json.return_value = '{"operations": [{"Категория": "Test", "Описание": "Test description"}]}'
    mock_read_xls_file.return_value = Mock()

    search_text = "Test"
    operations_json = '[{"Категория": "Test", "Описание": "Test description"}]'

    result = search_by_request(search_text, operations_json)

    assert len(result) == 502


def test_search_by_request_no_match(mock_convert_data_frame_to_json: Mock, mock_read_xls_file: Mock) -> None:
    """
    Test the search_by_request function when there is no match for the search text.

    Args:
        mock_convert_data_frame_to_json (Mock): Mock for convert_data_frame_to_json.
        mock_read_xls_file (Mock): Mock for read_xls_file.
    """
    mock_convert_data_frame_to_json.return_value = '{"operations": [{"Категория": "Test", "Описание": "Test description"}]}'
    mock_read_xls_file.return_value = Mock()

    search_text = "Nonexistent"
    operations_json = '[{"Категория": "Test", "Описание": "Test description"}]'

    result = search_by_request(search_text, operations_json)

    assert len(result) == 2
