import enum

from pydantic import BaseModel, validator


class TransactionType(enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"


class Transaction(BaseModel):
    type: TransactionType
    amount: int

    @validator('amount', pre=True)
    def value_greater_than_zero(cls, amount):
        if amount <= 0:
            raise ValueError('amount must be greater than zero')
        return amount
