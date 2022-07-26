# KOMODO All-in-one Hacking Tool
# Joshua Sloves / Ethan Tomford

####### SAMPLE TARGET https://google-gruyere.appspot.com/359771356088723951563265865954951743836/
####### SAMPLE TARGET scanme.nmap.org
#######

import os, warnings, sys
from termcolor import colored
from art import *
from Wappalyzer import Wappalyzer, WebPage
import socket

try:
    class EXPLOITS:
        def __init__(self):
            self.url = url

        def MSWmap(self):
            global url
            url = self.url
            orig = str(self.url)
            print('Lauching WMAP Scanner through Metasploit on {}'.format(self.url))
            
            if 'https://' in orig:
                new = orig.replace('https://',"",1)
                ip = socket.gethostbyname(new)
                cmd = str('msfconsole -q -p wmap -x '+"'"+'wmap_sites -d 0;wmap_targets -c;wmap_sites -a '+ip+';wmap_targets -d 0;wmap_run -p /home/kali/.msf4/fav_modules;exit'+"'")
                print(cmd)
                os.system(cmd)

            elif 'http://' in orig:
                new = orig.replace('http://',"",1)
                ip = socket.gethostbyname(new)
                cmd = str('msfconsole -q -p wmap -x '+"'"+'wmap_sites -d 0;wmap_targets -c;wmap_sites -a '+ip+';wmap_targets -d 0;wmap_run -p /home/kali/.msf4/fav_modules;exit'+"'")
                print(cmd)
                os.system(cmd)

            else:
                ip = socket.gethostbyname(new)
                cmd = str('msfconsole -q -p wmap -x '+'wmap_sites -a '+ip+';wmap_targets -d 0;wmap_run -p /home/kali/.msf4/fav_modules')
                os.system(cmd)
                          
    class TECHNOLOGY_LOOKUP:
        def __init__(self):
            self.url = url

        # Discover WebApp underlying technology
        def wappalyzer(self):
            print('Running Wappalyzer technology detector on {}'.format(self.url))
            webpage = WebPage.new_from_url(str(self.url))
            warnings.filterwarnings('ignore', message="""Caught 'unbalanced parenthesis at position 119' compiling regex""", category=UserWarning )

            wappalyzer = Wappalyzer.latest()
            print(wappalyzer.analyze_with_versions_and_categories(webpage))
            
        def cmseek(self):
            global url
            url = self.url
            print('Lauching CMSeeK Detection on {}'.format(self.url))
            os.chdir('CMSeeK')
            cmd = str('python cmseek.py -u {}'.format(self.url))
            os.system(cmd)
            os.chdir('..')    
      
    class VULNERABILITY:
        def __init__(self):
            self.url = url

        # Open Source Vulnerability Scanner
        def nikto(self):
            global url
            url = self.url
            print('Lauching Nikto Vulnerability Scanner on {}'.format(self.url))
            cmd = str('nikto -h {} -ssl -o nikto.html -Format htm'.format(self.url))
            os.system(cmd)

        # Wordpress WebApp Vulnerability Scanner
        def WPScan(self):
            global url
            url = self.url
            print('Running WPScan Against {}'.format(self.url))
            cmd = str('wpscan --url '+self.url+' --no-update --no-banner')
            os.system(cmd)

        # Directory Traversal Exploiter
        def dotdotpwn(self):
            global url
            url = self.url
            orig = str(self.url)
            
            if 'https://' in orig:
                new = orig.replace('https://',"",1)
            elif 'http://' in orig:
                new = orig.replace('http://',"",1)
                
            print('Running DotDotPwn Against {}'.format(new))
            cmd = str('dotdotpwn -m http -h {}'.format(new))
            os.system(cmd)

    class INFORMATION_GATHERING:
        def __init__(self):
            self.url = url

        # Network Mapper
        def nmap(self):
            global url
            url = self.url
    
            print("Launching aggressive NMAP Scan\n")
            orig = str(self.url)

            if 'https://' in orig:
                new = orig.replace('https://',"",1)
            elif 'http://' in orig:
                new = orig.replace('http://',"",1)

            cmd = str('nmap -p0- -v -A -sV -T4 {}'.format(new))
            os.system(cmd)

        # Test TLS/SSL Encryption
        def testssl(self):
            global url
            url = self.url
            
            os.chdir('testssl.sh')
            cmd = str('./testssl.sh -s -p -h --vulnerabilities {}'.format(self.url))
            os.system(cmd)
            os.chdir('..')

        # URL Reputation Checker
        def checkURL(self):
            global url
            url = self.url
            
            os.chdir('checkURL')
            cmd = str('python checkURL.py --url {}'.format(self.url))
            os.system(cmd)
            os.chdir('..')
            
        # Brute force directories and file names on web application servers
        def dirbuster(self):
            global url
            url = self.url
            
            os.chdir('python-dirbuster')
            cmd = str('python dirbust.py '+self.url+'/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt')
            os.system(cmd)
      
    def landing(prompt,url_temp):
        global url
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
                  colored('(Warning: Likely Long Run Time)','red'))
            print('99. Go Back')

            print(colored("\n-- syntax: 1245 --", "yellow"))
            options = input('Choose an option to proceed: \n')
            
            if options == '99':
                initial(validURL,url)

            else:
                for resp in options:
                    if resp == '1':
                        url = INFORMATION_GATHERING() # call the class
                        url.nmap() #Start nmap scan
                        print('Nmap Successfully Executed')

                    elif resp == '2':
                        url = INFORMATION_GATHERING() # call the class
                        url.testssl() #Start testssl.sh scan
                        print('Testssl.sh Successfully Executed')

                    elif resp == '3':
                        url = INFORMATION_GATHERING() # call the class
                        url.checkURL() #Start CheckURL scan
                        print('CheckURL Successfully Executed')

                    elif resp == '4':
                        url = INFORMATION_GATHERING() # call the class
                        url.dirbuster() #Start DirBuster scan
                        print('DirBuster Successfully Executed')
         
                    else:
                        print('\n['+str(resp)+']'+colored(' Invalid tool option. Please try again!\n','red',
                            attrs=['bold']))

        elif prompt == '2':
            print('\nCurrent Target: '+url)
            print(colored('\n***Preparing VULNERABILITY Scans***\n','yellow',
                          attrs=['bold','blink']))
            print('1. Nikto - Open Source Vulnerability Scanner')
            print('2. WPScan - Wordpress WebApp Vulnerability Scanner')
            print('3. DotDotPwn - Directory Traversal Exploiter')
            print('99. Go Back')

            print(colored("\n-- syntax: 1245 --", "yellow"))
            options = input('Choose an option to proceed: \n')
            
            if options == '99':
                initial(validURL,url)

            else:
                for resp in options:
                    if resp == '1':
                        url = VULNERABILITY() # call the class
                        url.nikto() #Start Nikto Scan
                        print('Nikto Successfully Executed')

                    elif resp == '2':
                        url = VULNERABILITY() # call the class
                        url.WPScan() #Start WPScan Scan
                        print('WPScan Successfully Executed')

                    elif resp == '3':
                        url = VULNERABILITY() # call the class
                        url.dotdotpwn() #Start DotDotPwn Scan
                        print('DotDotPwn Successfully Executed')
            
                    else:
                        print('\n['+str(resp)+']'+colored(' Invalid tool option. Please try again!\n','red',
                            attrs=['bold']))

        elif prompt == '3':
            print('\nCurrent Target: '+url)
            print(colored('\n***Preparing TECHNOLOGY LOOKUP Scans***\n','green',
                          attrs=['bold','blink']))
            print('1. Wappalyzer - Underlying Technology Lookup')
            print('2. CMSeeK - Basic CMS Detection')
            print('99. Go Back')

            print(colored("\n-- syntax: 1245 --", "yellow"))
            options = input('Choose an option to proceed: \n')
            
            if options == '99':
                initial(validURL,url)

            else:
                for resp in options:
                    if resp == '1':
                        url = TECHNOLOGY_LOOKUP() # call the class
                        url.wappalyzer() #Start Nikto Scan
                        print('Wappalyzer Successfully Executed')

                    if resp == '2':
                        url = TECHNOLOGY_LOOKUP() # call the class
                        url.cmseek() #Start Nikto Scan
                        print('CMSeeK Successfully Executed')
                        
                    else:
                        print('\n['+str(resp)+']'+colored(' Invalid tool option. Please try again!\n','red',
                            attrs=['bold']))

        elif prompt == '4':
            print('\nCurrent Target: '+url)
            print(colored('\n***Preparing EXPLOIT Scans***\n','magenta,
                          attrs=['bold','blink']))
            print('1. Metasploit: WMAP - Web App Vuln. Scanner Conducted Within Metasploit framework')
            print('99. Go Back')

            print(colored("\n-- syntax: 1245 --", "yellow"))
            options = input('Choose an option to proceed: \n')
            
            if options == '99':
                initial(validURL,url)

            else:
                for resp in options:
                    if resp == '1':
                        url = EXPLOITS() # call the class
                        url.MSWmap() #Start Nikto Scan
                        print('Metasploit: WMAP Successfully Executed')
                        
                    else:
                        print('\n['+str(resp)+']'+colored(' Invalid tool option. Please try again!\n','red',
                            attrs=['bold']))

        elif prompt == '0':
            validURL = False
            validateURL(validURL,url) 

        elif prompt == '99':
            sys.exit(colored('\nTerminating KOMODO (╯°□°）╯︵ ┻━┻','red', attrs=['bold']))
                   
        else:
            print(colored('\nInvalid input. Please try again!\n','red',
                          attrs=['bold']))

    def initial(validURL,url_temp):   
        while validURL == True:
            global url
            url = url_temp
            
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
            landing(prompt,url)

    def validateURL(validURL, url_temp):
        global url
        url = url_temp
        
        #User input for URL Prefix and Target
        while validURL == False:
            prefix = input('Enter 1 for '+colored('HTTPS','yellow')+' or 2 for '+colored('HTTP','yellow')+': ')
            if prefix == '1':
                target = input('('+colored('HTTPS','yellow')+' Selected) Enter the target URL or IP Address: ')
                url = 'https://'+str(target)
                validURL = True
                print ("URL SUCCESSFULLY VALIDATED") #for debugging
                print(colored('\nCurrent Target: '+url,
                        attrs=['bold']))

                initial(validURL,url)

            elif prefix == '2':
                target = input('('+colored('HTTP','yellow')+' Selected) Enter the target URL or IP Address: ')
                url = 'http://'+str(target)
                validURL = True
                print ("URL SUCCESSFULLY VALIDATED") #for debugging
                print(colored('\nCurrent Target: '+url,
                        attrs=['bold']))

                initial(validURL,url)
                
            else:
                print(colored('\nInvalid Input.','red', attrs=['bold']))
                
except:
    print(colored('Whoops! Something went wrong. Please try again.', 'red',))

#Main
def main():

    #Print KOMODO Title
    print((('*' * 50) + '\n') * 3)
    tprint('    KOMODO')
    print((('*' * 50) + '\n') * 3)

    global url
    url = ""
    validURL = False
    
    #Initial Screen
    validateURL(validURL,url) 

if __name__ == '__main__':
    main()
