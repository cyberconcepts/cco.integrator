'''
System startup
  
2019-09-29 helmutm@cy55.de
'''

from cco.integrator import config, context, dispatcher, registry, system


async def start(home):
    params = system.cmdlineArgs()
    reg = registry.load()
    # TODO: load config, including plugins (with registry update):
    #conf = config.loadConfig(home, cfgname, cfgpath)
    config.loadLoggerConf(home)
    ctx = context.setup(home=home, registry=reg, **params)
    await dispatcher.start(ctx)
    await system.wait()
    exit()

