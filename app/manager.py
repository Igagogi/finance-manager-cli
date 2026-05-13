"""
Модуль с бизнес-логикой приложения Finance Tracker CLI.
"""

import csv
import json

from pathlib import Path
from datetime import datetime
from typing import Callable

from app.transaction import Transaction


class TransactionManager:
    """
    Класс для управления транзакциями.

    Отвечает за:
    - хранение транзакций
    - добавление и удаление
    - фильтрацию
    - сортировку
    - статистику
    - сохранение и загрузку данных
    """
    def __init__(self) -> None:
        """Инициализирует пустой список транзакций."""
        self.transactions: list[Transaction] = []
    
    # =========================
    # БАЗОВЫЕ ОПЕРАЦИИ
    # =========================

    def add_transaction(self, transaction: Transaction) -> None:
        """Добавляет транзакцию в список."""
        self.transactions.append(transaction)
    
    def get_all_transactions(self) -> list[Transaction]:
        """Возвращает копию списка всех транзакций."""
        return self.transactions.copy()

    def _validate_index(self, index: int) -> None:
        """Проверяет корректность индекса."""
        if not 0 <= index < len(self.transactions):
            raise IndexError("Некорректный индекс транзакции.")

    def delete_transaction(self, index: int) -> None:
        """Удаляет транзакцию по индексу."""
        self._validate_index(index)
        del self.transactions[index]

    def update_transaction(self, index: int, new_transaction: Transaction) -> None:
        """Обновляет транзакцию по индексу."""
        self._validate_index(index)
        self.transactions[index] = new_transaction

    # =========================
    # СТАТИСТИКА
    # =========================

    def get_balance(self) -> float:
        """Возвращает текущий баланс."""
        return sum(trans.net_amount for trans in self.transactions)
    
    def get_total_income(self) -> float:
        """Возвращает общую сумму доходов."""
        return sum(trans.amount for trans in self.transactions if trans.type_ == "income")
    
    def get_total_expense(self) -> float:
        """Возвращает общую сумму расходов."""
        return sum(trans.amount for trans in self.transactions if trans.type_ == "expense")
    
    def get_max_transaction(self) -> Transaction | None:
        """ Возвращает транзакцию с максимальной суммой."""
        if not self.transactions:
            return None
        return max(self.transactions, key=lambda trans: trans.amount)

    def get_transactions_count(self) -> int:
        """Возвращает количество транзакций."""
        return len(self.transactions)
    
    # =========================
    # ФИЛЬТРАЦИЯ
    # =========================
    
    def filter_transactions(self, predicate: Callable[[Transaction], bool]) -> list[Transaction]:
        """Универсальный метод фильтрации."""
        return [trans for trans in self.transactions if predicate(trans)]
    
    def filter_by_type(self, type_: str) -> list[Transaction]:
        """Фильтрует транзакции по типу операции."""
        return self.filter_transactions(lambda t: t.type_ == type_)
    
    def filter_by_amount_greater(self, amount: float) -> list[Transaction]:
        """Фильтрует транзакции с суммой больше указанной."""
        return self.filter_transactions(lambda t: t.amount > amount)
    
    def filter_by_amount_range(self, min_amount: float, max_amount: float) -> list[Transaction]:
        """Фильтрует транзакции по диапазону суммы."""
        if min_amount > max_amount:
            raise ValueError("Минимальная сумма не может быть больше максимальной.")
        return self.filter_transactions(lambda t: min_amount <= t.amount <= max_amount)
    
    def filter_by_category(self, category: str) -> list[Transaction]:
        """Фильтрует транзакции по категории."""
        return self.filter_transactions(lambda t: t.category == category)
    
    def filter_by_date_range(self, start_date: datetime, end_date: datetime) -> list[Transaction]:
        """Фильтрует транзакции по диапазону дат."""
        if start_date > end_date:
            raise ValueError("Начальная дата не может быть больше конечной")
        return self.filter_transactions(lambda t: start_date <= t.date <= end_date)
    
    # =========================
    # СОРТИРОВКА
    # =========================

    def sort_by_amount(self, reverse: bool = False) -> list[Transaction]:
        """Сортирует транзакции по сумме."""
        return sorted(self.transactions, key=lambda t: t.amount, reverse=reverse)

    def sort_by_date(self, reverse: bool = False) -> list[Transaction]:
        """Сортирует транзакции по дате."""
        return sorted(self.transactions, key=lambda t: t.date, reverse=reverse)

    # =========================
    # РАБОТА С ФАЙЛАМИ
    # =========================

    def save_to_file(self, filename: Path) -> None:
        """Сохраняет транзакции в JSON-файл."""
        data = [trans.to_dict() for trans in self.transactions]
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
    def load_from_file(self, filename: Path) -> None:
        """Загружает транзакции из JSON-файла."""
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.transactions = [Transaction.from_dict(trans) for trans in data]

    def save_to_csv(self, filename: Path) -> None:
        """Экспортирует транзакции в CSV-файл."""
        with open(filename, 'w', newline='', encoding='utf-8') as file:

            fieldnames = ['amount', 'type', 'date', 'category', 'description']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for trans in self.transactions:
                writer.writerow(trans.to_dict())






