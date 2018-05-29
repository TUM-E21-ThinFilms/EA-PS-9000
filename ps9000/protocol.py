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

import slave
import logging
import time
import e21_util

from slave.protocol import Protocol
from slave.transport import Timeout

from e21_util.lock import InterProcessTransportLock
from e21_util.error import CommunicationError

class EAPS9000Protocol(Protocol):
    def __init__(self, logger=None):

        if logger is None:
            logger = logging.getLogger(__name__)
            logger.addHandler(logging.NullHandler())

        self.logger = logger

    def set_logger(self, logger):
        self.logger = logger

    def send_message(self, transport, message):        

        try:
            transport.write(message + "\r\n")
        except slave.transport.Timeout:
            raise CommunicationError('Received timeout.')

    def read_response(self, transport, max_frames=2):
        try:
            response = transport.read_until("\r\n")
            self.logger.debug('Response "%s"', response)
        except slave.transport.Timeout:
            raise CommunicationError('Could not read response: No delemiter CR LF received. Timeout')

        return response

    def query(self, transport, msg):
        with InterProcessTransportLock(transport):
            self.logger.debug('Query message "%s"', msg)
            self.send_message(transport, msg)
            response = self.read_response(transport)
            return response

    def clear(self, transport):
        with InterProcessTransportLock(transport):
            self.logger.debug("Clearing buffer...")
            try:
                while True:
                    transport.read_bytes(25)
            except:
                pass

    def write(self, transport, msg):
        with InterProcessTransportLock(transport):
            self.logger.debug('Send message "%s"', msg)
            self.send_message(transport, msg)
