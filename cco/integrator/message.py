'''
Message types and related functions
  
2019-06-20 helmutm@cy55.de

'''

from cco.integrator.common import Named

from typing import Any, Dict, Optional


class MessageType(Named):
    priority = 5

class ControlMT(MessageType):
    priority = 2

class InfoMT(MessageType):
    priority = 5

class CommandMT(MessageType):
    priority = 7

quitMT = ControlMT('quit')
systemMT = ControlMT('system')

dataMT = InfoMT('data')
eventMT = InfoMT('event')
queryMT = InfoMT('query')

commandMT = CommandMT('command')
createMT = CommandMT('create')
updateMT = CommandMT('update')


class Message:

    def __init__(self, 
                 payload: Dict[str, Any] = {}, 
                 type: MessageType = dataMT) -> None:
        self.payload = payload
        self.type = type
        #self.timestamp = 

    def __str__(self) -> str:
        return '<Message type=%s, payload=%s>' % (self.type.name, self.payload)


no_message = Message(type=MessageType('empty'))

quit = Message(type=quitMT)

message_types: Dict[str, MessageType] = {}

for mt in (quitMT, systemMT, dataMT, eventMT, queryMT,
           commandMT, createMT, updateMT):
    message_types[mt.name] = mt
