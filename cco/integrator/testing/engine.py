'''
A simple testing engine

2019-06-19 helmutm@cy55.de
'''

def init():
    return Collector()


class Collector(object):

    def __init__(self):
        self.count = 0
        self.items = []


class Item(object):

    def __init__(self, number, message, result):
        self.number = number
        self.message = message
        self.result = result
