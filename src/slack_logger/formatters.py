import logging
import json


class BlockFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super(BlockFormatter, self).__init__(fmt, datefmt, style)

    def format(self, record:logging.LogRecord) -> str:
        blocks = []
        return json.dumps(blocks)


class TextFormatter(logging.Formatter):
    def __init__(self):
        super(TextFormatter, self).__init__()

    def format(self, record: logging.LogRecord) -> str:
        return super(TextFormatter).format(record)
