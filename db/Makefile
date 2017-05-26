all: mysql

mysql:
	sudo apt-get update
	./setup_mysql.sh
	sudo apt-get -y install python3-pip
	sudo pip3 install PyMySQL
	sudo pip3 install tabulate

.PHONY: all mysql

