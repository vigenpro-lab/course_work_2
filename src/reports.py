import datetime
import functools
import json
import logging
from typing import Any, Callable, Optional

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def write_report(file_name: Optional[str] = None) -> Callable:
    """
    A decorator that writes the result of the decorated function to a JSON file.

    Args:
        file_name (Optional[str]): The name of the output file. If not provided, a timestamped name is generated.

    Returns:
        Callable: The decorated function.
    """
    def decorator_write_report(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper_write_report(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            output_file = file_name or (f"/Users/vigenkarapetan/PycharmProjects/cours_work_2/cours_work_2/src/reports"
                                        f"/report_"
                                        f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            logging.info(f"Writing report to {output_file}")
            with open(output_file, 'w') as f:
                json.dump(result.to_dict(orient='records'), f, ensure_ascii=False, indent=4)
            return result
        return wrapper_write_report
    return decorator_write_report if file_name is None else decorator_write_report(file_name)


@write_report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Filters transactions by category and date range.

    Args:
        transactions (pd.DataFrame): The DataFrame containing transaction data.
        category (str): The category to filter by.
        date (Optional[str]): The end date in the format 'dd.mm.yyyy'. Defaults to today if not provided.

    Returns:
        pd.DataFrame: The filtered transactions.
    """
    logging.info(f"Filtering transactions for category '{category}' up to date '{date}'")

    if date is None:
        end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.strptime(date, '%d.%m.%Y')

    start_date = end_date - pd.DateOffset(months=3)

    logging.info(f"Filtering transactions from {start_date.strftime('%d.%m.%Y')} to {end_date.strftime('%d.%m.%Y')}")

    filtered_transactions = transactions[
        (transactions['Категория'] == category) & (pd.to_datetime(transactions['Дата операции'],
                                                                  format='%d.%m.%Y %H:%M:%S') >= start_date)
        & (pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S') <= end_date)
    ]

    return filtered_transactions
