'''
Context class and related functions
  
2019-06-14 helmutm@cy55.de
'''

from dataclasses import dataclass, field
from functools import partial
from logging import getLogger, Logger

from cco.integrator.config import loadConfig, Config
from cco.integrator.mailbox import createMailbox, Mailbox
from cco.integrator.process import Process
from cco.integrator.registry import default_registry, Registry

from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Context:

    home:       str = '.'
    system:     str = 'generic'
    state:      Any = None
    cfgname:    str = 'config.yaml'
    registry:   Registry = default_registry
    services:   Dict[str, Dict[str, Mailbox]] = field(default_factory=dict)
    parent_mb:  Optional[Mailbox] = None
    config:     Config = field(default_factory=dict)
    logger:     Logger = field(default_factory=partial(getLogger, 'integrator'))
    mailbox:    Mailbox = field(default_factory=createMailbox)
    children:   List[Tuple[Process, Mailbox]] = field(default_factory=list)
    pname:      Optional[str] = None

    def __post_init__(self):
        if not self.config:
            self.config = loadConfig(self.home, self.cfgname)


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
