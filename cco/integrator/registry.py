'''
Function registry for controlled dynamic addressing via config options
  
2019-06-20 helmutm@cy55.de

'''

from importlib import import_module


class Registry(object):

    def __init__(self):
        self.groups = {}

    def __str__(self):
        return '<Registry groups=%s>' % self.groups


class Group(object):

    def __init__(self):
        self.handlers = {}

    def __str__(self):
        return '<Group handlers=%s>' % self.handlers


def getHandler(ctx, name, group=None, defGroup='actor'):
    group = group or ctx.config.get('group')
    name = ctx.config.get(name) or name
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
                    'webserver.simple', 'webserver.wsgi']

def load(modules=standard_modules, 
                  prefix=standard_prefix,
                  registry=None):
    if registry is None:
        registry = default_registry
    for m in modules:
        mname = '.'.join(x for x in [prefix, m] if x)
        module = import_module(mname)
        regFct = getattr(module, 'register_handlers', None)
        if regFct is not None:
            regFct(registry)
    return registry

def declare_handlers(fcts, group=None, registry=None):
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
