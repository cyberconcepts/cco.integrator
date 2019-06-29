'''
Data and function definitions for configuration settings
  
2019-06-16 helmutm@cy55.de
'''

import logging.config
from os.path import join
import yaml


def loadConfig(home, name):
    confPath = join(home, 'etc')
    confData = loadYaml(join(confPath, name))
    return confData

def loadLoggerConf(home, name):
    confPath = join(home, 'etc')
    logConf = loadYaml(join(confPath, 'logging.yaml'))
    logging.config.dictConfig(logConf)

def loadYaml(path):
    f = open(path)
    data = yaml.load(f.read(), Loader=yaml.SafeLoader) 
    f.close()
    return data

