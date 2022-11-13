import logging

import streamlabsio

logging.basicConfig(level=logging.INFO)


def on_youtube_event(event, msg):
    print(f"{event}: {msg.attrs()}")


def on_twitch_event(event, msg):
    if event == "follow":
        print(f"Received follow from {msg.name}")
    elif event == "bits":
        print(f"{msg.name} donated {msg.amount} bits! With message: {msg.message}")
    elif event == "donation":
        print(f"{msg.name} donated {msg.formatted_amount}! With message: {msg.message}")


def main():
    # read token from config.toml
    with streamlabsio.connect() as client:
        client.obs.on("streamlabs", on_twitch_event)
        client.obs.on("twitch_account", on_twitch_event)
        client.obs.on("youtube_account", on_youtube_event)

        # run for 30 seconds then disconnect client from server
        client.sio.sleep(30)


if __name__ == "__main__":
    main()
