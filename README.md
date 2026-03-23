[![PyPI version](https://badge.fury.io/py/streamlabsio.svg)](https://badge.fury.io/py/streamlabsio)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/onyx-and-iris/streamlabs-socketio-py/blob/dev/LICENSE)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# A Python client for Streamlabs Socket API

For an outline of past/future changes refer to: [CHANGELOG](CHANGELOG.md)

### Requirements

-   A Streamlabs Socket API key.
    -   You can acquire this by logging into your Streamlabs.com dashboard then `Settings->Api Settings->API Tokens`

-   Python 3.10 or greater

### Install

```console
pip install streamlabsio
```

### Use

```python
import streamlabsio


def on_streamlabs_event(event, data):
    print(f'{event}: {data.attrs()}')


def on_twitch_event(event, data):
    if event == 'follow':
        print(f'{data.name} just followed!')


def main():
    with streamlabsio.connect(token="<API token>") as client:
        client.obs.on('streamlabs', on_streamlabs_event)
        client.obs.on('twitch_account', on_twitch_event)

        # run for 30 seconds then disconnect client from server
        client.sio.sleep(30)


if __name__ == '__main__':
    main()
```

> note: From the [SocketIO docs](https://python-socketio.readthedocs.io/en/latest/client.html#managing-background-tasks), `client.sio.wait()` may be used if your application has nothing to do in the main thread.

### Client class
*`streamlabsio.connect(*, token: str, raw: bool = False)`*

The following keyword arguments may be passed:

-   token: Streamlabs SocketIO api token.
-   raw: Receive raw data messages as json objects.

### Event Data Attributes

For event data you may inspect the available attributes using `attrs()`.

example:

```python
def on_twitch_event(event, data):
    print(f'{event}: {data.attrs()}')
```

### Errors

-   `SteamlabsSIOError`: Base StreamlabsSIO error class
-   `SteamlabsSIOConnectionError`: Exception raised when connection errors occur

### Logging

To view the logs emitted by the streamlabsio library simply add the following to your code:

```python
from loguru import logger

logger.enable('streamlabsio')
```

### Official Documentation

-   [Streamlabs Socket API](https://dev.streamlabs.com/docs/socket-api)
