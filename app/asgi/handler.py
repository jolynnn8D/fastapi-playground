import asyncio

from app.asgi.asgi_spec import AsgiSpec
from app.asgi.http_parser import HttpParser


class ConnectionHandler:
    def __init__(self, app, connection, loop):
        self.app = app
        self.connection = connection
        self.loop = loop
        self.parser = HttpParser()

    async def handle_connection(self):
        try:
            data = await self.loop.sock_recv(self.connection, 1024)
            self.parser.parse_req(data)
            print(self.parser.req)
            asgi_spec = AsgiSpec(self.parser)
            asyncio.create_task(asgi_spec.run(self.app))
            await asgi_spec.response_event.wait()
            http_response = self.parser.serialize_http_response(asgi_spec.response)
            await self.loop.sock_sendall(self.connection, http_response)

        except Exception as e:
            print(e)
        finally:
            self.connection.close()
