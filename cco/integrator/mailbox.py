'''
Mailbox types with send and receive functions
  
2019-06-20 helmutm@cy55.de

'''

from asyncio import Queue, QueueEmpty, TimeoutError, wait_for
from dataclasses import dataclass, field

from cco.integrator.message import no_message, Message

from typing import Optional


@dataclass
class Mailbox:

    queue: Queue = field(default_factory=Queue)


def createMailbox() -> Mailbox:
    return Mailbox()


async def send(mb: Mailbox, msg: Message) -> None:
    await mb.queue.put(msg)

async def receive(mb: Mailbox, timeout: Optional[int] = None) -> Message:
    if timeout is None:
        return await mb.queue.get()
    try:
        if timeout == 0:
            return await mb.queue.get_nowait()
        return await wait_for(mb.queue.get(), timeout)
    except (QueueEmpty, TimeoutError):
        return no_message

