import asyncio
import importlib
import sys

from app.asgi.server import Server


class NoAppFoundError(Exception):
    pass


def get_from_str(input_str):
    module_str, attrs_str = input_str.split(":")
    try:
        module = importlib.import_module(module_str)
        app = getattr(module, attrs_str)
        return app
    except ModuleNotFoundError as e:
        raise NoAppFoundError(e)


def main():
    app = get_from_str(sys.argv[1])
    server = Server(app, "127.0.0.1", 8000)
    asyncio.run(server.start())
