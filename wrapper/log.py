import json
import asyncio
import logging
from logging.handlers import QueueListener, QueueHandler
from logging import StreamHandler, LogRecord
from queue import Queue
from config import settings

class GoLikeFormatter(logging.Formatter):
    """Formatter to dump error message into JSON"""

    def format(self, record: LogRecord) -> str:
        record_dict = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%fZ"),
            "level": record.levelname,
            "msg": record.getMessage(),
            "module": record.module,
            "lineno": record.lineno
        }
        return f"{record_dict['time']}\t{record_dict['level']}\t{record_dict['module']}:{record_dict['lineno']}\t{record_dict['msg']}"

class JsonFormatter(logging.Formatter):
    """Formatter to dump error message into JSON"""

    def format(self, record: LogRecord) -> str:
        record_dict = {
            "time": self.formatTime(record),# "%Y%m%dT%H%M%S.%fZ"),
            "level": record.levelname,
            "msg": record.getMessage(),
            "module": record.module,
            "lineno": record.lineno,
        }
        return json.dumps(record_dict)

# helper coroutine to setup and manage the logging
async def init_logging():
    # get the root logging
    log = logging.getLogger()
    # create the shared queue
    que = Queue()
    handler = QueueHandler(que)
    # handler.setFormatter(JsonFormatter())
    handler.setFormatter(GoLikeFormatter())
    # add a handler that uses the shared queue
    log.addHandler(handler)
    # log all messages, debug and up
    log.setLevel(settings.log_level)
    # create a listener for messages on the queue
    listener = QueueListener(que, StreamHandler())
    try:
        # start the listener
        listener.start()
        # report the logging is ready
        logging.debug(f'logging has started')
        # wait forever
        while True:
            await asyncio.sleep(60)
    finally:
        # report the logging is done
        logging.debug(f'logging is shutting down')
        # ensure the listener is closed
        listener.stop()

# reference to the logging task
logging_TASK = None
# coroutine to safely start the logging
async def safely_start_logging():
    # initialize the logging
    logging_TASK = asyncio.create_task(init_logging())
    # allow the logging to start
    await asyncio.sleep(0)
