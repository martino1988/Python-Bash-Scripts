#!/bin/bash

if [ "$#" == 2 ]
then
echo "... file transmitting ..."
sshpass -p 'password' scp $1 pi@192.168.xx.xx:/home/pi/RetroPie/roms/$2
echo ""
echo "--- FINISHED ---"
else
echo -e "\033[31mSyntax ERROR!\033[0m"
echo "Syntax: bash upload.sh <path/to/file> <emulator>"
echo -e "Example: \033[45m\033[1mbash upload.sh /home/user/Downloads/Spiel1.bin psx\033[0m"
fi
