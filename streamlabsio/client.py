import logging
from pathlib import Path
from typing import Any, Union

import socketio
from observable import Observable

from .error import SteamlabsSIOConnectionError, SteamlabsSIOError
from .models import as_dataclass

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, token=None, raw=False):
        self.logger = logger.getChild(self.__class__.__name__)
        self.token = token or self._token_from_toml()
        self._raw = raw
        self.sio = socketio.Client()
        self.sio.on('connect', self.connect_handler)
        self.sio.on('event', self.event_handler)
        self.sio.on('disconnect', self.disconnect_handler)
        self.obs = Observable()
        self.event_types: set[str] = (
            {'donation'}  # streamlabs
            | {'follow', 'subscription', 'host', 'bits', 'raid'}  # twitch
            | {'follow', 'subscription', 'superchat'}  # youtube
        )

    def __enter__(self):
        try:
            self.sio.connect(f'https://sockets.streamlabs.com?token={self.token}')
        except socketio.exceptions.ConnectionError as e:
            self.logger.exception(f'{type(e).__name__}: {e}')
            raise SteamlabsSIOConnectionError(
                'no connection could be established to the Streamlabs SIO server'
            ) from e
        self.log_mode()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sio.disconnect()

    @property
    def raw(self) -> bool:
        return self._raw

    @raw.setter
    def raw(self, val: bool) -> None:
        self._raw = val
        self.log_mode()

    def log_mode(self):
        info = (
            'Raw mode' if self.raw else 'Normal mode',
            'activated.',
            'JSON messages' if self.raw else 'Event objects',
            'will be passed to callbacks.',
        )
        self.logger.info(' '.join(info))

    def _token_from_toml(self) -> str:
        """
        Retrieves the Streamlabs token from a TOML configuration file.
        This method attempts to load the token from a 'config.toml' file located
        either in the current working directory or in the user's home configuration
        directory under '.config/streamlabsio/'.
        Returns:
            str: The Streamlabs token retrieved from the TOML configuration file.
        Raises:
            SteamlabsSIOError: If no configuration file is found, if the file cannot
            be decoded, or if the required 'streamlabs' section or 'token' key is
            missing from the configuration file.
        """

        try:
            import tomllib
        except ModuleNotFoundError:
            import tomli as tomllib

        def get_filepath() -> Union[Path, None]:
            filepaths = (
                Path.cwd() / 'config.toml',
                Path.home() / '.config' / 'streamlabsio' / 'config.toml',
            )
            for filepath in filepaths:
                if filepath.exists():
                    return filepath
            return None

        filepath = get_filepath()
        if not filepath:
            raise SteamlabsSIOError('no token provided and no config.toml file found')

        try:
            with open(filepath, 'rb') as f:
                conn = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            ERR_MSG = f'Error decoding {filepath}: {e}'
            self.logger.exception(ERR_MSG)
            raise SteamlabsSIOError(ERR_MSG) from e

        if 'streamlabs' not in conn or 'token' not in conn['streamlabs']:
            ERR_MSG = (
                'config.toml does not contain a "streamlabs" section '
                'or the "streamlabs" section does not contain a "token" key'
            )
            self.logger.exception(ERR_MSG)
            raise SteamlabsSIOError(ERR_MSG)

        return conn['streamlabs']['token']

    def connect_handler(self) -> None:
        self.logger.info('Connected to Streamlabs Socket API')

    def event_handler(self, data: Any) -> None:
        """
        Handles incoming events and triggers corresponding OBS actions.
        Args:
            data (dict): The event data containing information about the event.
                Expected keys:
                    - 'for': The target of the event.
                    - 'type': The type of the event.
                    - 'message': A list containing the event message.
        Returns:
            None
        """

        if 'for' in data and data['type'] in self.event_types:
            message = data['message'][0]
            self.obs.trigger(
                data['for'],
                data['type'],
                message if self.raw else as_dataclass(data['type'], message),
            )
            self.logger.debug(data)

    def disconnect_handler(self) -> None:
        self.logger.info('Disconnected from Streamlabs Socket API')


def connect(**kwargs) -> Client:
    SIO_cls = Client
    return SIO_cls(**kwargs)
