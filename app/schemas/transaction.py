import uuid

from pydantic import BaseModel


class BaseTransaction(BaseModel):
    amount: float
    category: str
    description: str | None = None
    tags: set[str] = set()


class Transaction(BaseTransaction):
    id: uuid.UUID


class TransactionUpdate(BaseTransaction):
    amount: float | None = None
    category: str | None = None
