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

echo "Install dbus-seplos"
# remount rw
bash /opt/victronenergy/swupdate-scripts/remount-rw.sh

# remove old symlinks
rm -rf /opt/victronenergy/service/dbus-cpu
rm -rf /opt/victronenergy/dbus-cpu

# make sure all necessary files are executable
chmod +x /data/etc/dbus-cpu/scripts/*.sh
chmod +x /data/etc/dbus-cpu/src/*.py
chmod +x /data/etc/dbus-cpu/service/run
chmod +x /data/etc/dbus-cpu/service/log/run

# install by copying files
mkdir /opt/victronenergy/service/dbus-cpu
cp -rf /data/etc/dbus-cpu/service/* /opt/victronenergy/service/dbus-cpu
mkdir /opt/victronenergy/dbus-cpu
cp -rf /data/etc/dbus-cpu /opt/victronenergy

if [$1 == "gui"];
then
    # install gui qml
    bash /data/etc/dbus-cpu/scripts/install-gui.sh
    echo "Installed GUI"

# add install-script to rc.local to be ready for firmware update
filename=/data/rc.local
if [ ! -f "$filename" ]; then
    echo "#!/bin/bash" > "$filename"
    chmod 755 "$filename"
fi

if ! grep -qxF "bash /data/etc/dbus-cpu/scripts/install.sh" $filename;
then
    echo "bash /data/etc/dbus-cpu/scripts/install.sh" >> $filename
fi

echo "Installed dbus-cpu"
