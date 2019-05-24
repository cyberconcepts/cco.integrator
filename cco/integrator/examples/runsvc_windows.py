'''
Windows scheduler service, e.g. to
  - copy/move files to target server/directory
  - start Excel and execute macro
  
2019-04-13 helmutm@cy55.de

Usage:
  python runsvc_windows.py (install|update|start|stop)

Based on SMWinservice by Davide Mastromatteo (https://gist.github.com/mastro35)
'''

import sys

import win32serviceutil

from cco.integrator import scheduler, winbase


class WinService(winbase.WinService):
    
    _svc_name_ = 'winsvc'
    _svc_display_name_ = 'Windows scheduler Service'
    _svc_description_ = 'Scheduler Service for processing files and data'

    def start(self):
        self.actorMailbox = scheduler.init()

    def stop(self):
        self.actorMailbox.put('quit')

    def main(self):
        scheduler.start(self.actorMailbox, 'windows')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        mailbox = scheduler.init()
        scheduler.start(mailbox, 'windows')
    else:
        win32serviceutil.HandleCommandLine(WinService)

