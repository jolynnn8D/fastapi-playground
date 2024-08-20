from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

transaction_db = [{"transaction_id": "1", "amount": 100, "description": "test"}, {"transaction_id": "2", "amount": 200, "description": "test2"}]

class Transaction(BaseModel):
    amount: int
    description: str | None = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/transactions/{transaction_id}")
async def get_transaction(transaction_id: str, is_valid: bool = True, query_param: Annotated[str | None, Query(min_length=5)] = None):
    if not is_valid:
        return {"error": "Invalid transaction_id"}
    if query_param:
        return {"transaction_id": transaction_id, "query_param": query_param}
    return {"transaction_id": transaction_id}

@app.get("/transactions/")
async def list_transactions(page: int = 0, limit: int = 10):
    return transaction_db[page * limit: (page + 1) * limit]

@app.post("/transactions/")
async def create_transaction(transaction: Transaction):
    transaction_db.append(transaction.model_dump())
    return {"message": "Transaction created successfully"}