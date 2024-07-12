import asyncio
import timeit
import signal
import logging
import asyncio
from typing import List

import nats
from nats.aio import msg
from invoker import invoke
from log import safely_start_logging
from config import settings

tasks_termination_timeout: float = settings.tasks_termination_timeout
request_subject: str = settings.request_subject
response_subject_prefix: str = settings.response_subject_prefix
broker_servers: List[str] = settings.broker.servers

async def error_cb(e):
    logging.error("Error:", e)

async def closed_cb():
    # Wait for tasks to stop otherwise get a warning.
    await asyncio.sleep(tasks_termination_timeout)
    loop.stop()

async def reconnected_cb():
    logging.info("Got reconnected to NATS...")

async def main():
    await safely_start_logging()
    logging.info('Start lambda function')

    options = {
        "error_cb": error_cb,
        "closed_cb": closed_cb,
        "reconnected_cb": reconnected_cb,
        "servers": broker_servers
    }

    js = None
    try:
        nc = await nats.connect(**options)
        js = nc.jetstream()
    except Exception as e:
        logging.exception(e)

    if not js:
        logging.exception("JetStream wasn't initialized")
        raise RuntimeError("JetStream wasn't initialized")

    logging.info("Listening on [%s]", request_subject)

    async def subscribe_handler(message: msg.Msg):
        subject = message.subject
        reply = message.reply
        data = message.data.decode()
        logging.info(
            "Received a message on '%s %s' %s", subject, reply, data
        )
        start = timeit.default_timer()
        response = invoke(data, None)
        id = subject.split('.')[1]
        if not id:
            logging.warn("Can't retrieve id from %s", message.subject)
            return
        response_subject = f"{response_subject_prefix}.{id}"
        logging.debug("Response to %s", response_subject)

        if response:
            await js.publish(response_subject, response)
            await message.ack()
            end = timeit.default_timer()
            logging.info("Processed request %s in time %f", message, end-start)
        else:
            logging.warn("Response from function is None")

    def signal_handler():
        if nc.is_closed:
            return
        asyncio.create_task(nc.drain())

    for sig in ('SIGINT', 'SIGTERM'):
        asyncio.get_running_loop().add_signal_handler(getattr(signal, sig), signal_handler)

    await js.subscribe(request_subject, cb=subscribe_handler)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    try:
        loop.run_forever()
    finally:
        loop.close()
