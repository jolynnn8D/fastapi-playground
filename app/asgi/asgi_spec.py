import asyncio

from app.asgi.http_parser import HttpParser


class AsgiSpec:
    def __init__(self, parser: HttpParser):
        self.scope: dict = {
            "asgi": {"version": "3.0", "spec_version": "2.0"},
            "method": parser.req["method"].decode(),
            "type": parser.req["type"].decode().lower(),
            "http_version": parser.req["http_version"].decode(),
            "path": parser.req["path"].decode(),
            "headers": parser.req["headers"],
            "query_string": b"",
        }
        self.parser = parser
        self.response = []
        self.response_event = asyncio.Event()

    async def run(self, app):
        await app(self.scope, self.receive, self.send)

    async def send(self, message):
        self.response.append(message)
        if message.get("type") == "http.response.body":
            self.response_event.set()

    async def receive(self):
        message = {
            "type": "http.request",
            "body": self.parser.req["body"],
            "more_body": False,
        }
        return message
