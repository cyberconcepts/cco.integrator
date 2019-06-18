'''
Dispatcher functions
  
2019-05-26 helmutm@cy55.de
'''

import glob
from threading import Thread
from Queue import Queue, Empty
import os
from os.path import abspath, dirname, isdir, isfile, join
import shutil
import sys
import time
import traceback

from cco.integrator import actor, context


this_module = sys.modules[__name__]


def run(ctx, name='dispatcher'):
    p = Thread(target=start, args=[ctx])
    p.start()
    return (p, ctx.mailbox)

def start(ctx):
    start_actors(ctx)
    listener(ctx)

def listener(ctx):
    ctx.logger.info('listening.')
    while step(ctx):
        pass

def step(ctx):
    conf = ctx.config.get('dispatcher')
    actions = ctx.config.get('actions', {})
    msg = ctx.mailbox.get()
    ctx.logger.debug('msg=%s.' % msg)
    if msg == 'quit':
        for (p, mb) in ctx.children:
            mb.put('quit')
        return False
    if isinstance(msg, dict):
        target = msg.get('target')
        if target is None:
            ctx.logger.warn('No target in message.')
        else:
            mb = ctx.registry.get('actors', {}).get(target)
            if mb is None:
                ctx.logger.warn('Target %s missing in registry.' % target)
            else:
                mb.put(msg)
    return True


def start_actors(ctx):
    for act in ctx.config.get('actors', []):
        actor.run(ctx, act)

