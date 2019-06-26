'''
Creation and handling of actor processes (mostly just threads)
  
2019-06-21 helmutm@cy55.de

'''

from asyncio import create_task


class Process(object):

    def __init__(self, task, name):
        self.task = task
        self.name = name


def run(target, params, name='???'):
    t = create_task(target(*params))
    return Process(t, name)
