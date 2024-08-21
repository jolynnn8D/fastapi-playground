import asyncio
import socket

import requests


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client_socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

    async def connect(self, loop):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to {self.host}, {self.port}")
        while True:
            msg = input()
            self.client_socket.sendall(msg.encode("utf-8"))
            data = self.client_socket.recv(1024)
            print(f"Received: {data}")

    async def start(self):
        loop = asyncio.get_event_loop()
        await self.http_request(loop)

    async def http_request(self, loop):
        get_data = requests.get(f"http://{self.host}:{self.port}/transactions")
        print(get_data.json())
        while True:
            msg = input()
            try:
                data = requests.post(
                    f"http://{self.host}:{self.port}/echo", json={"msg": msg}
                )
                print(data.json())
            except Exception as e:
                print(e)


if __name__ == "__main__":
    client = Client("127.0.0.1", 8000)
    asyncio.run(client.start())
