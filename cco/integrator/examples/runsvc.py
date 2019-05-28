'''
Application Integrator (Linux version):
  
2019-04-13 helmutm@cy55.de

'''
from os.path import abspath, dirname
import sys

home = abspath(dirname(dirname(__file__)))
sys.path.insert(0, home)

from cco.integrator import dispatcher


if __name__ == '__main__':
    mailbox = dispatcher.init()
    dispatcher.start(mailbox, dict(system='linux', home=home))

