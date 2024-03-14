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
        self.prev_cpu_time = 0
        self.prev_user_time = 0
        self.prev_system_time = 0
        self.prev_idle_time = 0
        self.prev_base_time = 0

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
        self.dbusservice.add_path('/CPU_Load_User', None, writeable=True)
        self.dbusservice.add_path('/CPU_Load_System', None, writeable=True)
        self.dbusservice.add_path('/CPU_IDLE', None, writeable=True)
        self.dbusservice.add_path('/DeviceName', 'DBUS-CPU')

        GLib.timeout_add(POLL_TIME, self.update)

    def cpu_percentage_loop(self):
        """
        :return:
        """
        val = get_cpu_times()
        if val is None:
            return 0, 0, 0
        user_time, system_time, idle_time, base_time = val
        cpu_time = user_time + system_time
        diff_cpu_time = cpu_time - self.prev_cpu_time
        diff_user_time = user_time - self.prev_user_time
        diff_system_time = system_time - self.prev_system_time
        diff_idle_time = system_time - self.prev_idle_time
        diff_base_time = base_time - self.prev_base_time
        cpu_percentage = 100.0 * diff_cpu_time / (diff_cpu_time + diff_base_time)
        user_percentage = 100.0 * diff_user_time / (diff_user_time + diff_base_time)
        system_percentage = 100.0 * diff_system_time / (diff_system_time + diff_base_time)
        idle_percentage = 100.0 * diff_idle_time / (diff_idle_time + diff_base_time)
        self.prev_cpu_time = cpu_time
        self.prev_base_time = base_time
        logger.debug(f'CPU load: {cpu_percentage:2.1f} %, '
                     f'CPU user: {user_percentage:2.1f} %, '
                     f'CPU system: {user_percentage:2.1f} %, '
                     f'CPU idle: {idle_percentage:2.1f} %')
        return cpu_percentage, user_percentage, system_percentage, idle_percentage

    def update(self):
        with self.dbusservice as dbus:
            cpu, user, system, idle = self.cpu_percentage_loop()
            dbus['/CPU_Load'] = cpu
            dbus['/CPU_Load_User'] = user
            dbus['/CPU_Load_System'] = system
            dbus['/CPU_IDLE'] = idle
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
