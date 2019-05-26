'''
Application Integrator (Linux version):
  
2019-04-13 helmutm@cy55.de

'''

from cco.integrator import dispatcher


if __name__ == '__main__':
    mailbox = dispatcher.init()
    dispatcher.start(mailbox, 'linux')

