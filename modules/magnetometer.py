import sys
import os
from base import Base

here = os.path.dirname( os.path.abspath(__file__) )
sys.path.append(os.path.join(here, '..', 'yoctolib_python', 'Sources'))

from yocto_magnetometer import *

class Magnetometer(Base):
    def get_value(self):
        value = {}
        for ax in ('x', 'y', 'z'):
            value[ax] = self._get_ax_value(ax)

        self.last_value = value

        return self.last_value

    def _initModule(self):
        magnetometer = YMagnetometer.FindMagnetometer('%s.magnetometer' % self.uid)
        if magnetometer.set_resolution(0.001) == YAPI.SUCCESS and magnetometer.get_resolution() == 0.001:
            self._log('Succesfully increased resolution of magnetometer.')

        self.module = magnetometer
        self.last_values = {'x': 0, 'y': 0, 'z': 0}

    def _get_ax_value(self, axis):
        if axis not in ('x', 'y', 'z'): return None

        return getattr(self.module, 'get_%sValue' % axis)()
