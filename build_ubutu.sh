#!/bin/bash
chmod 777 ./inifile/lousao/nuclei
chmod 777 ./inifile/naabu/naabu
chmod 777 ./inifile/httpx/httpx
chmod 777 ./inifile/lousao/fscan
chmod 777 ./inifile/ffuf/ffuf
chmod 777 ./inifile/subfinder/subfinder
sed -i "s/\r//" check_nohup_size.sh
chmod 777 check_nohup_size.sh
systemctl enable docker.service
chmod 777 ./inifile/bypass403/f403_linux_amd64
sudo apt-get update
sudo apt-get install python3-pip
pip3 install -r requirements.txt
sudo apt-get install dnsutils
sudo apt-get install libpcap-dev
sudo ln -s /usr/lib/x86_64-linux-gnu/libpcap.so.1 /usr/lib/x86_64-linux-gnu/libpcap.so.0.8