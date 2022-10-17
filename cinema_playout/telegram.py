import requests

from cinema_playout.config import DEBUG, TG_CHAT_ID, TG_TOKEN


def send_message(message: str):
    '''
    Send a message to the `Telsat Cinema Notifications` group.

    Telegram bot API:
    https://core.telegram.org/bots/api
    Example api call:
    https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=Hello World!
    '''
    chat_id = TG_CHAT_ID
    token = TG_TOKEN
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=token)

    if DEBUG:
        print(f"Telegram message: {message}")
    else:
        try:
            requests.get(url, params=dict(chat_id=chat_id, text=message))
        except Exception as exc:
            raise exc
