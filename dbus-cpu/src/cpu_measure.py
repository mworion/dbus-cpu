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

from cpu_utils import logger


def get_cpu_times():
    """
    :return:
    """
    with open("/proc/stat") as procfile:
        cpustats = procfile.readline().split()

    if cpustats[0] != 'cpu':
        raise ValueError("First line of /proc/stat not recognised")

    user_time = int(cpustats[1])    # time spent in user space
    nice_time = int(cpustats[2])    # 'nice' time spent in user space
    system_time = int(cpustats[3])  # time spent in kernel space

    idle_time = int(cpustats[4])    # time spent idly
    iowait_time = int(cpustats[5])    # time spent waiting is also doing nothing

    time_doing_things = user_time + nice_time + system_time
    time_doing_nothing = idle_time + iowait_time

    return time_doing_things, time_doing_nothing
