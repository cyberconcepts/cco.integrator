'''
Logger for testing purposes
  
2019-06-10 helmutm@cy55.de
'''

from collections import deque
import logging

loggerQueue: deque = deque()


class QueueHandler(logging.Handler):

    def __init__(self, level: int = logging.NOTSET) -> None:
        logging.Handler.__init__(self, level)
        self.logs = loggerQueue

    def emit(self, logRecord: logging.LogRecord) -> None:
        self.logs.append(logRecord)

