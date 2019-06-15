'''
Context class and related functions
  
2019-06-14 helmutm@cy55.de
'''

import logging.config
from logging import getLogger
from os.path import join
from Queue import Queue
import yaml


def setup(**kw):
    return Context(**kw)

def setupChild(p, config=None, logger=None):
    return setup(
        config=config or p.config,
        logger=logger or p.logger,
        home=p.home,
        system=p.system,
        parent_mb=p.mailbox,
        services=p.services,
        registry=p.registry
    )


class Context(object):

    def __init__(self, home='.', system='dummy', cfgname='config.yaml', 
                 registry=None, services=None, parent_mb=None,
                 config=None, logger=None, 
                 mailbox=None, children=None):
        self.home = home
        self.system = system
        self.registry = registry or {}
        self.services = services or {}
        self.parent_mb = parent_mb
        self.config = config or loadConfig(home, cfgname)
        self.logger = logger or getLogger('cco.integrator')
        self.mailbox = mailbox or Queue()
        self.children = children or []


def loadConfig(home, name):
    confPath = join(home, 'etc')
    confData = loadYaml(join(confPath, name))
    logConf = loadYaml(join(confPath, 'logging.yaml'))
    logging.config.dictConfig(logConf)
    return confData

def loadYaml(path):
    f = open(path)
    data = yaml.load(f.read(), Loader=yaml.SafeLoader) 
    f.close()
    return data

