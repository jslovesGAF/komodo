#!/bin/bash

echo "------ Running all neccesssary installations for KOMODO ------"

sudo apt-get update
sudo apt-get install idle3
sudo apt-get install python-is-python3

#Wappalzyer 
python3 -m pip install python-Wappalyzer

#Art - for tprint
sudo pip install art==5.7
sudo pip install termcolor

#lolcat
sudo pip install lolcat

#testssl 
cd misc
git clone --depth 1 https://github.com/drwetter/testssl.sh.git
cd ..

#Dotdotpwn 
sudo apt install dotdotpwn

#Nuclei
sudo apt install nuclei
nuclei

#CheckURL
cd misc
git clone https://github.com/UndeadSec/checkURL.git
cd ..

#Gobuster
sudo apt install gobuster

#Wmap Database Connect
#Start PostgreSQL Service
sudo service postgresql start
#initialise MS PostgreSQL DB
sudo msfdb init

#wpscan update database
sudo wpscan --update

#install txt2html 
sudo apt install txt2html
