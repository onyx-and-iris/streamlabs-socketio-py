import os

from loguru import logger

import streamlabsio

logger.enable('streamlabsio')


def on_streamlabs_event(event, data):
    match event:
        case 'donation':
            print('{name} donated {amount}! With message: {message}'.format(**data))


def on_twitch_event(event, data):
    event_message = {
        'follow': 'Received follow from {name}',
        'bits': '{name} donated {amount} bits! With message: {message}',
        'subscription': '{name} just subscribed for {months} months!',
        'raid': '{name} just raided with {raiders} raiders!',
        'host': '{name} just hosted with {viewers} viewers!',
    }

    if event in event_message:
        print(event_message[event].format(**data))


def on_youtube_event(event, data):
    event_message = {
        'follow': 'Received follow from {name}',
        'superchat': '{name} donated {displayString} with a superchat! With comment: {comment}',
        'subscription': '{name} just subscribed for {months} months!',
    }

    if event in event_message:
        print(event_message[event].format(**data))


def main():
    try:
        with streamlabsio.connect(
            token=os.getenv('STREAMLABS_TOKEN'), raw=True
        ) as client:
            client.obs.on('streamlabs', on_streamlabs_event)
            client.obs.on('twitch_account', on_twitch_event)
            client.obs.on('youtube_account', on_youtube_event)

            client.wait()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
