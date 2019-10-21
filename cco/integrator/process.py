'''
Creation and handling of actor processes (mostly just threads)
  
2019-06-21 helmutm@cy55.de

'''

from asyncio import create_task, Task
from dataclasses import dataclass
import traceback

from cco.integrator.common import Named

from typing import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cco.integrator.context import Context
else:
    Context = 'Context'


@dataclass
class Process(Named):

    task: Task


def run(target: Callable, ctx: Context, name: str = '???') -> Process:
    #t = create_task(target(ctx))
    t = create_task(runExcept(target, ctx))
    return Process(name, t)

async def runExcept(target: Callable, ctx: Context) -> None:
    try:
        await (target(ctx))
    except:
        ctx.logger.error(traceback.format_exc())
