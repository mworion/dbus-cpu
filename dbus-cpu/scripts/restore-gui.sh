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

# restore original backup
if [ -f /opt/victronenergy/gui/qml/PageSettingsFirmware.qml.backup ]; then
    echo "Restoring PageSettingsFirmware.qml..."
    cp -f /opt/victronenergy/gui/qml/PageSettingsFirmware.qml.backup /opt/victronenergy/gui/qml/PageSettingsFirmware.qml
    bash /data/etc/dbus-cpu/scripts/restart-gui.sh
    echo "PageSettingsFirmware.qml was restored."
fi

