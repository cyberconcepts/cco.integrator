'''
Base class for running a Python program as a Windows service.
  
2019-05-10 helmutm@cy55.de

Based on SMWinservice by Davide Mastromatteo (https://gist.github.com/mastro35)
'''

import socket
import sys

import servicemanager
import win32event
import win32service
import win32serviceutil


class WinService(win32serviceutil.ServiceFramework):
    
    _svc_name_ = 'winsvc'
    _svc_display_name_ = 'Windows Service'
    _svc_description_ = 'Basic Service for processing files and data'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def start(self):
        ''' Override in subclass.'''
        pass

    def stop(self):
        ''' Override in subclass.'''
        pass

    def main(self):
        ''' Override in subclass.'''
        pass
        #win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    # win32 service call back methods

    def SvcStop(self):
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.do_stop = True

    def SvcDoRun(self):
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(WinService)

