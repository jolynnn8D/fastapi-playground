import uuid
from typing import Annotated

from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI()

transaction_db = {
    "1": {"transaction_id": "1", "amount": 100, "description": "test"},
    "2": {"transaction_id": "2", "amount": 200, "description": "test2"},
}


class Transaction(BaseModel):
    amount: int
    description: str | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/transactions/{transaction_id}")
async def get_transaction(
    transaction_id: Annotated[str, Path(title="ID of the transaction")],
    is_valid: bool = True,
    query_param: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Some query string",
            min_length=5,
            alias="fancy-query",
            deprecated=True,  # shows deprecated in docs
            include_in_schema=False,  # removes field from docs
        ),
    ] = None,
):
    if not is_valid:
        return {"error": "Invalid transaction_id"}
    if query_param:
        return {"transaction_id": transaction_id, "query_param": query_param}
    if transaction_id in transaction_db:
        return transaction_db[transaction_id]
    return {"transaction_id": transaction_id}


@app.get("/transactions/")
async def list_transactions(page: int = 0, limit: int = 10):
    return list(transaction_db.values())[page * limit : (page + 1) * limit]


@app.post("/transactions/")
async def create_transaction(transaction: Transaction):
    transaction_db[str(uuid.uuid4())] = transaction.model_dump()
    return {"message": "Transaction created successfully"}


@app.put("/transactions/{transaction_id}")
async def update_transaction(transaction_id: str, transaction: Transaction):
    if transaction:
        transaction_db[transaction_id] = transaction.model_dump()
    return {"message": "Transaction updated successfully"}
