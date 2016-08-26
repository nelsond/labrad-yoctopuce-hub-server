"""
### BEGIN NODE INFO
[info]
name = yoctopuce-hub
version = 0.1
description = Hub server for reading values from Yoctopuce devices

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 5
### END NODE INFO
"""

import sys
import os
import json
from labrad.server import LabradServer, Signal, setting
from twisted.internet.task import LoopingCall
import modules as yoctopuce_modules

here = os.path.dirname( os.path.abspath(__file__) )
sys.path.append(os.path.join(here, '.', 'yoctolib_python', 'Sources'))

from yocto_api import *

class YoctopuceHubServer(LabradServer):
    """
    Hub server for reading values from Yoctopuce modules
    """
    name = 'yoctopuce_hub'

    onUpdate = Signal(200, 'signal: onUpdate', 's*(sv)')

    def __init__(self, modules, *args, **kwargs):
        self.initModules(modules)

        LabradServer.__init__(self, *args, **kwargs)

    def initModules(self, _modules):
        self.modules = {}

        for module in _modules:
            name = module['name']
            uid = module['uid']
            klass = getattr(yoctopuce_modules, module['class'])

            self.modules[name] = klass(uid)

    def initServer(self):
        self.worker = LoopingCall(lambda: self.update())
        self.worker.start(1)

    def update(self):
        for name, module in self.modules.iteritems():
            value = module.get_value()
            self.onUpdate( (str(name), self._extract_value(value)) )

    @setting(1, 'modules_available', returns='*(ss)')
    def modules_available(self, c):
        """
        Lists all modules connected to this computer
        """

        modules = []
        module = YModule.FirstModule()
        while module is not None:
            modules.append( (module.get_productName(), module.get_serialNumber()) )
            module = module.nextModule()

        return modules

    @setting(2, 'modules_enabled', returns='*(ss)')
    def modules_enabled(self, c):
        """
        Lists all modules enabled for reading
        """

        modules = []
        for name, module in self.modules.iteritems():
            modules.append( (name, module.__class__.__name__) )

        return modules

    @setting(3, 'get_reading', name='s', returns='*(sv)')
    def get_reading(self, c, name):
        """
        Gets the last measurement for given module name
        """

        module = self.modules[name]
        return self._extract_value(module.last_value)

    @staticmethod
    def _extract_value(value):
        return [(n, v) for n,v in value.iteritems()]

if __name__ == '__main__':
    from labrad import util

    with open(os.path.join('.', 'modules.json'), 'r') as f:
        config_json = f.read()
        modules_config = json.loads(config_json)

    server = YoctopuceHubServer(modules_config)
    util.runServer(server)
