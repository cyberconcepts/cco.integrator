'''
Data and function definitions for configuration settings
  
2019-06-16 helmutm@cy55.de
'''

import logging.config
from os.path import join
import yaml


def loadConfig(home, name):
    confPath = join(home, 'etc', name)
    confData = loadYaml(confPath)
    return confData

def loadLoggerConf(home, name='logging.yaml'):
    confPath = join(home, 'etc', name)
    logConf = loadYaml(confPath)
    logging.config.dictConfig(logConf)

def loadYaml(path):
    with open(path) as f: 
        data = yaml.load(f.read(), Loader=yaml.SafeLoader) 
    # TODO: load config include
    return data

