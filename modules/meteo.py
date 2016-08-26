import sys
import os
from base import Base

here = os.path.dirname( os.path.abspath(__file__) )
sys.path.append(os.path.join(here, '..', 'yoctolib_python', 'Sources'))

from yocto_temperature import *
from yocto_humidity import *
from yocto_pressure import *

class Meteo(Base):
    def get_value(self):
        value = {'T': self.temperature.get_currentValue(),
                 'RH': self.humidity.get_currentValue(),
                 'p': self.pressure.get_currentValue()}

        self.last_value = value

        return self.last_value

    def _initModule(self):
        self.temperature = YTemperature.FindTemperature('%s.temperature'  % self.uid)
        self.humidity    = YHumidity.FindHumidity('%s.humidity' % self.uid)
        self.pressure    = YPressure.FindPressure('%s.pressure'  % self.uid)

        self.last_values = {'T': 0, 'RH': 0, 'p': 0}
