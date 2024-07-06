import json

from src.reports import spending_by_category
from src.services import search_by_request
from src.utils import convert_data_frame_to_json, read_xls_file
from src.views import get_data


def main() -> None:
    """
    The main function that reads transaction data, processes it, and prints the results.
    """
    df = read_xls_file("../data/operations.xlsx")
    data = get_data(df)

    print("Главная страница:")
    print(data)
    print()

    search_query = input("Введи запрос для поиска по транзакциям: ")
    search_result = search_by_request(search_query, convert_data_frame_to_json(df))

    print("Поиск по запросу:")
    print(search_result)
    print()

    category = input("Введите название категории: ")
    category_spending = spending_by_category(df, category).to_dict(orient='records')

    print("Траты по категории:")
    print(json.dumps(category_spending, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
