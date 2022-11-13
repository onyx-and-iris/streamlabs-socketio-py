import logging
from threading import Thread

import streamlabsio

logging.basicConfig(level=logging.INFO)


def on_youtube_event(event, msg):
    print(f"{event}: {msg.attrs()}")


def on_twitch_event(event, msg):
    if event == "follow":
        print(f"Received follow from {msg.name}")
    elif event == "bits":
        print(f"{msg.name} donated {msg.amount} bits! With message: {msg.message}")


def register_callbacks(client):
    client.obs.on("streamlabs", on_twitch_event)
    client.obs.on("twitch_account", on_twitch_event)
    client.obs.on("youtube_account", on_youtube_event)


def main():
    with streamlabsio.connect() as client:
        worker = Thread(target=register_callbacks, args=(client,), daemon=True)
        worker.start()

        while cmd := input("<Enter> to exit\n"):
            if not cmd:
                break


if __name__ == "__main__":
    main()
