#!/bin/sh

sudo apt-get install python-dev

git clone https://github.com/isislovecruft/python-gnupg.git
cd python-gnupg
sudo make install
