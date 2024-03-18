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

echo "o-o   o--o  o   o  o-o            "
echo "|  \  |   | |   | |               "
echo "|   O O--o  |   |  o-o            "
echo "|  /  |   | |   |     |           "
echo "o-o   o--o   o-o  o--o            "
echo "                                  "
echo "                                  "
echo "  o-o  o--o  o   o                "
echo " |     |   | |   |                "
echo " |     O--o  |   |                "
echo " |     |     |   |                "
echo " o--o  o      o-o                 "
echo "                                  "
echo "Download latest dbus-cpu"
curl -s https://api.github.com/repos/mworion/dbus-cpu/releases/latest | grep "browser_download_url.*gz" | cut -d : -f 2,3 | tr -d \" | wget -qi -
tar -xvzf dbus-cpu.tar.gz
rm -rf /data/etc/dbus-cpu
mv ./dbus-cpu /data/etc
rm dbus-cpu.tar.gz
bash /data/etc/dbus-cpu/scripts/install.sh withgui
echo "Download and copy dbus-cpu done"
