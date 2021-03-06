'''
Actors for doing some simple real work.
  
2019-05-26 helmutm@cy55.de

'''

import os
from os.path import isdir, join
import shutil
import traceback

from cco.integrator import registry


async def move_file(ctx, cfg, msg):
    target = join(ctx.home, cfg['target-dir'])
    for fn in msg.payload['filenames']:
        ctx.logger.debug('move_file; fn=%s, target=%s.' % (fn, target))
        try:
            shutil.copy2(fn, target)
            make_copy(ctx, cfg, 'backup-dir', fn)
            os.remove(fn)
        except:
            ctx.logger.error(traceback.format_exc())
    return True

# utility functions

def make_copy(ctx, cfg, dname, fn):
    """Copy the file to the destination specified via dname."""
    dest = cfg.get(dname)
    if dest is not None:
        path = join(ctx.home, dest)
        if not isdir(path):
            ctx.logger.warn('make_copy: destination %s not found.' % path)
        else:
            shutil.copy2(fn, path)

#*** register_handlers ***

def register_handlers(reg):
    registry.declare_handlers([move_file], 'worker', reg)
