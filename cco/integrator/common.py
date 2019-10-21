'''
Common class and function definitions
  
2019-08-26 helmutm@cy55.de

'''

from dataclasses import dataclass

@dataclass
class Named:

    name: str
