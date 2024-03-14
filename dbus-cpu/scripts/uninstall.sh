#!/bin/bash

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

echo "Install dbus-cpu"

# remove copied files
rm -rf /service/dbus-cpu

# remove logs
rm -rf /var/log/dbus-cpu

rm -rf /opt/victronenergy/service/dbus-cpu
rm -rf /opt/victronenergy/dbus-cpu

# restore GUI changes
# bash /data/etc/dbus-cpu/scripts/restore-gui.sh

# remove install-script from rc.local
filename=/data/rc.local
if [ -f "$filename" ];
then
  sed -i "/bash \/data\/etc\/dbus-cpu\/scripts\/install.sh/d" $filename
fi

echo "Uninstalled dbus-cpu"

