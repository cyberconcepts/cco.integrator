'''
Actors that check for some condition
  
2019-06-16 helmutm@cy55.de

'''

from glob import glob
from os.path import isfile, join
from Queue import Empty


def step(ctx):
    timeout = ctx.config.get('receive_timeout', 15)
    path = join(ctx.home, ctx.config.get('path', '.'))
    #ctx.logger.debug(path)
    fns = check(path)
    if fns:
        action = ctx.config.get('action', 'dummy')
        msg = dict(action=action, filenames=fns)
        ctx.logger.debug('msg=%s.' % msg)
        ctx.parent_mb.put(msg)
    try:
        msg = ctx.mailbox.get(timeout=timeout)
    except Empty:
        msg = None
    return msg != 'quit'


def check(path):
    return [f for f in glob(join(path, '*')) if isfile(f)]
