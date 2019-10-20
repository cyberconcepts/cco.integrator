'''
Data and function definitions for configuration settings
  
2019-06-16 helmutm@cy55.de
'''

import logging.config
import yaml

from cco.integrator.system import makePath

from typing import Any, Dict, List, Union

ConfigList = List[Any]
ConfigDict = Dict[str, Any]
Config = Dict[str, Union[bool, str, int, float, ConfigList, ConfigDict]]


def loadConfig(home: str, 
               name: str = 'config.yaml', 
               path: str = 'etc') -> Config:
    confPath = makePath(home, path, name)
    confData = loadYaml(confPath)
    return confData

def loadLoggerConf(home: str, 
                   name: str = 'logging.yaml', 
                   path: str = 'etc') -> None:
    confPath = makePath(home, path, name)
    logConf = loadYaml(confPath)
    logging.config.dictConfig(logConf)

def loadYaml(path: str) -> Config:
    with open(path) as f: 
        data = yaml.load(f.read(), Loader=yaml.SafeLoader) 
    # TODO: load and merge (?) config include
    # TODO: validate against JSON schema (if provided)
    return data

