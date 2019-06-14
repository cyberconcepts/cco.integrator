'''
Context class and related functions
  
2019-06-14 helmutm@cy55.de
'''

import logging.config
from logging import getLogger
from os.path import join
from Queue import Queue
import yaml


def setup(home, **kw):
    return Context(home, **kw)


class Context(object):

    def __init__(self, home, system='dummy', cfgname='config.yaml', **kw):
        self.home = home
        self.system = system
        self.config = kw.get('config', loadConfig(home, cfgname))
        self.logger = getLogger('cco.integrator')
        self.services = {}
        self.registry = {}
        self.mailbox = Queue()
        self.children = []


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

