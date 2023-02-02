#!/bin/bash
git clone https://github.com/maurosoria/dirsearch.git ./inifile/dirsearch-master
yum -y install bind-utils
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

