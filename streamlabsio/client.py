import socketio
from loguru import logger
from observable import Observable

from .error import SteamlabsSIOConnectionError
from .models import as_dataclass


class Client:
    EVENT_TYPES: set[str] = (
        {'donation'}  # streamlabs
        | {'follow', 'subscription', 'host', 'bits', 'raid'}  # twitch
        | {'follow', 'subscription', 'superchat'}  # youtube
    )

    def __init__(self, *, token: str, raw: bool = False):
        self._logger = logger.bind(name=self.__class__.__name__)
        self._token = token
        self._raw = raw
        self.sio = socketio.Client()
        self.sio.on('connect', self._connect_handler)
        self.sio.on('event', self._event_handler)
        self.sio.on('disconnect', self._disconnect_handler)
        self.obs = Observable()

    def __enter__(self) -> 'Client':
        try:
            self.sio.connect(f'https://sockets.streamlabs.com?token={self._token}')
        except socketio.exceptions.ConnectionError as e:
            self._logger.exception('Connection to Streamlabs Socket API failed')
            ERR_MSG = 'Failed to connect to Streamlabs Socket API. Please check your token and network connection.'
            raise SteamlabsSIOConnectionError(ERR_MSG) from e
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.sio.disconnect()

    def _connect_handler(self) -> None:
        self._logger.info('Connected to Streamlabs Socket API')

    def _event_handler(self, data: dict) -> None:
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

        match data:
            case {
                'for': str() as target,
                'type': str() as event_type,
                'message': list() as message_list,
            } if event_type in Client.EVENT_TYPES:
                # The message type is expected to be a list, however, in practice, it often contains only one item.
                # To ensure compatibility with the actual data structure,
                # we will iterate over the message list and trigger events for each message item.
                for message in message_list:
                    self.obs.trigger(
                        target,
                        event_type,
                        message if self._raw else as_dataclass(event_type, message),
                    )
                    self._logger.debug(
                        f'Triggered event: {target} {event_type} {message}'
                    )
            case _:
                self._logger.debug(f'Unexpected event data: {data}')

    def _disconnect_handler(self) -> None:
        self._logger.info('Disconnected from Streamlabs Socket API')


def request_client_object(*, token: str, raw: bool = False) -> Client:
    return Client(token=token, raw=raw)
