#!/bin/bash
git clone https://github.com/maurosoria/dirsearch.git ./inifile/dirsearch-master
chmod 777 ./inifile/lousao/nuclei
#cp ./inifile/lousao/nuclei-templates/ /root/
#sudo apt-get install yum
yum -y install bind-utils
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt


