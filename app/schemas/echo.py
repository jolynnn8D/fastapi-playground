from pydantic import BaseModel


class EchoInput(BaseModel):
    msg: str
