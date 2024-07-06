import json
import logging
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def search_by_request(search_text: str, operations_json: str) -> str:
    """
    Search for operations containing the specified text in the category or description fields.

    Args:
        search_text (str): The text to search for.
        operations_json (str): The JSON string representing the operations data.

    Returns:
        str: A JSON string containing the filtered operations.
    """
    logging.info("Loading operations data from JSON")
    operations: List[Dict[str, Any]] = json.loads(operations_json)

    logging.info("Searching for text '%s' in operations", search_text)
    filtered_operations: List[Dict[str, Any]] = []
    for operation in operations:
        category = str(operation.get("Категория", ""))
        description = str(operation.get("Описание", ""))
        if search_text.lower() in category.lower() or search_text.lower() in description.lower():
            filtered_operations.append({
                "Дата операции": operation.get("Дата операции"),
                "Дата платежа": operation.get("Дата платежа"),
                "Номер карты": operation.get("Номер карты"),
                "Статус": operation.get("Статус"),
                "Сумма операции": operation.get("Сумма операции"),
                "Валюта операции": operation.get("Валюта операции"),
                "Сумма платежа": operation.get("Сумма платежа"),
                "Валюта платежа": operation.get("Валюта платежа"),
                "Кэшбэк": operation.get("Кэшбэк"),
                "Категория": operation.get("Категория"),
                "MCC": operation.get("MCC"),
                "Описание": operation.get("Описание"),
                "Бонусы (включая кэшбэк)": operation.get("Бонусы (включая кэшбэк)"),
                "Округление на инвесткопилку": operation.get("Округление на инвесткопилку"),
                "Сумма операции с округлением": operation.get("Сумма операции с округлением")
            })

    logging.info("Found %d matching operations", len(filtered_operations))
    return json.dumps(filtered_operations, ensure_ascii=False, indent=4)
