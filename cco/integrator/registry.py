'''
Function registry for controlled dynamic addressing via config options
  
2019-06-20 helmutm@cy55.de

'''

from importlib import import_module

from typing import Callable, Dict, List, Optional, cast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cco.integrator.context import Context
else:
    Context = 'Context'

class Registry:

    def __init__(self) -> None:
        self.groups: Dict[str, Group] = {}

    def __str__(self) -> str:
        return '<Registry groups=%s>' % self.groups


class Group:

    def __init__(self) -> None:
        self.handlers: Dict[str, Callable] = {}

    def __str__(self) -> str:
        return '<Group handlers=%s>' % self.handlers


def getHandler(ctx: Context, name: str, 
               group: Optional[str] = None, 
               defGroup: str = 'actor') -> Optional[Callable]:
    group = cast(Optional[str], group or ctx.config.get('group'))
    name = cast(str, ctx.config.get(name) or name)
    if group is None and '.' in name:
        group, name = name.rsplit('.', 1)
    if group is None:
        group = defGroup
    if group not in ctx.registry.groups:
        return None
    h = ctx.registry.groups[group].handlers.get(name)
    if h is None and group != defGroup:
        h = ctx.registry.groups[defGroup].handlers.get(name)
    return h

default_registry = Registry()

standard_prefix = 'cco.integrator'
standard_modules = ['actor', 'checker', 'worker',
                    'client.web', 'server.web']

def load(modules: List[str] = standard_modules, 
         prefix: str = standard_prefix,
         registry: Optional[Registry] = None) -> Registry:
    if registry is None:
        registry = default_registry
    for m in modules:
        mname = '.'.join(x for x in [prefix, m] if x)
        module = import_module(mname)
        regFct = getattr(module, 'register_handlers', None)
        if regFct is not None:
            regFct(registry)
    return registry

def declare_handlers(fcts: List[Callable], 
                     group: Optional[str] = None, 
                     registry: Optional[Registry] = None) -> None:
    if registry is None:
        registry = default_registry
    for f in fcts:
        if group is None:
            group = f.__module__
        if isinstance(f, tuple):
            f, name = f
        else:
            name = f.__name__
        g = registry.groups.setdefault(group, Group())
        g.handlers[name] = f
