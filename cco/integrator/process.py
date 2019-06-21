'''
Creation and handling of actor processes (mostly just threads)
  
2019-06-21 helmutm@cy55.de

'''

from threading import Thread


class Process(object):

    def __init__(self, thread):
        self.thread = thread


def run(target, params):
    th = Thread(target=target, args=params)
    p = Process(th)
    th.start()
    return p
