import logging
from pathlib import Path
from typing import Optional

import socketio
from observable import Observable

from .error import SteamlabsSIOConnectionError
from .models import as_dataclass

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, token=None, raw=False):
        self.logger = logger.getChild(self.__class__.__name__)
        self.token = token or self._token_from_toml()
        self._raw = raw
        self.sio = socketio.Client()
        self.sio.on("connect", self.connect_handler)
        self.sio.on("event", self.event_handler)
        self.sio.on("disconnect", self.disconnect_handler)
        self.obs = Observable()
        self.streamlabs = ("donation",)
        self.twitch = ("follow", "subscription", "host", "bits", "raids")
        self.youtube = ("follow", "subscription", "superchat")

    def __enter__(self):
        try:
            self.sio.connect(f"https://sockets.streamlabs.com?token={self.token}")
        except socketio.exceptions.ConnectionError as e:
            self.logger.exception(f"{type(e).__name__}: {e}")
            raise SteamlabsSIOConnectionError(
                "no connection could be established to the Streamlabs SIO server"
            ) from e
        return self

    def _token_from_toml(self) -> str:
        try:
            import tomllib
        except ModuleNotFoundError:
            import tomli as tomllib

        def get_filepath() -> Optional[Path]:
            filepaths = (
                Path.cwd() / "config.toml",
                Path.home() / ".config" / "streamlabsio" / "config.toml",
            )
            for filepath in filepaths:
                if filepath.exists():
                    return filepath

        try:
            filepath = get_filepath()
            if not filepath:
                raise FileNotFoundError("config.toml was not found")
            with open(filepath, "rb") as f:
                conn = tomllib.load(f)
                assert "token" in conn.get(
                    "streamlabs"
                ), "token not found in config.toml"
            return conn["streamlabs"].get("token")
        except (FileNotFoundError, tomllib.TOMLDecodeError) as e:
            self.logger.error(f"{type(e).__name__}: {e}")
            raise

    def connect_handler(self):
        self.logger.info("Connected to Streamlabs Socket API")

    def event_handler(self, data):
        if "for" in data and data["type"] in set(
            self.streamlabs + self.twitch + self.youtube
        ):
            message = data["message"][0] if isinstance(data["message"][0], dict) else {}
            self.obs.trigger(
                data["for"],
                data["type"],
                message
                if self._raw
                else as_dataclass(data["type"], message),
            )
            self.logger.debug(data)

    def disconnect_handler(self):
        self.logger.info("Disconnected from Streamlabs Socket API")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sio.disconnect()


def connect(**kwargs):
    SIO_cls = Client
    return SIO_cls(**kwargs)
