'''
Scheduler service (Linux version):
  - copy/move files to target server/directory
  - Windows only: start Excel and execute macro
  
2019-04-13 helmutm@cy55.de

'''

from cco.integrator import scheduler


if __name__ == '__main__':
    mailbox = scheduler.init()
    scheduler.start(mailbox, 'linux')

