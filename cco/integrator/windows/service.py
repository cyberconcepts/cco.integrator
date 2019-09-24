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
    
    _svc_name_ = 'cco.integrator'
    _svc_display_name_ = 'cco.integrator service'
    _svc_description_ = 'Integrator Service for processing files and data'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def start(self):
        # to be implemented by subclass
        pass

    def stop(self):
        # to be implemented by subclass
        pass

    # win32 service call back methods

    def SvcStop(self):
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.start()

