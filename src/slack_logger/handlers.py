import logging
import json
import threading
import queue
import time

import requests

from . import formatters

SLACK_API_URL = 'https://slack.com/api'


class ChannelHandler(logging.Handler):
    def __init__(self, level: int, channel_id: str, bot_token: str, max_timeout: int):
        super(ChannelHandler, self).__init__(level)

        if level != logging.DEBUG and max_timeout == 0:
            raise ValueError(
                'Non debug level handlers, are not allowed to have no timeout, this would cause the logger to hang.'
            )

        self.channel_id = channel_id
        self.bot_token = bot_token
        self.max_timeout = max_timeout

        self._fifo_queue = queue.Queue()
        self._worker_thread = threading.Thread(
            target=send_slack_message, args=(self.channel_id, self.bot_token, self._fifo_queue)
        )
        self._worker_thread.setDaemon(True)
        self._worker_thread.start()

    def emit(self, record):
        msg = self.format(record)
        data = dict(formatter=self.formatter, message=msg)
        self._fifo_queue.put(data)
        # self.send_slack_message(msg)


def send_slack_message(channel_id: str, bot_token: str,  fifo_queue: queue.Queue):
    while True:
        if fifo_queue.empty():
            time.sleep(3)
            continue
        data = fifo_queue.get()
        message = data['message']
        formatter = data['formatter']

        headers = {
            'Authorization': 'Bearer {0}'.format(bot_token),
            'Content-Type': 'application/json'
        }
        url = SLACK_API_URL + '/chat.postMessage'
        body = {
            'channel': channel_id,
        }
        if isinstance(formatter, formatters.BlockFormatter):
            body['text'] = ''
            body['blocks'] = message
        else:
            body['text'] = message

        try:
            resp = requests.post(url, data=json.dumps(body), headers=headers)
            if not resp.json()['ok']:
                resp.raise_for_status()
        except ConnectionError as err:
            raise
        except TimeoutError as err:
            raise