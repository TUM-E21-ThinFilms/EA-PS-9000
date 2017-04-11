# Copyright (C) 2016, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from slave.driver import Driver, Command
from slave.types import Mapping, Float, String, Integer, Boolean, SingleType
from protocol import EAPS9000Protocol

class EAPS9000Driver(Driver):

    def __init__(self, transport, protocol=None):
        if protocol is None:
            protocol = EAPS9000Protocol()
        
        self.thread = None
        
        super(EAPS9000Driver, self).__init__(transport, protocol)

    def _write(self, message):
        self._protocol.write(self._transport, message)

    def _query(self, message):
        return self._protocol.query(self._transport, message)

    def clear(self):
        self._protocol.clear(self._transport)

    def get_identification(self):
        return str(self._query('*IDN?'))

    def reset(self):
        self._write('*RST')

    def set_voltage(self, voltage):
        if not isinstance(voltage, (long, int)):
            raise ValueError("Expected voltage to be an integer")

        self._write('VOLT '+ str(voltage))

    def get_voltage(self):
        return float(self._query('VOLT?'))

    def set_current(self, current):
        if not isinstance(current, (long, int)):
            raise ValueError("Expected current to be an integer")

        self._write('CURR '+ str(current))

    def get_current(self):
        return float(self._query('CURR?'))

    def measure_voltage(self):
        return float(self._query('MEAS:VOLT?'))

    def measure_current(self):
        return float(self._query('MEAS:CURR?'))

    def set_output(self, bool):
        if not bool in [0, 1]:
            raise ValueError("Expected bool to be a boolean value")

        # yeah, the series PS 9000 (old) has this boolean inverted...
        self._write('OUTP '+ str(int(not bool)))

    def get_output(self):
        return not bool(self._query('OUTP?'))

