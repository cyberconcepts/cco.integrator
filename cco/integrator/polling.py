'''
A polling server
  
2019-05-23 helmutm@cy55.de

'''

import json
from Queue import Empty
from time import sleep
import urllib2


def serve(mailbox, receiver, logger, conf):
    url = conf.get('url', 'http://localhost:8123/poll')
    timeout = conf.get('http_timeout', 30)
    sleep_excp = conf.get('sleep_on_excp', 30)
    sleep_idle = conf.get('sleep_on_idle', 0)
    sleep_data = conf.get('sleep_on_data', 0)
    active = True
    while active:
        try:
            resp = get_data(url, timeout)
        except urllib2.URLError, e:
            logger.warn('polling: URL = %s => error %s.' % (url, e.reason))
            if check_mailbox(mailbox) != 'quit':
                return
            sleep(sleep_excp)
            continue
        if resp is None:    # timeout
            logger.warn('polling: no response from %s.' % url)
            if check_mailbox(mailbox) != 'quit':
                return
            sleep(sleep_excp)
        elif resp.get('result') == 'idle':
            sleep(sleep_idle)
        else:
            receiver.put(resp['message'])
            sleep(sleep_data)
        active = check_mailbox(mailbox) != 'quit'

def get_data(url, timeout):
    conn = urllib2.urlopen(url, timeout=timeout)
    if conn is None:
        return None
    data = json.loads(conn.read())
    conn.close()
    return data

def check_mailbox(mailbox):
    try:
        return mailbox.get_nowait()
    except Empty:
        return None
