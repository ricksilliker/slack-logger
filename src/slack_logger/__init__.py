import logging

from .handlers import ChannelHandler
from .formatters import TextFormatter

__all__ = ['ChannelHandler', 'TextFormatter']
__version__ = '0.1.0'


def get_channel_logger(channel_id: str, auth_token: str, name='', timeout=10) -> logging.Logger:
    log = logging.getLogger(name)
    handler = ChannelHandler(
        channel_id=channel_id,
        bot_token=auth_token,
        level=logging.INFO,
        timeout=timeout
    )
    log.addHandler(handler)
    return log