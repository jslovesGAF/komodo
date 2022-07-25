#!/bin/bash

echo "------ Running all neccesssary installations for KOMODO ------"

#Wappalzyer 
python3 -m pip install python-Wappalyzer

#Art - for tprint
pip install art==5.7

#testssl 
git clone --depth 1 https://github.com/drwetter/testssl.sh.git

#Dotdotpwn 
sudo apt install dotdotpwn

#CheckURL
git clone https://github.com/UndeadSec/checkURL.git

#Python Dirbuster
git clone https://github.com/coderj001/python-dirbuster.git
cd python-dirbuster/
pip install -r requirements.txt
cd ..
echo "------ Errors regarding 'urllib' can be disregarded. ------"
