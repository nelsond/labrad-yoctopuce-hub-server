import sys
import os

here = os.path.dirname( os.path.abspath(__file__) )
sys.path.append(os.path.join(here, '..', 'yoctolib_python', 'Sources'))

from yocto_api import *

class Base:
    def __init__(self, uid):
        self.uid = uid

        self._initHub()
        self._initModule()

    def get_value(self):
        return [0]

    def _initHub(self):
        if YAPI.RegisterHub('usb') == YAPI.SUCCESS:
            self._log('Successfully registered with hub')
        else:
            self._log('Error registering with hub')
            raise Exception('YAPI Error')

    def _initModule(self):
        pass

    def _log(self, message):
        print('(%s) %s' % (self.uid, message))
