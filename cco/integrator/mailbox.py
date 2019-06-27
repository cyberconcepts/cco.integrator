'''
Mailbox types with send and receive functions
  
2019-06-20 helmutm@cy55.de

'''

from asyncio import Queue, QueueEmpty, TimeoutError, wait_for

from cco.integrator.message import no_message


def createMailbox():
    return Mailbox()


class Mailbox(object):

    def __init__(self):
        self.queue = Queue()


async def send(mb, msg):
    await mb.queue.put(msg)

async def receive(mb, timeout=None):
    if timeout is None:
        return await mb.queue.get()
    try:
        if timeout == 0:
            return await mb.queue.get_nowait()
        return await wait_for(mb.queue.get(), timeout)
    except (QueueEmpty, TimeoutError):
        return no_message

