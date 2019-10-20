'''
Common class and function definitions
  
2019-08-26 helmutm@cy55.de

'''

class Named:

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return '<%s %s>' % (self.__class__.__name__, self.name)

