[![PyPI version](https://badge.fury.io/py/streamlabsio.svg)](https://badge.fury.io/py/streamlabsio)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/onyx-and-iris/streamlabs-socketio-py/blob/dev/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

# A Python client for Streamlabs SocketIO API

### Requirements

-   A Streamlabs SocketIO API key.
    -   You can acquire this by logging into your Streamlabs.com dashboard then `Settings->Api Settings->API Tokens`

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
from threading import Thread

import streamlabsio


def on_twitch_event(event, msg):
    print(f"{event}: {msg.attrs()}")


def main():
    with streamlabsio.connect(token="<apikey>") as client:
        client.obs.on("streamlabs", on_twitch_event)
        client.obs.on("twitch_account", on_twitch_event)

        # run for 30 seconds then disconnect client from server
        client.sio.sleep(30)


if __name__ == "__main__":
    main()
```

note. From the [SocketIO docs](https://python-socketio.readthedocs.io/en/latest/client.html#managing-background-tasks), `client.sio.wait()` may be used if your application has nothing to do in the main thread.

### Attributes

For event messages you may inspect the available attributes using `attrs()`.

example:

```python
def on_twitch_event(event, msg):
    print(f"{event}: {msg.attrs()}")
```

### Official Documentation

-   [Streamlabs SocketIO API](https://dev.streamlabs.com/docs/socket-api)
