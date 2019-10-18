'''
Context class and related functions
  
2019-06-14 helmutm@cy55.de
'''

from logging import getLogger

from cco.integrator.config import loadConfig
from cco.integrator.mailbox import createMailbox
from cco.integrator.registry import default_registry


def setup(**kw):
    #print('context.setup: {}'.format(kw))
    return Context(**kw)

def setupChild(p, config=None, state=None, logger=None):
    return setup(
        config=config or p.config,
        state=state,
        logger=logger or p.logger,
        home=p.home,
        system=p.system,
        parent_mb=p.mailbox,
        services=p.services,
        registry=p.registry
    )


class Context:

    def __init__(self, home='.', system='generic', state=None, 
                 cfgname='config.yaml', 
                 registry=None, services=None, parent_mb=None,
                 config=None, logger=None, 
                 mailbox=None, children=None, pname=None):
        self.home = home
        self.system = system
        self.state = state
        self.registry = registry or default_registry
        self.services = services or {}
        self.parent_mb = parent_mb
        self.config = config or loadConfig(home, cfgname)
        self.logger = logger or getLogger('cco.integrator')
        self.mailbox = mailbox or createMailbox()
        self.children = children or []
        self.pname = pname

