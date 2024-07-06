import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import requests
import yfinance as yf
from dotenv import load_dotenv
from pandas import DataFrame

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
API_KEY = os.getenv("API_KEY")

current_dir = os.path.dirname(__file__)
settings_file = os.path.join(current_dir, '..', 'user_settings.json')
settings_file = os.path.abspath(settings_file)


def get_time_of_day(hour: Any = None) -> str:
    """
    Returns a greeting message based on the current time of the day.
    """
    if hour is None:
        hour = datetime.now()
    else:
        hour = datetime.strptime(hour, "%Y-%m-%d %H:%M:%S")

    hour = hour.hour

    if 5 <= hour < 12:
        return "Доброе утро!"
    elif 12 <= hour < 18:
        return "Добрый день!"
    elif 18 <= hour < 21:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


def get_card_data(df: DataFrame) -> List[Dict[str, str]]:
    """
    Extracts and processes card transaction data from a DataFrame.

    Parameters:
        df (DataFrame): Input DataFrame containing transaction data.

    Returns:
        List[Dict[str, str]]: List of dictionaries with card data.
    """
    logger.info("Extracting card data...")
    df['Номер карты'] = df['Номер карты'].fillna('Unknown')
    df_total_spend = df[df['Сумма операции'] < 0].groupby('Номер карты').agg({
        'Сумма операции': 'sum',
        'Кэшбэк': 'sum'
    }).reset_index()

    return [
        {
            "last_digits": row["Номер карты"],
            "total_spent": row["Сумма операции"],
            "cashback": row["Кэшбэк"]
        }
        for idx, row in df_total_spend.iterrows()
    ]


def top_transaction(df: DataFrame) -> List[Dict[str, str]]:
    """
    Extracts top transaction details from a DataFrame.

    Parameters:
        df (DataFrame): Input DataFrame containing transaction data.

    Returns:
        List[Dict[str, str]]: List of dictionaries with top transaction details.
    """
    logger.info("Extracting top transactions...")
    df_top = df.nlargest(5, 'Сумма операции')

    return [
        {
            "date": row["Дата платежа"],
            "amount": row["Сумма платежа"],
            "category": row["Категория"],
            "description": row["Описание"]
        }
        for idx, row in df_top.iterrows()
    ]


def get_currency() -> List[Dict[str, str]]:
    """
    Retrieves currency exchange rates based on user settings.

    Returns:
        List[Dict[str, str]]: List of dictionaries with currency rates.
    """
    logger.info("Retrieving currency rates...")
    lst = []
    with open(settings_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    for currency in data["user_currencies"]:
        url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
        try:
            response = requests.get(url, headers={'apikey': API_KEY})
            response.raise_for_status()
            response_data = response.json()
            rate = response_data["rates"]["RUB"]
            lst.append({
                "currency": currency,
                "rate": rate
            })
        except requests.RequestException as e:
            logger.error(f"Failed to retrieve currency data for {currency}: {e}")
            continue

    return lst


def get_stock_currency() -> List[Dict[str, float]]:
    """
    Retrieves stock prices based on user settings.

    Returns:
        List[Dict[str, float]]: List of dictionaries with stock prices.
    """
    logger.info("Retrieving stock prices...")
    lst = []
    with open(settings_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    for stock in data["user_stocks"]:
        ticker = yf.Ticker(stock)
        try:
            data_tod = ticker.history(period="1d")
            price = float(data_tod["High"].iloc[0]) if not data_tod.empty else 0.0
            lst.append({
                "stock": stock,
                "price": price
            })
        except Exception as e:
            logger.error(f"Failed to retrieve stock price data for {stock}: {e}")
            continue

    return lst


def get_data(df: DataFrame) -> Dict[str, object]:
    """
    Retrieves all necessary data for the dashboard.

    Returns:
        Dict[str, object]: Dictionary with various data components.
    """
    logger.info("Getting data for the dashboard...")
    result = json.dumps({
        "greeting": get_time_of_day(),
        "cards": get_card_data(df),
        "top_transactions": top_transaction(df),
        "currency_rates": get_currency(),
        "stock_prices": get_stock_currency()
    }, ensure_ascii=False, indent=4)

    return result
