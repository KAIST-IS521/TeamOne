all: mysql

mysql:
	sudo apt-get update
	sudo apt-get -y install python3-pip
	./setup_mysql.sh
	sudo pip3 install tabulate

.PHONY: all mysql

