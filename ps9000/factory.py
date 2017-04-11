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


from e21_util.logging import get_sputter_logger
from e21_util.transport import Serial
from protocol import EAPS9000Protocol
from driver import EAPS9000Driver

class PS9000Factory:
    def get_logger(self):
        return get_sputter_logger('EA PS 9000 series', 'ps9000.log')
    
    def create_powersupply(self, device="/dev/ttyUSB17", logger=None):
        if logger is None:
            logger = self.get_logger()
            
        protocol = EAPS9000Protocol(logger=logger)
        return EAPS9000Driver(Serial(device, 9600, 8, 'N', 2, 1), protocol)
