import logging
from pathlib import Path

import socketio
from observable import Observable

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from .models import as_dataclass


class Client:
    logger = logging.getLogger("socketio.client")

    def __init__(self, token=None):
        self.token = token or self._token_from_toml()
        self.sio = socketio.Client()
        self.sio.on("connect", self.connect_handler)
        self.sio.on("event", self.event_handler)
        self.sio.on("disconnect", self.disconnect_handler)
        self.obs = Observable()
        self.streamlabs = ("donation",)
        self.twitch = ("follow", "subscription", "host", "bits", "raids")
        self.youtube = ("follow", "subscription", "superchat")

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
        self.logger.info("Connected to Streamlabs Socket API")

    def event_handler(self, data):
        if "for" in data and data["type"] in set(
            self.streamlabs + self.twitch + self.youtube
        ):
            self.obs.trigger(
                data["for"],
                data["type"],
                as_dataclass(data["type"], *data["message"]),
            )

    def disconnect_handler(self):
        self.logger.info("Disconnected from Streamlabs Socket API")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sio.disconnect()


def connect(**kwargs):
    SIO_cls = Client
    return SIO_cls(**kwargs)
