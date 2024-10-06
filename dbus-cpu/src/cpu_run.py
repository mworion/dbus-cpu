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
from cpu_measure import get_cpu_times, get_memory_usage, get_load_avg

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
        self.dbusservice.add_path('/CPU_Memory_Total', None, writeable=True)
        self.dbusservice.add_path('/CPU_Memory_Free', None, writeable=True)
        self.dbusservice.add_path('/CPU_Memory_Cached', None, writeable=True)
        self.dbusservice.add_path('/CPU_Memory_Buffers', None, writeable=True)
        self.dbusservice.add_path('/CPU_Memory_Used', None, writeable=True)
        self.dbusservice.add_path('/CPU_AVG_1', None, writeable=True)
        self.dbusservice.add_path('/CPU_AVG_5', None, writeable=True)
        self.dbusservice.add_path('/CPU_AVG_15', None, writeable=True)
        self.dbusservice.add_path('/DeviceName', 'DBUS-CPU')

        GLib.timeout_add(POLL_TIME, self.update)

    def cpu_percentage_loop(self):
        """
        """
        val = get_cpu_times()
        if val is None:
            return 0, 0, 0, 0

        user_time, system_time, idle_time, base_time = val
        cpu_time = user_time + system_time
        diff_cpu_time = cpu_time - self.prev_cpu_time
        diff_user_time = user_time - self.prev_user_time
        diff_system_time = system_time - self.prev_system_time
        diff_idle_time = idle_time - self.prev_idle_time
        diff_base_time = base_time - self.prev_base_time
        cpu_percentage = 100.0 * diff_cpu_time / (diff_cpu_time + diff_base_time)
        user_percentage = 100.0 * diff_user_time / (diff_user_time + diff_base_time)
        system_percentage = 100.0 * diff_system_time / (diff_system_time + diff_base_time)
        idle_percentage = 100.0 * diff_idle_time / (diff_idle_time + diff_base_time)
        self.prev_cpu_time = cpu_time
        self.prev_base_time = base_time
        self.prev_user_time = user_time
        self.prev_system_time = system_time
        self.prev_idle_time = idle_time
        return cpu_percentage, user_percentage, system_percentage, idle_percentage

    @staticmethod
    def cpu_memory_loop():
        """
        """
        val = get_memory_usage()
        if val is None:
            return 0, 0, 0, 0, 0

        return val

    @staticmethod
    def cpu_load_avg_loop():
        """
        """
        val = get_load_avg()
        if val is None:
            return 0, 0, 0

        return val

    def update(self):
        """
        """
        with self.dbusservice as dbus:
            cpu, user, system, idle = self.cpu_percentage_loop()
            total, free, cached, buffers, used = self.cpu_memory_loop()
            avg_1, avg_5, avg_15 = self.cpu_load_avg_loop()
            dbus['/CPU_Load'] = cpu
            dbus['/CPU_Load_User'] = user
            dbus['/CPU_Load_System'] = system
            dbus['/CPU_IDLE'] = idle
            dbus['/CPU_Memory_Total'] = total
            dbus['/CPU_Memory_Free'] = free
            dbus['/CPU_Memory_Cached'] = cached
            dbus['/CPU_Memory_Buffers'] = buffers
            dbus['/CPU_Memory_Used'] = used
            dbus['/CPU_AVG_1'] = avg_1
            dbus['/CPU_AVG_5'] = avg_5
            dbus['/CPU_AVG_15'] = avg_15

        return True

    @staticmethod
    def handle_changed_value(path, value):
        """
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
    logger.info('cpu-dbus started')

    try:
        main_loop.run()
    except KeyboardInterrupt:
        pass
    logger.info('cpu-dbus stopped')


if __name__ == "__main__":
    main()
