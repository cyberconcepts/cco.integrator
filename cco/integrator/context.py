'''
Context class and related functions
  
2019-06-14 helmutm@cy55.de
'''

from logging import getLogger, Logger

from cco.integrator.config import loadConfig, Config
from cco.integrator.mailbox import createMailbox, Mailbox
from cco.integrator.process import Process
from cco.integrator.registry import default_registry, Registry

from typing import Any, Dict, List, Optional, Tuple


class Context:

    def __init__(self, 
                 home: str = '.', 
                 system: str = 'generic', 
                 state: Any = None, 
                 cfgname: str = 'config.yaml', 
                 registry: Optional[Registry] = None, 
                 services: Optional[Dict[str, Dict[str, Mailbox]]] = None, 
                 parent_mb: Optional[Mailbox] = None,
                 config: Optional[Config] = None, 
                 logger: Optional[Logger] = None, 
                 mailbox: Optional[Mailbox] = None, 
                 children: Optional[List[Tuple[Process, Mailbox]]] = None, 
                 pname: Optional[str] = None) -> None:
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


def setup(**kw) -> Context:
    #print('context.setup: {}'.format(kw))
    return Context(**kw)

def setupChild(p: Context, 
               config: Optional[Config] = None, 
               state: Any = None, 
               logger: Optional[Logger] = None) -> Context:
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
