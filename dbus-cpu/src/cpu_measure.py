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

def get_cpu_times():
    """
    :return:
    """
    with open("/proc/stat") as procfile:
        cpustats = procfile.readline().split()

    if cpustats[0] != 'cpu':
        return None

    user_time = int(cpustats[1])    # time spent in user space
    nice_time = int(cpustats[2])    # 'nice' time spent in user space
    system_time = int(cpustats[3])  # time spent in kernel space

    idle_time = int(cpustats[4])    # time spent idly
    user_time = user_time + nice_time
    base_time = sum(int(x) for x in cpustats[1:7])

    return user_time, system_time, idle_time, base_time
