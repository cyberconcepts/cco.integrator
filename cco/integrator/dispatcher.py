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


def startThread(ctx):
    start_actors(ctx)
    p = Thread(target=listener, args=[ctx])
    p.start()
    return (p, ctx.mailbox)

def start(ctx):
    start_actors(ctx)
    listener(ctx)
    for (p, mb) in ctx.children:
        if mb:
            mb.put('quit')
    time.sleep(1)

def listener(ctx):
    ctx.logger.info('listening.')
    schedConf = ctx.config.get('dispatcher', {})
    timeout = schedConf.get('receive_timeout', 15)
    actions = ctx.config.get('actions', {})
    while step(ctx.mailbox, ctx.logger, timeout, actions):
        pass

def step(mailbox, logger, timeout, actions):
    try:
        msg = mailbox.get(timeout=timeout)
    except Empty:
        msg = actions.get('default', 'default_action')
    logger.debug('msg=%s.' % msg)
    if msg == 'quit':
        return False
    try:
        processActions(actions, logger, msg)
    except:
        logger.error(traceback.format_exc())
    return True

def processActions(actions, logger, msg):
    return

def handler(ctx, msg):
    acts = actions.get(msg, [])
    if isinstance(acts, dict):
        acts = [acts]
    active = True
    while active:
        active = False
        for act in acts:
            if isinstance(act, basestring):
                act = actions[act]
            logger.debug('action=%s.' % act)
            modSpec = act.get('module')
            module = modSpec and import_module(modSpec) or this_module
            fct = getattr(module, act['function'])
            active = fct(act, logger) or active

def start_actors(ctx):
    for act in ctx.config.get('actors', []):
        actor.run(ctx, act)

# predefined actions

def move_file(conf, logger):
    """Move the first file found in source_dir to target_dir."""
    source = conf['source_dir']
    fnames = glob.glob(join(source, '*'))
    for fn in fnames:
        if isfile(fn):
            target = conf['target_dir']
            logger.info('move_file; fn=%s, target=%s.' % (fn, target))
            shutil.copy2(fn, target)
            make_copy(conf, logger, 'backup_dir', fn)
            os.remove(fn)
            return True
    return False


# utility functions

def make_copy(conf, logger, dname, fn):
    """Copy the file to the destination specified via dname."""
    dest = conf.get(dname)
    if dest is not None:
        if not isdir(dest):
            logger.warn('make_copy: destination %s not found.' % dest)
        else:
            shutil.copy2(fn, dest)
