# KOMODO All-in-one Hacking Tool
# Joshua Sloves / Ethan Tomford

####### SAMPLE TARGET https://google-gruyere.appspot.com/359771356088723951563265865954951743836/
####### SAMPLE TARGET scanme.nmap.org
#######

import os, warnings, sys, re, datetime
from termcolor import colored
from art import *
from Wappalyzer import Wappalyzer, WebPage
import socket

class EXPLOITS:
    def __init__(self):
        self.url = url
        self.output = output

    def MSWmap(self):
        global url
        global output
        url = self.url
        orig = str(self.url)
        output = self.output

        try:
            print('Lauching WMAP Scanner through Metasploit on {}'.format(self.url))
            os.chdir('html')
            #regular expression to replace all link issues i.e. / & .
            rep = {"https://": "", "http://": ""} #define desired replacements here

            #these three lines do the replacing
            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            new = (pattern.sub(lambda m: rep[re.escape(m.group(0))], orig))
            ip = socket.gethostbyname(new)
            
            cmd = str('msfconsole -q -p wmap -x '+"'"+'wmap_sites -d 0;wmap_targets -c;wmap_sites -a '+ip+';wmap_targets -d 0;wmap_run -p /home/kali/.msf4/fav_modules;exit'+"'"+" | txt2html -extract -8 >> {file}".format(file=output))
            os.system(cmd)
            os.chdir('..')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))
                      
class TECHNOLOGY_LOOKUP:
    def __init__(self):
        self.url = url
        self.output = output

    # Discover WebApp underlying technology
    def wappalyzer(self):
        global output
        output = self.output

        try:   
            os.chdir('html')
            with open(output, "a") as f:
                webpage = WebPage.new_from_url(str(self.url))
                warnings.filterwarnings('ignore', message="""Caught 'unbalanced parenthesis at position 119' compiling regex""", category=UserWarning )

                wappalyzer = Wappalyzer.latest()
                print(wappalyzer.analyze_with_versions_and_categories(webpage))

                f.write(str(wappalyzer.analyze_with_versions_and_categories(webpage)))
                print('Running Wappalyzer technology detector on {}'.format(self.url))
                f.close()
            os.chdir('..')
            print('Wappalyzer Successfully Executed')

        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))
        
    def cmseek(self):
        global url
        global output
        url = self.url
        output = self.output

        try:
            print('Lauching CMSeeK Detection on {}'.format(self.url))
            os.chdir('CMSeeK')
            cmd = str('python cmseek.py -u {url} | txt2html -extract -8 >> ../html/{file} '.format(url=self.url,file=self.output))
            os.system(cmd)
            os.chdir('..')
            print('CMSeeK Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))
  
class VULNERABILITY:
    def __init__(self):
        self.url = url

    # Open Source Vulnerability Scanner
    def nikto(self):
        global url
        url = self.url
        
        try:
            os.chdir('html')
            print('Lauching Nikto Vulnerability Scanner on {}'.format(self.url))
            cmd = str('nikto -h {url} | txt2html -extract -8 >> {file} '.format(url=self.url,file=self.output))
            os.system(cmd)
            print('Nikto Successfully Executed')
            os.chdir('..')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))
            
    # Wordpress WebApp Vulnerability Scanner
    def WPScan(self):
        global url
        url = self.url
        
        try:
            os.chdir('html')            
            print('Running WPScan Against {}'.format(self.url))
            cmd = str('wpscan --url {url} --no-update --no-banner | txt2html -extract -8 >> {file}'.format(url=self.url,file=self.output))
            os.system(cmd)
            os.chdir('..')
            print('WPScan Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

    # Directory Traversal Exploiter
    def dotdotpwn(self):
        global url
        url = self.url
        orig = str(self.url)
        
        try:
            os.chdir('html')
            if 'https://' in orig:
                new = orig.replace('https://',"",1)
            elif 'http://' in orig:
                new = orig.replace('http://',"",1)
                
            print('Running DotDotPwn Against {}'.format(new))
            cmd = str('dotdotpwn -m http -h {url} | txt2html -extract -8 >> {file}'.format(url=new, file=output))
            os.system(cmd)
            os.chdir('..')
            print('DotDotPwn Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

class INFORMATION_GATHERING:
    def __init__(self):
        self.url = url

    # Network Mapper
    def nmap(self):
        global url
        url = self.url

        try:
            os.chdir('html')
            print("Launching aggressive NMAP Scan\n")
            orig = str(self.url)

            if 'https://' in orig:
                new = orig.replace('https://',"",1)
            elif 'http://' in orig:
                new = orig.replace('http://',"",1)

            cmd = str('nmap -v -A -T5 {url} --stats-every 30m | txt2html -extract -8 >> {file}'.format(url=new, file=output))
            os.system(cmd)
            os.chdir('..')
            print('Nmap Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

    # Test TLS/SSL Encryption
    def testssl(self):
        global url
        url = self.url
        
        try:
            print("Launching TestSSL Scan\n")
            os.chdir('testssl.sh')
            cmd = str('./testssl.sh -s -p -h --vulnerabilities {url} | txt2html -extract -8 >> ../html/{file}'.format(url=self.url, file=output))
            os.system(cmd)
            os.chdir('..')
            print('TestSSL Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

    # URL Reputation Checker
    def checkURL(self):
        global url
        url = self.url
        
        try:
            print("Launching CheckURL Scan\n")
            os.chdir('checkURL')
            cmd = str('python checkURL.py --url {url} | txt2html -extract -8 >> ../html/{file}'.format(url=self.url, file=output))
            os.system(cmd)
            os.chdir('..')
            print('CheckURL Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))
        
    # Brute force directories and file names on web application servers
    def dirbuster(self):
        global url
        url = self.url
        
        try:
            print("DirBuster Scan Not Currently Functional!\n")
##            os.chdir('python-dirbuster')
##            cmd = str('python dirbust.py '+self.url+'/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt')
##            os.system(cmd)
##            os.chdir('..')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))


def header(tool):
    seperator = str("<p>" + ("-"*40) + "<br>" + "</p>")
    current_time = "<p><i>" + str(datetime.datetime.now()) + "</i></p>"
    os.chdir('html')
    #open the output file & append to it
    with open(output, "a") as f:
        f.write(seperator)
        if tool == "nmap":
            f.write(str("<h1 style='color: red;'>NMAP</h1>"))
            f.write(current_time)
        elif tool == "testssl":
            f.write(str("<h1 style='color: red;'>TESTSSL</h1>"))
            f.write(current_time)
        elif tool == "checkURL":
            f.write(str("<h1 style='color: red;'>CheckURL</h1>"))
            f.write(current_time)
        elif tool == "dirbuster":
            f.write(str("<h1 style='color: red;'>DirBuster</h1>"))
            f.write(current_time)
        elif tool == "nikto":
            f.write(str("<h1 style='color: red;'>Nikto</h1>"))
            f.write(current_time)
        elif tool == "WPscan":
            f.write(str("<h1 style='color: red;'>WPScan</h1>")) 
            f.write(current_time)
        elif tool == "dotdotpwn":
            f.write(str("<h1 style='color: red;'>DotDotPWN</h1>")) 
            f.write(current_time)
        elif tool == "wappalyzer":
            f.write(str("<h1 style='color: red;'>Wappalyzer</h1>"))
            f.write(current_time)
        elif tool == "cmseek":
            f.write(str("<h1 style='color: red;'>CMSeek</h1>"))
            f.write(current_time)
        elif tool == "MSWmap":
            f.write(str("<h1 style='color: red;'>MS Wmap</h1>"))    
            f.write(current_time)
        f.write(seperator)
        f.close()
    os.chdir('..')
  
def landing(prompt,url_temp,output_temp):
    global url
    global output

    output = output_temp
    validURL = True
    url = str(url_temp)

    if prompt == '1':
        print('\nCurrent Target: '+url)
        print(colored('\n***Preparing INFORMATION GATHERING Scans***','cyan',
                      attrs=['bold','blink']))
        print('1. Nmap - Network Mapper')
        print('2. Testssl.sh - Test TLS/SSL Encryption')
        print('3. CheckURL - URL Reputation Checker')
        print('4. DirBuster - Brute Force Directories '+
              colored('(NOT CURRENTLY SUPPORTED)','red'))
        print(colored('99.','red', attrs=['bold']) + ' Go Back')

        print(colored("\n-- syntax: 1245 --", "yellow"))
        options = input('Choose an option to proceed: ')
        
        if options == '99':
            initial(validURL,url,output)

        else:
            for resp in options:
                if resp == '1':
                    url = INFORMATION_GATHERING() # call the class
                    header("nmap")
                    url.nmap() #Start nmap scan

                elif resp == '2':
                    url = INFORMATION_GATHERING() # call the class
                    header("testssl")
                    url.testssl() #Start testssl.sh scan

                elif resp == '3':
                    url = INFORMATION_GATHERING() # call the class
                    header("checkURL")
                    url.checkURL() #Start CheckURL scan

                elif resp == '4':
                    url = INFORMATION_GATHERING() # call the class
                    header("disbuster")
                    url.dirbuster() #Start DirBuster scan
     
                else:
                    print('\n['+str(resp)+']'+colored(' Invalid tool option. Please try again!\n','red',
                        attrs=['bold']))

    elif prompt == '2':
        print('\nCurrent Target: '+url)
        print(colored('\n***Preparing VULNERABILITY Scans***\n','yellow',
                      attrs=['bold','blink']))
        print('1. Nikto - Open Source Vulnerability Scanner')
        print('2. WPScan - Wordpress WebApp Vulnerability Scanner')
        print('3. DotDotPwn - Directory Traversal Exploiter'+
              colored('(Warning: Likely Long Run Time)','red'))
        print(colored('99.','red', attrs=['bold']) + ' Go Back')

        print(colored("\n-- syntax: 1245 --", "yellow"))
        options = input('Choose an option to proceed: ')
        
        if options == '99':
            initial(validURL,url,output)

        else:
            for resp in options:
                if resp == '1':
                    url = VULNERABILITY() # call the class
                    header("nikto")
                    url.nikto() #Start Nikto Scan

                elif resp == '2':
                    url = VULNERABILITY() # call the class
                    header("WPscan")
                    url.WPScan() #Start WPScan Scan

                elif resp == '3':
                    url = VULNERABILITY() # call the class
                    header("dotdotpwn")
                    url.dotdotpwn() #Start DotDotPwn Scan
        
                else:
                    print('\n['+str(resp)+']'+colored(' Invalid tool option. Please try again!\n','red',
                        attrs=['bold']))

    elif prompt == '3':
        print('\nCurrent Target: '+url)
        print(colored('\n***Preparing TECHNOLOGY LOOKUP Scans***\n','green',
                      attrs=['bold','blink']))
        print('1. Wappalyzer - Underlying Technology Lookup')
        print('2. CMSeeK - Basic CMS Detection')
        print(colored('99.','red', attrs=['bold']) + ' Go Back')

        print(colored("\n-- syntax: 1245 --", "yellow"))
        options = input('Choose an option to proceed: ')
        
        if options == '99':
            initial(validURL,url,output)

        else:
            for resp in options:
                if resp == '1':
                    url = TECHNOLOGY_LOOKUP() # call the class
                    header("wappalyzer")
                    url.wappalyzer() #Start Wappalyzer Scan

                if resp == '2':
                    url = TECHNOLOGY_LOOKUP() # call the class
                    header("cmseek")
                    url.cmseek() #Start CMSeeK Scan
                    
                else:
                    print('\n['+str(resp)+']'+colored(' Invalid tool option. Please try again!\n','red',
                        attrs=['bold']))

    elif prompt == '4':
        print('\nCurrent Target: '+url)
        print(colored('\n***Preparing EXPLOIT Scans***\n','magenta',attrs=['bold','blink']))
        print('1. Metasploit: WMAP - Web App Vuln. Scanner Conducted Within Metasploit framework')
        print(colored('99.','red', attrs=['bold']) + ' Go Back')

        print(colored("\n-- syntax: 1245 --", "yellow"))
        options = input('Choose an option to proceed: ')
        
        if options == '99':
            initial(validURL,url,output)

        else:
            for resp in options:
                if resp == '1':
                    url = EXPLOITS() # call the class
                    header("MSWmap")
                    url.MSWmap() #Start WMAP scan
                    print('Metasploit: WMAP Successfully Executed')
                    
                else:
                    print('\n['+str(resp)+']'+colored(' Invalid tool option. Please try again!\n','red',
                        attrs=['bold']))

    elif prompt == '0':
        validURL = False
        validateURL(validURL,url,output) 

    elif prompt == '99':
        sys.exit(colored('\nTerminating KOMODO (╯°□°）╯︵ ┻━┻','red', attrs=['bold']))
               
    else:
        print(colored('\nInvalid input. Please try again!\n','red',
                      attrs=['bold']))

def initial(validURL,url_temp,output_temp):   
    while validURL == True:
        global url
        url = url_temp
        global output
        output = output_temp
        
        print(colored('\n1. Information Gathering','cyan',
                      attrs=['bold']))
        print(colored('2. Vulnerability','yellow',
                      attrs=['bold']))
        print(colored('3. Technology Lookup','green',
                      attrs=['bold']))
        print(colored('4. Exploits','magenta',
                      attrs=['bold']))
        print(colored('0. Change Target', 'red', attrs=['bold']))
        print(colored('99. Exit', 'red', attrs=['bold']))

        prompt = input('\nChoose a category to proceed: ')               
        landing(prompt,url,output)

def validateURL(validURL, url_temp, output_temp):
    global url
    url = url_temp
    global output
    output = output_temp
    
    #User input for URL Prefix and Target
    while validURL == False:
        prefix = input('Enter 1 for '+colored('HTTPS','yellow')+' or 2 for '+colored('HTTP','yellow')+': ')
        if prefix == '1':
            target = input('('+colored('HTTPS','yellow')+' Selected) Enter the target URL or IP Address: ')
            
            #regular expression to replace all link issues i.e. / & .
            rep = {"/": "-", ".com": "", ".": "-"} #define desired replacements here

            #these three lines do the replacing
            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            output = (pattern.sub(lambda m: rep[re.escape(m.group(0))], target)) + ".html"
             
            url = 'https://'+str(target)
            validURL = True
            #print ("URL SUCCESSFULLY VALIDATED") #for debugging
            print(colored('\nCurrent Target: '+url,
                    attrs=['bold']))

            initial(validURL,url,output)

        elif prefix == '2':
            target = input('('+colored('HTTP','yellow')+' Selected) Enter the target URL or IP Address: ')

            #regular expression to replace all link issues i.e. / & .
            rep = {"/": "-", ".com": "", ".": "-"} #define desired replacements here

            #these three lines do the replacing
            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            output = (pattern.sub(lambda m: rep[re.escape(m.group(0))], target)) + ".html"
            
            url = 'http://'+str(target)
            validURL = True
            #print ("URL SUCCESSFULLY VALIDATED") #for debugging
            print(colored('\nCurrent Target: '+url,
                    attrs=['bold']))

            initial(validURL,url,output)
            
        else:
            print(colored('\nInvalid Input.','red', attrs=['bold']))

#Main
def main():

    #Print KOMODO Title
    print((('*' * 50) + '\n') * 3)
    tprint('    KOMODO')
    print((('*' * 50) + '\n') * 3)

    global url
    global output
    
    url = ""
    output = ""
    validURL = False
    
    #Initial Screen
    validateURL(validURL,url,output) 

if __name__ == '__main__':
    main()
