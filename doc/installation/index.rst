Driver installation
===================

.. warning:: The driver is only tested with Venus OS > 3.00 and < v3.3. It will
             not work with Venus OS other than that.

Install or update over SSH
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. note:: Requires root access.

Log into your Venus OS device using a SSH client like Putty or bash and run
these commands to start the installer including the changes to the GUI:

.. code-block:: bash

   wget -O /tmp/install.sh https://raw.githubusercontent.com/mworion/dbus-seplos/master/install-target-gui.sh
   bash /tmp/install.sh


For those, who want to just use the driver without impacting the GUI, please use the 
headless installation

.. code-block:: bash

   wget -O /tmp/install.sh https://raw.githubusercontent.com/mworion/dbus-seplos/master/install-target-headless.sh
   bash /tmp/install.sh


The installer will download the latest released version of the driver and installs
it on your system. The location of the install will be in

.. code-block:: bash

   /data/etc/dbus-cpu

The installer will also create a service file for the driver and enable it. All
the installations to the system will be done from this origin with symlinks.

In addition the installer will add lines to

.. code-block:: bash

   /data/rc.local

to keep the installation persistent over reboots und firmware updates of the venus
system. Uninstall will remove this entry.

Last the installer will backup / add some files to the GUI system to make the GUI
aware of the more detailed information provided by dbus-cpu. Uninstall will
remove these files and changes.

You could customize the installation by editing the script. All scripts are located
in the same directory:

.. code-block:: bash

   /data/etc/dbus-cpu/scripts

Settings
^^^^^^^^
Basically no settings could be made as the driver is designed to be plug and play.

Behavior
^^^^^^^^
dbus-cpu will start automatically after installation. It will read CPU stats
(usage, memory) from /proc/stat and /proc/meminfo and publish them on the D-Bus.

