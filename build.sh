#!/bin/bash
git clone https://github.com/maurosoria/dirsearch.git ./inifile/dirsearch-master
chmod 777 ./inifile/lousao/nuclei
yum -y install bind-utils
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt


