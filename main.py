"""
Стартовый модуль приложения Finance Tracker v2

Отвечает за:
- CLI-интерфейс
- обработку пользовательского ввода
- вызов методов FinanceManager
"""

from pathlib import Path
from datetime import datetime

from app.manager import TransactionManager
from app.transaction import Transaction

manager = TransactionManager()

DATA_FILE = Path('data/data.json')

if DATA_FILE.exists():
    manager.load_from_file(DATA_FILE)

def get_input(prompt: str, validator_message='Некорректное значение', type_data=int, validator=None):
    """Универсальная функция для получения и проверки пользовательского ввода."""
    while True:
        try:
            value = type_data(input(prompt))

            if validator and not validator(value):
                print(validator_message)
                continue
            
            return value

        except ValueError:
            print("Ошибка ввода. Попробуйте снова.")

def validate_date(date: str) -> bool:
    """Проверяет корректность даты в формате YYYY-MM-DD."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def create_transaction() -> Transaction:
    """Создает объект Transaction с полной валидацией данных."""
    amount = get_input("Сумма транзакции: ", "Сумма должна быть больше 0", float, lambda x: x > 0)
    type_ = get_input("Тип операции (income/expense): ", "Только income/expense", str, lambda x: x.lower() in ("income", "expense")).lower()
    date = get_input("Дата (YYYY-MM-DD): ", "Формат должен быть YYYY-MM-DD", str, validate_date)
    category = get_input("Категория: ", "Категория не может быть пустой", str, lambda x: x.strip() != "")
    description = get_input("Описание: ", "Описание не может быть пустым", str, lambda x: x.strip() != "")
    return Transaction(amount, type_, date, category, description)

def add_transaction() -> None:
    """Добавляет новую транзакцию."""
    manager.add_transaction(create_transaction())
    print("\nТранзакция добавлена!\n")

def print_transactions(transactions=None) -> bool:
    """Выводит список транзакций. Если список не передан — выводит все транзакции."""

    if transactions is None:
        transactions = manager.get_all_transactions()
    if not transactions:
        return False
    
    print("\nСписок транзакций:\n")

    for index, transaction in enumerate(transactions, 1):
        print(f"{index}. {transaction}")
    
    print()
    return True

def print_balance() -> None:
    """Показывает текущий баланс."""
    print(f"\nТекущий баланс: {manager.get_balance():.2f}\n")

def delete_transaction() -> None:
    """Удаляет транзакцию по номеру."""
    if not print_transactions():
        print("\nТранзакций нет.\n")
        return

    while True:
        index = get_input("Выберите транзакцию для удаления: ", type_data=int)

        try:
            manager.delete_transaction(index - 1)
        except IndexError:
            print("Транзакции с таким номером не существует.")
            continue
        
        print("\nТранзакция успешно удалена.\n")
        return

def update_transaction() -> None:
    """Редактирует существующую транзакцию."""
    if not print_transactions():
        print("\nТранзакций нет.\n")
        return

    while True:
        index = get_input("Выберите транзакцию для редактирования: ", type_data=int)

        all_transactions = manager.get_all_transactions()
        try:
            _ = all_transactions[index - 1]
        except IndexError:
            print("Транзакции с таким номером не существует.")
            continue

        new_transaction = create_transaction()
        manager.update_transaction(index - 1, new_transaction)       
        print("\nТранзакция успешно обновлена.\n")
        return
    
# =========================
# ФИЛЬТРАЦИЯ
# =========================

def filter_by_type() -> None:
    """Фильтрация транзакций по типу."""
    type_ = get_input("Тип операции (income/expense): ", "Только income/expense", str, lambda x: x.lower() in ("income", "expense")).lower()
    filtered = manager.filter_by_type(type_)
    if not filtered:
        print("\nТранзакции не найдены.\n")
        return
    print(f"\nНайдено транзакций: {len(filtered)}")
    print_transactions(filtered)

def filter_by_category() -> None:
    """Фильтрация транзакций по категории."""
    category = get_input("Категория: ", "Категория не может быть пустой", str, lambda x: x.strip() != "")
    filtered = manager.filter_by_category(category)
    if not filtered:
        print("\nТранзакции не найдены.\n")
        return
    print(f"\nНайдено транзакций: {len(filtered)}")
    print_transactions(filtered)

def filter_by_amount_greater() -> None:
    """Фильтрация транзакций по сумме больше указанной."""
    amount = get_input("Сумма: ", "Сумма должна быть больше 0", float, lambda x: x > 0)
    filtered = manager.filter_by_amount_greater(amount)
    if not filtered:
        print("\nТранзакции не найдены.\n")
        return
    print(f"\nНайдено транзакций: {len(filtered)}")
    print_transactions(filtered)

def filter_by_amount_range() -> None:
    """Фильтрация транзакций по диапазону суммы."""
    while True:
        min_amount = get_input("Минимальная сумма: ", "Сумма должна быть больше 0", float, lambda x: x > 0)
        max_amount = get_input("Максимальная сумма: ", "Сумма должна быть больше 0", float, lambda x: x > 0)
        if min_amount > max_amount:
            print('Минимальное значение не может быть больше максимального')
            continue
        break
    
    filtered = manager.filter_by_amount_range(min_amount, max_amount)
    if not filtered:
        print("\nТранзакции не найдены.\n")
        return
    print(f"\nНайдено транзакций: {len(filtered)}")
    print_transactions(filtered)

def filter_by_date_range() -> None:
    """Фильтрация транзакций по диапазону дат."""
    while True:
        start_date = get_input("Начальная дата (YYYY-MM-DD): ", "Формат должен быть YYYY-MM-DD", str, validate_date)
        end_date = get_input("Конечная дата (YYYY-MM-DD): ", "Формат должен быть YYYY-MM-DD", str, validate_date)
        datetime_start_date = datetime.strptime(start_date, '%Y-%m-%d')
        datetime_end_date = datetime.strptime(end_date, '%Y-%m-%d')
        if datetime_start_date > datetime_end_date:
            print("Начальная дата не может быть больше конечной.")
            continue
        break

    filtered = manager.filter_by_date_range(datetime_start_date, datetime_end_date)
    if not filtered:
        print("\nТранзакции не найдены.\n")
        return
    print(f"\nНайдено транзакций: {len(filtered)}")
    print_transactions(filtered)

# =========================
# СОРТИРОВКА
# =========================

def sort_by_amount() -> None:
    """Сортировка транзакций по сумме."""
    choice = get_input("1 - по возрастанию, 2 - по убыванию: ", "Только 1 или 2", int, lambda x: x in (1, 2))
    reverse = choice == 2
    sorted_transactions = manager.sort_by_amount(reverse)
    print_transactions(sorted_transactions)

def sort_by_date() -> None:
    """Сортировка транзакций по дате."""
    choice = get_input("1 - по возрастанию, 2 - по убыванию: ", "Только 1 или 2", int, lambda x: x in (1, 2))
    reverse = choice == 2
    sorted_transactions = manager.sort_by_date(reverse)
    print_transactions(sorted_transactions)

# =========================
# СТАТИСТИКА
# =========================

def statistics_by_income() -> None:
    """Показывает общую сумму доходов."""
    print(f"\nОбщий доход: {manager.get_total_income():.2f}\n")

def statistics_by_expense() -> None:
    """Показывает общую сумму расходов."""
    print(f"\nОбщий расход: {manager.get_total_expense():.2f}\n")

def max_transaction() -> None:
    """Показывает транзакцию с максимальной суммой."""
    transaction = manager.get_max_transaction()

    if transaction is None:
        print("\nТранзакций нет.\n")
        return

    print(f"\nМаксимальная транзакция:\n{transaction}\n")

def count_transaction() -> None:
    """Показывает количество всех транзакций"""
    print(f"\nКоличество транзакций: {manager.get_transactions_count()}\n")

def save_to_csv() -> None:
    """Экспортирует транзакции в CSV-файл."""
    filename = get_input("Название файла: ", "Название не может быть пустым", str, lambda x: x.strip() != "")

    if not filename.endswith('.csv'):
        filename += '.csv'

    csv_path = Path("data") / filename
    
    manager.save_to_csv(csv_path)

    print(f"\nCSV-файл сохранен: {csv_path}\n")

# =========================
# МЕНЮ СТАТИСТИКИ
# =========================

def statistics_menu():
    """Вложенное меню статистики."""
    menu = {
        1: ('Общий доход', statistics_by_income),
        2: ('Общий расход', statistics_by_expense),
        3: ('Баланс', print_balance),
        4: ('Максимальная транзакция', max_transaction),
        5: ('Количество транзакций', count_transaction),
        0: ('Назад', None),
    }

    while True:

        print("\n===== СТАТИСТИКА =====\n")

        for i, item in menu.items():
            print(f"{i}. {item[0]}")

        choice = get_input("\nВыберите пункт меню: ", type_data=int)
        if choice in menu:
            text, action = menu[choice]
            print(f"\nВы выбрали: {text}\n")

            if choice == 0:
                break
            if action:
                action()
            
        else:
            print("\nТакого пункта меню не существует.\n")


# =========================
# МЕНЮ ФИЛЬТРОВ
# =========================

def filters_menu():
    """ Вложенное меню фильтрации транзакций."""
    menu = {
        1: ('По типу', filter_by_type),
        2: ('По категории', filter_by_category),
        3: ('По сумме больше', filter_by_amount_greater),
        4: ('По диапазону суммы', filter_by_amount_range),
        5: ('По диапазону дат', filter_by_date_range),
        0: ('Назад', None),
    }

    while True:

        print("\n===== ФИЛЬТРЫ =====\n")

        for i, item in menu.items():
            print(f"{i}. {item[0]}")

        choice = get_input("\nВыберите пункт меню: ", type_data=int)
        if choice in menu:
            text, action = menu[choice]
            print(f"\nВы выбрали: {text}\n")

            if choice == 0:
                break
            if action:
                action()
            
        else:
            print("\nТакого пункта меню не существует.\n")
    

# =========================
# ОСНОВНОЕ МЕНЮ
# =========================

menu = {
    1: ('Добавить транзакцию', add_transaction),
    2: ('Показать транзакции', print_transactions),
    3: ('Удалить транзакцию', delete_transaction),
    4: ('Редактировать транзакцию', update_transaction),
    5: ('Сортировка по сумме', sort_by_amount),
    6: ('Сортировка по дате', sort_by_date),
    7: ('Фильтры', filters_menu),
    8: ('Статистика', statistics_menu),
    9: ('Экспорт в CSV', save_to_csv),
    0: ('Выход', None),
}

def main():
    """Точка входа в приложение."""

    print("\nДобро пожаловать в Finance Manager v2\n")

    while True:
        
        print("\n===== ГЛАВНОЕ МЕНЮ =====\n")

        for i, item in menu.items():
            print(f"{i}. {item[0]}")

        choice = get_input("\nВыберите пункт меню: ", type_data=int)
        if choice in menu:
            text, action = menu[choice]
            print(f"\nВы выбрали: {text}\n")

            if choice == 0:
                print("\nДо свидания!\n")
                break
            if action:
                action()
            if choice in (1, 3, 4):
                manager.save_to_file(DATA_FILE)
            
        else:
            print("\nТакого пункта меню не существует.\n")

if __name__ == "__main__":
    main()




