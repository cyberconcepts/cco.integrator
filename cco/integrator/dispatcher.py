'''
Dispatcher functions
  
2019-05-26 helmutm@cy55.de
'''

import glob
from importlib import import_module
import logging.config
from logging import getLogger
from threading import Thread
from Queue import Queue, Empty
import os
from os.path import abspath, dirname, isdir, isfile, join
import shutil
import sys
import time
import traceback
import yaml


this_module = sys.modules[__name__]


def loadConfig(param):
    basePath = param.get('home', '.')
    confPath = join(basePath, 'etc')
    confName = param.get('cfgname', 'config.yaml')
    confData = loadYaml(join(confPath, confName))
    logConf = loadYaml(join(confPath, 'logging.yaml'))
    logging.config.dictConfig(logConf)
    return confData

def init():
    return Queue()

def setup(mailbox, param):
    conf = loadConfig(param)
    logger = getLogger('integrator.common')
    actors = start_actors(mailbox, logger, conf)
    return conf, logger, actors

def startThread(ctx):
    actors = start_actors(ctx.mailbox, ctx.logger, ctx.config)
    p = Thread(target=listener, args=[ctx.mailbox, ctx.logger, ctx.config])
    p.start()
    return [(p, ctx.mailbox)] + actors

def start(ctx):
    actors = start_actors(ctx.mailbox, ctx.logger, ctx.config)
    listener(ctx.mailbox, ctx.logger, ctx.config)
    for (p, mb) in actors:
        if mb:
            mb.put('quit')
    time.sleep(2)

def listener(mailbox, logger, conf):
    logger.info('listening.')
    schedConf = conf.get('dispatcher', {})
    actions = conf.get('actions', {})
    timeout = schedConf.get('receive_timeout', 15)
    while process(mailbox, logger, timeout, actions):
        pass

def process(mailbox, logger, timeout, actions):
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

def start_actors(parent_mb, logger, conf):
    actors = []
    for actor in conf.get('actors', []):
        act = conf.get(actor, {})
        logger.debug('starting actor %s.' % actor)
        modSpec = act.get('module')
        module = modSpec and import_module(modSpec) or this_module
        fct = getattr(module, act['function'])
        mb = Queue()
        p = Thread(target=fct, args=[mb, parent_mb, logger, act])
        p.start()
        actors.append((p, mb))
    return actors

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

def loadYaml(path):
    f = open(path)
    data = yaml.load(f.read(), Loader=yaml.SafeLoader) 
    f.close()
    return data

