from enum import Enum


class Tags(Enum):
    transactions = "transactions"


class PaginationParams:
    def __init__(self, page: int = 0, limit: int = 10):
        self.page = page
        self.limit = limit
