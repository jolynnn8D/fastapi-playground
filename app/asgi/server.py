import asyncio
import socket

from app.asgi.handler import ConnectionHandler


class Server:
    def __init__(self, app, host, port):
        self.app = app
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setblocking(False)
        self.server_socket.bind((self.host, self.port))

    async def listen_for_connections(self, loop):
        self.server_socket.listen()
        print(f"Listening on {self.host, self.port}")
        while True:
            connection, address = await loop.sock_accept(self.server_socket)
            # connection.setblocking(False)
            print(f"{address} connected")
            connection_handler = ConnectionHandler(self.app, connection, loop)
            asyncio.create_task(connection_handler.handle_connection())

    async def start(self):
        loop = asyncio.get_event_loop()
        await self.listen_for_connections(loop)
