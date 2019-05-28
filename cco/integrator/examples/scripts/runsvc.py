'''
Application Integrator (Linux version):
  
2019-04-13 helmutm@cy55.de

'''

from os.path import abspath, dirname

from cco.integrator import dispatcher

home = abspath(dirname(dirname(__file__)))

if __name__ == '__main__':
    mailbox = dispatcher.init()
    dispatcher.start(mailbox, dict(system='linux', home=home))

