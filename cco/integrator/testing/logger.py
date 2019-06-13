'''
Logger for testing purposes
  
2019-06-10 helmutm@cy55.de
'''

import logging

from cco.integrator.tests import loggerQueue


class QueueHandler(logging.Handler):

    def __init__(self, level=logging.NOTSET):
        logging.Handler.__init__(self, level)
        self.logs = loggerQueue

    def emit(self, logRecord):
        self.logs.append(logRecord)

