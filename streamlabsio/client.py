import logging
import pprint
from pathlib import Path

import socketio
from observable import Observable

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from .models import as_dataclass

pp = pprint.PrettyPrinter(indent=4)


class Client:
    logger = logging.getLogger("socketio.socketio")

    def __init__(self, token=None):
        self.token = token or self._token_from_toml()
        self.sio = socketio.Client()
        self.sio.on("connect", self.connect_handler)
        self.sio.on("event", self.event_handler)
        self.sio.on("disconnect", self.disconnect_handler)
        self.obs = Observable()

    def __enter__(self):
        self.sio.connect(f"https://sockets.streamlabs.com?token={self.token}")
        return self

    def _token_from_toml(self) -> str:
        filepath = Path.cwd() / "config.toml"
        with open(filepath, "rb") as f:
            conn = tomllib.load(f)
            assert "token" in conn.get("streamlabs")
        return conn["streamlabs"].get("token")

    def connect_handler(self):
        self.logger.info("Connected to Twitch Socketio")

    def event_handler(self, data):
        self.obs.trigger(
            data.get("for"),
            data["type"],
            as_dataclass(data["type"], *data["message"]),
        )

    def disconnect_handler(self):
        self.logger.info("Disconnected from Twitch Socketio")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sio.disconnect()


def connect(**kwargs):
    SIO_cls = Client
    return SIO_cls(**kwargs)
