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

echo "Install GUI"
# backup old PageSettingsFirmware.qml once. New firmware upgrade will remove the backup
if [ ! -f /opt/victronenergy/gui/qml/PageSettingsFirmware.qml.backup ]; then
    cp /opt/victronenergy/gui/qml/PageSettingsFirmware.qml /opt/victronenergy/gui/qml/PageSettingsFirmware.qml.backup
fi

# copy new PageBattery.qml
cp /data/etc/dbus-cpu/qml/PageSettingsFirmware.qml /opt/victronenergy/gui/qml/
# copy new PageBatteryCellVoltages
cp /data/etc/dbus-cpu/qml/PageSettingsCPU.qml /opt/victronenergy/gui/qml/


bash /data/etc/dbus-seplos/scripts/restart-gui.sh

echo "GUI installed"