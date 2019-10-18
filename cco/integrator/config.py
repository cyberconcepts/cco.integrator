'''
Data and function definitions for configuration settings
  
2019-06-16 helmutm@cy55.de
'''

import logging.config
import yaml

from cco.integrator.system import makePath


def loadConfig(home, name='config.yaml', path='etc'):
    confPath = makePath(home, path, name)
    confData = loadYaml(confPath)
    return confData

def loadLoggerConf(home, name='logging.yaml', path='etc'):
    confPath = makePath(home, path, name)
    logConf = loadYaml(confPath)
    logging.config.dictConfig(logConf)

def loadYaml(path):
    with open(path) as f: 
        data = yaml.load(f.read(), Loader=yaml.SafeLoader) 
    # TODO: load and merge (?) config include
    # TODO: validate against JSON schema (if provided)
    return data

