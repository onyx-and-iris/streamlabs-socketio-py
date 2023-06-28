from logging import config

import streamlabsio

config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "standard": {
                "format": "%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s"
            }
        },
        "handlers": {
            "stream": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            }
        },
        "loggers": {"streamlabsio.client": {"handlers": ["stream"], "level": "DEBUG"}},
    }
)


def on_youtube_event(event, data):
    print(f"{event}: {data.attrs()}")


def on_twitch_event(event, data):
    if event == "follow":
        print(f"Received follow from {data.name}")
    elif event == "bits":
        print(f"{data.name} donated {data.amount} bits! With message: {data.message}")
    elif event == "donation":
        print(
            f"{data.name} donated {data.formatted_amount}! With message: {data.message}"
        )


def main():
    with streamlabsio.connect() as client:
        client.obs.on("streamlabs", on_twitch_event)
        client.obs.on("twitch_account", on_twitch_event)
        client.obs.on("youtube_account", on_youtube_event)

        client.sio.sleep(30)


if __name__ == "__main__":
    main()
