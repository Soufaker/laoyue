#!/bin/bash
chmod 777 ./inifile/lousao/nuclei
chmod 777 ./inifile/naabu/naabu
chmod 777 ./inifile/httpx/httpx
chmod 777 ./inifile/lousao/fscan
chmod 777 ./inifile/ffuf/ffuf
chmod 777 ./inifile/subfinder/subfinder
sed -i "s/\r//" check_nohup_size.sh
chmod 777 check_nohup_size.sh
chmod 777 update.sh
systemctl enable docker.service
chmod 777 ./inifile/bypass403/f403_linux_amd64
#cp ./inifile/lousao/nuclei-templates/ /root/
#sudo apt-get install yum
#yum  -y install mlocate;updatedb
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
yum -y install bind-utils
yum install libpcap-devel
cd /usr/lib64/;sudo ln -s libpcap.so.1.5.3 libpcap.so.0.8