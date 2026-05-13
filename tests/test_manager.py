"""
Тесты для модуля manager.py.
"""

from app.transaction import Transaction
from app.manager import TransactionManager


def test_add_transaction():
    """Проверяет добавление транзакции в менеджер."""
    manager = TransactionManager()
    transaction = Transaction(1000, 'income', '2025-05-12', 'Salary', 'May salary')
    manager.add_transaction(transaction)

    assert len(manager.transactions) == 1
    assert manager.transactions[0] == transaction

def test_get_balance():
    """Проверяет корректный расчет баланса."""
    manager = TransactionManager()
    income_transaction = Transaction(1000, 'income', '2026-05-11', 'Зарплата', 'Оплата за день')
    expense_transaction = Transaction(500, 'expense', '2026-02-10', 'Еда', 'Расход')

    manager.add_transaction(income_transaction)
    manager.add_transaction(expense_transaction)

    assert manager.get_balance() == 500

def test_delete_transaction():
    """Проверяет удаление транзакции."""
    manager = TransactionManager()
    first_transaction = Transaction(1000, 'income', '2026-05-11', 'Зарплата', 'Оплата за день')
    second_transaction = Transaction(500, 'expense', '2026-02-10', 'Еда', 'Расход')

    manager.add_transaction(first_transaction)
    manager.add_transaction(second_transaction)

    manager.delete_transaction(0)

    assert len(manager.transactions) == 1
    assert manager.transactions[0] == second_transaction

def test_filter_by_type():
    """Проверяет фильтрацию транзакций по типу."""
    manager = TransactionManager()
    income_transaction = Transaction(1000, 'income', '2026-05-11', 'Зарплата', 'Оплата за день')
    expense_transaction_1 = Transaction(500, 'expense', '2026-02-10', 'Еда', 'Расход')
    expense_transaction_2 = Transaction(300, 'expense', '2026-05-10', 'Еда', 'Расход')

    manager.add_transaction(income_transaction)
    manager.add_transaction(expense_transaction_1)
    manager.add_transaction(expense_transaction_2)

    filtered = manager.filter_by_type('expense')

    assert len(filtered) == 2
    assert expense_transaction_1 in filtered
    assert expense_transaction_2 in filtered
    assert income_transaction not in filtered