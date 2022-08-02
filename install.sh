#!/bin/bash

echo "------ Running all neccesssary installations for KOMODO ------"

#Wappalzyer 
python3 -m pip install python-Wappalyzer

#Art - for tprint
pip install art==5.7
pip install termcolor

#testssl 
git clone --depth 1 https://github.com/drwetter/testssl.sh.git

#Dotdotpwn 
sudo apt install dotdotpwn

#CheckURL
git clone https://github.com/UndeadSec/checkURL.git

#CMSeeK
git clone https://github.com/Tuhinshubhra/CMSeeK
cd CMSeeK
pip install -r requirements.txt

cd ..

#Wmap Database Connect
#Start PostgreSQL Service
sudo service postgresql start
#initialise MS PostgreSQL DB
sudo msfdb init

#wpscan update database
sudo wpscan --update

#install txt2html 
sudo apt install txt2html
