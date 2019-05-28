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

from cco.integrator import dispatcher, winbase


class WinService(winbase.WinService):
    
    _svc_name_ = 'winsvc'
    _svc_display_name_ = 'Application Integrator Service'
    _svc_description_ = 'Integrator Service for processing files and data'

    def start(self):
        self.actorMailbox = dispatcher.init()

    def stop(self):
        self.actorMailbox.put('quit')

    def main(self):
        dispatcher.start(self.actorMailbox, dict(system='windows', home=home))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        mailbox = dispatcher.init()
        dispatcher.start(mailbox, dict(system='windows', home=home))
    else:
        win32serviceutil.HandleCommandLine(WinService)

