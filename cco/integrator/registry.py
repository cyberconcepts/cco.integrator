'''
Function registry for controlled dynamic addressing via config options
  
2019-06-20 helmutm@cy55.de

'''

class Registry(object):

    def __init__(self):
        self.groups = {}


class Group(object):

    def __init__(self):
        self.handlers = {}
