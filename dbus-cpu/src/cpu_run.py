############################################################
# -*- coding: utf-8 -*-
#
#  o-o   o--o  o   o  o-o
#  |  \  |   | |   | |
#  |   O O--o  |   |  o-o
#  |  /  |   | |   |     |
#  o-o   o--o   o-o  o--o
#
#
#   o-o  o--o  o   o
#  |     |   | |   |
#  |     O--o  |   |
#  |     |     |   |
#  o--o  o      o-o
#
# python-based service for victron cerbo > v3.00
#
# (c) 2024 by mworion
# Licence MIT
#
###########################################################

import time
import os
import sys
import platform
from cpu_utils import logger
from cpu_utils import POLL_TIME
from cpu_utils import DRIVER_VERSION
from cpu_measure import get_cpu_times

sys.path.insert(1,
                os.path.join(os.path.dirname(__file__),
                             '/opt/victronenergy/dbus-systemcalc-py/ext/velib_python'))
from vedbus import VeDbusService
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib


class DbusCPUService(object):
    def __init__(self, servicename, deviceinstance, productname='DBUS-CPU',
                 connection='None', productid=0):
        """
        :param servicename:
        :param deviceinstance:
        :param productname:
        :param connection:
        :param productid:
        """
        self.dbusservice = VeDbusService(servicename)
        self.prev_time_doing_things = 0
        self.prev_time_doing_nothing = 0

        logger.debug("%s /DeviceInstance = %d" % (servicename, deviceinstance))

        # Create the management objects, as specified in the ccgx dbus-api document
        self.dbusservice.add_path('/Mgmt/ProcessName', __file__)
        self.dbusservice.add_path('/Mgmt/ProcessVersion', 'Python ' + platform.python_version())
        self.dbusservice.add_path('/Mgmt/Connection', connection)

        # Create the mandatory objects
        self.dbusservice.add_path('/DeviceInstance', deviceinstance)
        self.dbusservice.add_path('/ProductId', productid)
        self.dbusservice.add_path('/ProductName', productname)
        self.dbusservice.add_path('/FirmwareVersion', DRIVER_VERSION)
        self.dbusservice.add_path('/HardwareVersion', 0)
        self.dbusservice.add_path('/Connected', 1)
        self.dbusservice.add_path('/CPU_Load', None, writeable=True)
        self.dbusservice.add_path('/DeviceName', 'DBUS-CPU')

        GLib.timeout_add(POLL_TIME, self.update)

    def cpu_percentage_loop(self):
        """
        :return:
        """
        time_doing_things, time_doing_nothing = get_cpu_times()
        diff_time_doing_things = time_doing_things - self.prev_time_doing_things
        diff_time_doing_nothing = time_doing_nothing - self.prev_time_doing_nothing
        cpu_percentage = 100.0 * diff_time_doing_things / (
                    diff_time_doing_things + diff_time_doing_nothing)
        self.prev_time_doing_things = time_doing_things
        self.prev_time_doing_nothing = time_doing_nothing
        logger.debug(f'CPU load: {cpu_percentage:2.1f} %')
        return cpu_percentage

    def update(self):
        with self.dbusservice as dbus:
            dbus['/CPU_Load'] = self.cpu_percentage_loop()
        return True

    @staticmethod
    def handle_changed_value(path, value):
        """
        :param path:
        :param value:
        :return:
        """
        logger.debug("someone else updated %s to %s" % (path, value))
        return True


def main():
    """
    """
    DBusGMainLoop(set_as_default=True)

    cpu_load_service = DbusCPUService(
        servicename='com.victronenergy.cpu',
        deviceinstance=0)

    main_loop = GLib.MainLoop()
    logger.info('cpu-dbus started on port')

    try:
        main_loop.run()
    except KeyboardInterrupt:
        pass
    logger.info('cpu-dbus stopped')


if __name__ == "__main__":
    main()
