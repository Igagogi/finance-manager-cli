"""
Модуль, описывающий одну финансовую транзакцию.
"""

from datetime import datetime

class Transaction:
    """
    Класс, представляющий одну финансовую транзакцию.

    Attributes:
        amount (float):
            Сумма транзакции.

        type_ (str):
            Тип операции:
            - income
            - expense

        date (datetime):
            Дата транзакции.

        category (str):
            Категория транзакции.

        description (str):
            Описание транзакции.
    """

    def __init__(self, amount: float, type_: str, date: str, category: str, description: str) -> None:
        """Инициализирует объект Transaction с валидацией данных."""

        if amount <= 0:
            raise ValueError("Сумма транзакции должна быть больше 0.")
        self.amount = amount

        self.type_ = type_.lower()
        if self.type_ not in ("income", "expense"):
            raise ValueError("Тип операции должен быть income или expense.")
        
        try:
            self.date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Дата должна быть в формате YYYY-MM-DD.")

        self.category = category.strip()
        if not self.category:
            raise ValueError("Категория не может быть пустой.")
        
        self.description = description.strip()
        if not self.description:
            raise ValueError("Описание не может быть пустым.")

    def __str__(self):
        """Возвращает строковое представление транзакции."""
        return f"[{self.date.strftime('%Y-%m-%d')}]: {self.operation_sign}{self.amount} | ({self.category}) - {self.description}"
    
    @property
    def operation_sign(self) -> str:
        """Возвращает знак операции.: "+" для income, "-" для expense"""
        return "+" if self.type_ == "income" else "-"
    
    @property
    def net_amount(self) -> float:
        """Возвращает сумму с учетом типа операции."""
        return +self.amount if self.type_ == "income" else -self.amount
    
    def to_dict(self) -> dict:
        """Преобразует объект Transaction в словарь."""
        return {
            'amount': self.amount,
            'type': self.type_,
            'date': self.date.strftime('%Y-%m-%d'),
            'category': self.category,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Создает объект Transaction из словаря."""
        return cls(data['amount'], data['type'], data['date'], data['category'], data['description'])