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


def get_memory_usage():
    """
    :return:
    """
    with open("/proc/meminfo") as procfile:
        mem_stats = procfile.readlines()

    if mem_stats[0].split()[0] != 'MemTotal:':
        return None

    mem_total = int(int(mem_stats[0].split()[1]) / 1024)
    mem_free = int(int(mem_stats[1].split()[1]) / 1024)
    mem_cached = int(int(mem_stats[3].split()[1]) / 1024)
    mem_buffers = int(int(mem_stats[4].split()[1]) / 1024)
    mem_used = mem_total - (mem_free + mem_buffers + mem_cached)

    return mem_total, mem_free, mem_cached, mem_buffers, mem_used
