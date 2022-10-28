# KOMODO All-in-one Hacking Tool
# Joshua Sloves / Ethan Tomford

####### SAMPLE TARGET google-gruyere.appspot.com/593948396113602183495718301495133174940
####### SAMPLE TARGET scanme.nmap.org
#######

import os, warnings, sys, re, datetime, socket, subprocess, urllib.request, json, requests, time
from termcolor import colored, cprint
from art import *
from Wappalyzer import Wappalyzer, WebPage
from bs4 import BeautifulSoup

key = ""
configType = "None"
scopeURL = ""

target ='google.com'
output = 'google.html'
tool = 'nmap'
#seperator = str("<p><br></p>")
x = datetime.datetime.now()
current_time = "Scan Results: "+ str(x.strftime("%x %I:%M%p"))
replacements = {'NULL':target,'TIME':current_time}

def write(soup):
    with open(output,'w') as f:
        f.write(str(soup))
        
def createHTML():
    with open('/home/kali/komodo/html/default.html') as infile, open(output, 'w') as outfile:
        for line in infile:
            for src, target in replacements.items():
                line = line.replace(src, target)
            outfile.write(line)
    return output
    
def main():
    
    output = createHTML()
    with open(output) as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        response = input("How many tools would you like to run? ")

        headerTag = soup.find('h1')
        initialTags =['\n','<button name="target" type="button" class="collapsible">'+current_time+'</button>','\n',
                     '<div name="target" class="content">','<p>Please see scan results below.</p>','\n']

        divName = 'tool0'
        for i in range(int(response)):
            divName = 'tool'+str(i)
            toolTags=['\n','<button name='+divName+' type="button" class="collapsible">'+tool+'</button>','\n',
                      '<div name ='+divName+' class="content"><p>blah blah blah</p>','</div>','<br>','\n']

            for k in range(len(toolTags)):
                initialTags.append(toolTags[k])
            initialStr = "".join(initialTags)
         
        #headerTag.insert_after(BeautifulSoup(initialStr, 'html.parser'))
        headerList = soup.find_all(re.compile('^h[1-6]$'))
        headerStr = str(headerList.pop())
        headerStr = headerStr[2:3]
        print('headerStr: '+headerStr)
        newHeader = soup.find(headerStr)
        #newHeader.insert_after(BeautifulSoup(initialStr, 'html.parser'))
        print('newHeader: '+str(newHeader))
        write(soup)
        
        
if __name__ == '__main__':
    main()

##    headerTag = soup.find('h1')
##    a_tags =['<button name="target" type="button" class="collapsible">'+'SCAN 1'+'</button>',
##             '<div class="content"><p>Please see scan results below.</p>',
##             '<button name="tool" type="button" class="collapsible">NMAP</button>',
##             '<div name ="nmap" class="content"><p>blah blah blah</p>','</div>','<p><br></p>','</div>']
##    a_str = "".join(a_tags)
##    headerTag.insert_after(BeautifulSoup(a_str, 'html.parser'))
##
##    buttonTag = soup.find("div", {"name": "nmap"})
##    print(buttonTag)
##    a_tags =['<button type="button" class="collapsible">SQL INJECTION TOOL</button>',
##             '<div class="content"><p>blah blah blah</p>','</div>','<p><br></p>','</div>']
##    a_str = "".join(a_tags)
##    buttonTag.insert_after(BeautifulSoup(a_str, 'html.parser'))
##_______________
##    buttonTag = soup.find("div", {"class": "content"})
##    a_tags =['<button type="button" class="collapsible">'+'SCAN 2'+'</button>',
##             '<div class="content"><p>Please see scan results below.</p>',
##             '<button type="button" class="collapsible">TRACEROUTE</button>',
##             '<div class="content"><p>blah blah blah</p>','</div>','<p><br></p>','</div>']
##    a_str = "".join(a_tags)
##    buttonTag.insert_after(BeautifulSoup(a_str, 'html.parser'))
##_______________
##
##    buttonTag2 = soup.find("div", {"class": "content"})
##    a_tags =['<button type="button" class="collapsible">'+'SCAN 3'+'</button>',
##             '<div class="content"><p>Please see scan results below.</p>',
##             '<button type="button" class="collapsible">WHOIS</button>',
##             '<div class="content"><p>blah blah blah</p>','</div>','<p><br></p>','</div>']
##    a_str = "".join(a_tags)
##    buttonTag2.insert_after(BeautifulSoup(a_str, 'html.parser'))
