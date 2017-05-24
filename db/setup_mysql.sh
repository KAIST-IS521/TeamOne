#!/bin/bash
root_password=$(cat ./root.pw)
echo PURGE | sudo debconf-communicate mysql-server
echo PURGE | sudo debconf-communicate mysql-server-5.5
echo "mysql-server mysql-server/root_password password ${root_password}" | sudo debconf-set-selections
echo "mysql-server mysql-server/root_password_again password ${root_password}" | sudo debconf-set-selections
sudo apt-get -y install mysql-server
mysql -uroot -p${root_password} < create_bankdb.sql
./get_pubkey.sh
python3 reg_pubkey.py
python3 reg_admin.py
echo PURGE | sudo debconf-communicate mysql-server
echo PURGE | sudo debconf-communicate mysql-server-5.5
