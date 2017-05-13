#!/bin/sh
mkdir -p pubkeys
while read -r line
do
    wget https://raw.githubusercontent.com/KAIST-IS521/2017-Spring/master/students/${line}.pub -O pubkeys/${line}.pub
done < "github_id.list"

