'''
Integrator service, e.g. to
  - copy/move files to target server/directory
  - start Excel and execute macro
  
2019-04-13 helmutm@cy55.de

Usage:
  python runsvc_windows.py (install|update|start|stop)

Based on SMWinservice by Davide Mastromatteo (https://gist.github.com/mastro35)
'''

import sys

import win32serviceutil

home = abspath(dirname(dirname(__file__)))
sys.path.insert(0, home)

from cco.integrator import context, dispatcher
from cco.integrator.windows import base


class WinService(base.WinService):
    
    _svc_name_ = 'winsvc'
    _svc_display_name_ = 'Application Integrator Service'
    _svc_description_ = 'Integrator Service for processing files and data'

    def start(self):
        self.context = context.setup(system='windows', home=home)

    def stop(self):
        self.context.mailbox.put('quit')

    def main(self):
        dispatcher.start(self.context)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        ctx = context.setup(system='windows', home=home)
        dispatcher.start(ctx)
    else:
        win32serviceutil.HandleCommandLine(WinService)

