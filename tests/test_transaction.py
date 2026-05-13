"""
Тесты для модуля transaction.py.
"""

import pytest
from app.transaction import Transaction


def test_transaction_creation():
    """Проверяет корректное создание объекта Transaction."""
    transaction = Transaction(1000, 'income', '2026-05-12', 'Зарплата', 'Оплата за день')
    
    assert transaction.amount == 1000
    assert transaction.type_ == 'income'
    assert transaction.category == 'Зарплата'
    assert transaction.description == 'Оплата за день'
    assert transaction.date.strftime('%Y-%m-%d') == '2026-05-12'

def test_invalid_amount():
    """Проверяет ошибку при отрицательной сумме."""
    with pytest.raises(ValueError, match="Сумма транзакции должна быть больше 0."): 
        transaction = Transaction(-1000, 'income', '2026-05-12', 'Зарплата', 'Оплата за день')

def test_operation_sign():
    """Проверяет корректный знак операции '+' или '-'."""
    income_transaction = Transaction(1000, 'income', '2026-05-11', 'Зарплата', 'Оплата за день')
    expense_transaction = Transaction(500, 'expense', '2026-02-10', 'Еда', 'Расход')

    assert income_transaction.operation_sign == '+'
    assert expense_transaction.operation_sign == '-'

def test_net_amount():
    """Проверяет корректный расчет суммы с учетом типа операции."""
    income_transaction = Transaction(1000, 'income', '2026-05-11', 'Зарплата', 'Оплата за день')
    expense_transaction = Transaction(500, 'expense', '2026-02-10', 'Еда', 'Расход')

    assert income_transaction.net_amount == 1000
    assert expense_transaction.net_amount == -500

