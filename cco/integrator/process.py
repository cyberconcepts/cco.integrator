'''
Creation and handling of actor processes (mostly just threads)
  
2019-06-21 helmutm@cy55.de

'''

from asyncio import create_task, Task
import traceback

from cco.integrator.common import Named

from typing import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cco.integrator.context import Context
else:
    Context = 'Context'


class Process(Named):

    def __init__(self, task: Task, name: str):
        self.task = task
        self.name = name


def run(target: Callable, ctx: Context, name: str = '???') -> Process:
    #t = create_task(target(ctx))
    t = create_task(runExcept(target, ctx))
    return Process(t, name)

async def runExcept(target: Callable, ctx: Context) -> None:
    try:
        await (target(ctx))
    except:
        ctx.logger.error(traceback.format_exc())
