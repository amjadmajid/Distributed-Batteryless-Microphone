Installation Script for MSP-FET430UIF Flash Emulation Tool
----------------------------------------------------------

The shell script in this package creates the necessary
udev rules for the Texas Instruments MSP-FET430UIF USB 
Flash Emulation Tool.

For successful installation, you need to run the script
with superuser privileges. In the directory of the script
run the following command:
sudo ./msp430uif_install.sh --install

The script will also reinit/restart the udev service.
