#!/bin/bash

if [ -e CCS/Debug/BatterylessMic.hex ]
then
	cd mspFlasher/Source
	make
	cd ..

	export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH

	clear
	for i in /dev/ttyACM*; do
		echo Flashing $i;
		./MSP430Flasher -i ${i#/dev/} -w ../CCS/Debug/BatterylessMic.hex -v -s -z [VCC];
	done
	read -p "Press any key to continue..."

else
    echo "File 'CCS/Debug/BatterylessMic.hex' not found in Debug directory!"
fi
