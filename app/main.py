import uuid
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path, Query, WebSocket, status
from fastapi.responses import HTMLResponse

from app.routers.common import PaginationParams, Tags
from app.schemas.echo import EchoInput
from app.schemas.transaction import Transaction, TransactionUpdate

app = FastAPI()

transaction_db = {
    "1": Transaction(id=uuid.uuid4(), amount=10.1, category="Food", description="Test")
}

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def root():
    return HTMLResponse(html)


@app.post("/echo")
async def echo(input: EchoInput):
    return {"message": f"Your message was {input.msg}"}


@app.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(
    transaction_id: Annotated[str, Path(title="ID of the transaction")],
):
    if transaction_id not in transaction_db:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction_db[transaction_id]


@app.get("/transactions/", response_model=list[Transaction])
async def list_transactions(
    pagination: Annotated[PaginationParams, Depends()],
    category: Annotated[str | None, Query()] = None,
):
    return list(transaction_db.values())[
        pagination.page * pagination.limit : (pagination.page + 1) * pagination.limit
    ]


@app.post(
    "/transactions/",
    status_code=status.HTTP_201_CREATED,
    response_model=Transaction,
    tags=[Tags.transactions],
)
async def create_transaction(transaction: Transaction):
    transaction_db[str(uuid.uuid4())] = transaction
    return transaction


@app.put("/transactions/{transaction_id}")
async def update_transaction(transaction_id: str, transaction: Transaction):
    if transaction:
        transaction_db[transaction_id] = transaction
    return {"message": "Transaction updated successfully"}


@app.patch("/transactions/{transaction_id}", response_model=Transaction)
async def patch_transaction(transaction_id: str, transaction: TransactionUpdate):
    if transaction_id not in transaction_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    original_transaction = transaction_db[transaction_id]
    update_data = transaction.model_dump(exclude_unset=True)
    updated_transaction = original_transaction.model_copy(update=update_data)
    transaction_db[transaction_id] = updated_transaction
    return updated_transaction


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
