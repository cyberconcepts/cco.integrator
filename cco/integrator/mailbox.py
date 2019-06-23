'''
Mailbox types with send and receive functions
  
2019-06-20 helmutm@cy55.de

'''

from Queue import Queue, Empty

from cco.integrator.message import no_message


def createMailbox():
    return Mailbox()


class Mailbox(object):

    def __init__(self):
        self.queue = Queue()


def send(mb, msg):
    mb.queue.put(msg)

def receive(mb, timeout=None):
    if timeout is None:
        return mb.queue.get()
    try:
        if timeout == 0:
            return mb.queue.get_nowait()
        return mb.queue.get(timeout=timeout)
    except Empty:
        return no_message

