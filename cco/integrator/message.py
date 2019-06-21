'''
Message types and related functions
  
2019-06-20 helmutm@cy55.de

'''

no_message = object()

message_types = {}


class MessageType(object):
    priority = 5
    def __init__(self, name):
        self.name = name

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


class Message(object):

    def __init__(self, payload=None, type=dataMT):
        self.payload = payload
        self.type = type
        #self.timestamp = 


quit = Message(type=quitMT)

for mt in (quitMT, systemMT, dataMT, eventMT, queryMT,
           commandMT, createMT, updateMT):
    message_types[mt.name] = mt
