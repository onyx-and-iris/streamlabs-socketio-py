[![PyPI version](https://badge.fury.io/py/streamlabsio.svg)](https://badge.fury.io/py/streamlabsio)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/onyx-and-iris/streamlabs-socketio-py/blob/dev/LICENSE)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

# A Python client for Streamlabs Socket API

For an outline of past/future changes refer to: [CHANGELOG](CHANGELOG.md)

### Requirements

-   A Streamlabs Socket API key.
    -   You can acquire this by logging into your Streamlabs.com dashboard then `Settings->Api Settings->API Tokens`

-   Python 3.8 or greater

### How to install using pip

```
pip install streamlabsio
```

### How to Use

You may store your api key in a `config.toml` file, its contents should resemble:

```toml
[streamlabs]
token = "<apikey>"
```

Place it next to your `__main__.py` file.

#### Otherwise:

You may pass it as a keyword argument.

Example `__main__.py`:

```python
import streamlabsio


def on_twitch_event(event, data):
    print(f"{event}: {data.attrs()}")


def main():
    with streamlabsio.connect(token="<apikey>") as client:
        client.obs.on("streamlabs", on_twitch_event)
        client.obs.on("twitch_account", on_twitch_event)

        # run for 30 seconds then disconnect client from server
        client.sio.sleep(30)


if __name__ == "__main__":
    main()
```

#### note

From the [SocketIO docs](https://python-socketio.readthedocs.io/en/latest/client.html#managing-background-tasks), `client.sio.wait()` may be used if your application has nothing to do in the main thread.

### Client class
`streamlabsio.connect(token="<apikey>", raw=False)`

The following keyword arguments may be passed:

-   `token`: str   Streamlabs SocketIO api token.
-   `raw`: boolean=False    Receive raw data messages as json objects.

The following attribute is available:

-   `raw`: boolean Toggle raw mode at runtime.

### Attributes

For event data you may inspect the available attributes using `attrs()`.

example:

```python
def on_twitch_event(event, data):
    print(f"{event}: {data.attrs()}")
```

### Errors

-   `SteamlabsSIOConnectionError`: Exception raised when connection errors occur

### Logging

To view raw incoming event data set logging level to DEBUG. Check `debug` example.

### Official Documentation

-   [Streamlabs Socket API](https://dev.streamlabs.com/docs/socket-api)
