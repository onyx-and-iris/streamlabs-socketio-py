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


def register_callbacks(client):
    client.obs.on("streamlabs", on_twitch_event)
    client.obs.on("twitch_account", on_twitch_event)


def main():
    with streamlabsio.connect(token="<apikey>") as client:
        worker = Thread(target=register_callbacks, args=(client,), daemon=True)
        worker.start()

        while cmd := input("<Enter> to exit\n"):
            if not cmd:
                break


if __name__ == "__main__":
    main()
```

### Attributes

For event messages you may inspect the available attributes using `attrs()`.

example:

```python
def on_twitch_event(event, msg):
    print(f"{event}: {msg.attrs()}")
```

### Official Documentation

-   [Streamlabs SocketIO API](https://dev.streamlabs.com/docs/socket-api)
