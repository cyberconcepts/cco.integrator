'''
Creation and handling of actor processes (mostly just threads)
  
2019-06-21 helmutm@cy55.de

'''

from asyncio import create_task
import traceback


class Process(object):

    def __init__(self, task, name):
        self.task = task
        self.name = name


def run(target, ctx, name='???'):
    #t = create_task(target(ctx))
    t = create_task(runExcept(target, ctx))
    return Process(t, name)

async def runExcept(target, ctx):
    try:
        await (target(ctx))
    except:
        ctx.logger.error(traceback.format_exc())
