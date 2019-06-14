'''
Application Integrator (Linux version):
  
2019-04-13 helmutm@cy55.de

'''

from os.path import abspath, dirname

from cco.integrator import context, dispatcher

home = abspath(dirname(dirname(__file__)))

if __name__ == '__main__':
    ctx = context.setup(system='linux', home=home)
    dispatcher.start(ctx)
