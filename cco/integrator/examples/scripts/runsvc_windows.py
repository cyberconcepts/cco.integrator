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

from cco.integrator.windows.service import WinService


class WinService(service.WinService):

    def start(self):
        asyncio.run(system.start(home, system='windows'))
        #win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(WinService)

