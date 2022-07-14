# KOMODO All-in-one Hacking Tool
# Joshua Sloves / Ethan Tomford

####### SAMPLE TARGET https://google-gruyere.appspot.com/359771356088723951563265865954951743836/
####### SAMPLE TARGET scanme.nmap.org

import os, warnings, sys
from termcolor import colored
from art import *
from Wappalyzer import Wappalyzer, WebPage

try:
    class TBD:
        def __init__(self):
            self.url = url

    class TECHNOLOGY_LOOKUP:
        def __init__(self):
            self.url = url

        # Discover WebApp underlying technology
        def wappalyzer(self):
            print(str(self.url))
            print('Running Wappalyzer technology detector on {}'.format(self.url))
            webpage = WebPage.new_from_url(str(self.url))
            warnings.filterwarnings('ignore', message="""Caught 'unbalanced parenthesis at position 119' compiling regex""", category=UserWarning )

            wappalyzer = Wappalyzer.latest()
            print(wappalyzer.analyze_with_versions_and_categories(webpage))
            print('Wappalyzer Successfully Executed')

      
    class VULNERABILITY:
        def __init__(self):
            self.url = url

        # Open Source Vulnerability Scanner
        def nikto(self):
            print('Lauching Nikto Vulnerability Scanner on {}'.format(self.url))
            cmd = str('nikto -h {} -ssl -o nikto.html -Format htm'.format(self.url))
            os.system(cmd)
            print('Nikto Successfully Executed')

        # Wordpress WebApp Vulnerability Scanner
        def WPScan(self):
            print('Running WPScan Against {}'.format(self.url))
            cmd = str('wpscan --url '+self.url)
            os.system(cmd)
            print('WPScan Successfully Executed')

        # Directory Traversal Exploiter
        def dotdotpwn(self):
            orig = str(self.url)
            
            if 'https://' in orig:
                new = orig.replace('https://',"",1)
            elif 'http://' in orig:
                new = orig.replace('http://',"",1)
                
            print('Running DotDotPwn Against {}'.format(new))
            cmd = str('dotdotpwn -m http -h {}'.format(new))
            os.system(cmd)
            print('DotDotPwn Successfully Executed')

    class INFORMATION_GATHERING:
        def __init__(self):
            self.url = url

        # Network Mapper
        def nmap(self):
            print("Launching aggressive NMAP Scan\n")
            orig = str(self.url)

            if 'https://' in orig:
                new = orig.replace('https://',"",1)
            elif 'http://' in orig:
                new = orig.replace('http://',"",1)

            cmd = str('nmap -p0- -v -A -sV -T4 {}'.format(new))
            os.system(cmd)
            print('Nmap Successfully Executed')

        # URL Reputation Checker
        def checkURL(self):
            os.chdir('checkURL')
            cmd = str('python checkURL.py --url {}'.format(self.url))
            os.system(cmd)
            print('CheckURL Successfully Executed')
            
        # Brute force directories and file names on web application servers
        def dirbuster(self):
            os.chdir('python-dirbuster')
            cmd = str('python dirbust.py '+self.url+'/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt')
            os.system(cmd)
            print('DirBuster Successfully Executed')
        
    def landing(prompt,url_temp):
        global url
        validURL = True
        url = str(url_temp)

        if prompt == '1':
            print('\nCurrent Target: '+url)
            print(colored('\n***Preparing INFORMATION GATHERING Scans***','cyan',
                          attrs=['bold','blink']))
            print('1. Nmap - Network Mapper')
            print('2. CheckURL - URL Reputation Checker')
            print('3. DirBuster - Brute Force Directories '+
                  colored('(Warning: Likely Long Run Time)','red'))
            print('99. Go Back')
            
            resp = input('\nChoose an option to proceed: \n')

            if resp == '1':
                url = INFORMATION_GATHERING() # call the class
                url.nmap() #Start nmap scan

            elif resp == '2':
                url = INFORMATION_GATHERING() # call the class
                url.checkURL() #Start CheckURL scan

            elif resp == '3':
                url = INFORMATION_GATHERING() # call the class
                url.dirbuster() #Start DirBuster scan
                
            elif resp == '99':
                initial(validURL,url)

        elif prompt == '2':
            print('\nCurrent Target: '+url)
            print(colored('\n***Preparing VULNERABILITY Scans***\n','yellow',
                          attrs=['bold','blink']))
            print('1. Nikto - Open Source Vulnerability Scanner')
            print('2. WPScan - Wordpress WebApp Vulnerability Scanner')
            print('3. DotDotPwn - Directory Traversal Exploiter')

            print('99. Go Back')

            resp = input('\nChoose an option to proceed: \n')

            if resp == '1':
                url = VULNERABILITY() # call the class
                url.nikto() #Start Nikto Scan
            
            if resp == '2':
                url = VULNERABILITY() # call the class
                url.WPScan() #Start WPScan Scan

            if resp == '3':
                url = VULNERABILITY() # call the class
                url.dotdotpwn() #Start DotDotPwn Scan
                
            elif resp == '99':
                initial(validURL,url)

        elif prompt == '3':
            print('\nCurrent Target: '+url)
            print(colored('\n***Preparing TECHNOLOGY LOOKUP Scans***\n','green',
                          attrs=['bold','blink']))
            print('1. Wappalyzer - Underlying Technology Lookup')
            print('2. TBD')
            print('99. Go Back')

            resp = input('\nChoose an option to proceed: \n')

            if resp == '1':
                url = TECHNOLOGY_LOOKUP() # call the class
                url.wappalyzer()
                
            if resp == '2':
                url = TECHNOLOGY_LOOKUP() # call the class
                url.builtwith()

            elif resp == '99':
                initial(validURL,url)
                
############################## WORK IN PROGRESS ############################
##        elif prompt == '4':
##            print('\nCurrent Target: '+url)
##            print(colored('\n***Preparing TBD Scans***\n','magenta',
##                          attrs=['bold','blink']))
##            print('1. TBD')
##            print('2. TBD')
##            print('99. Go Back')
##
##            resp = input('\nChoose an option to proceed: \n')
##
##            if resp == '1':
##                url = TECHNOLOGY_LOOKUP() # call the class
##                url.wappalyzer()
##                
##            if resp == '2':
##                url = TECHNOLOGY_LOOKUP() # call the class
##                url.builtwith()
############################## WORK IN PROGRESS ############################

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
            print(colored('4. TBD','magenta',
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
                print('\nCurrent Target: '+url)

                initial(validURL,url)

            elif prefix == '2':
                target = input('('+colored('HTTP','yellow')+' Selected) Enter the target URL or IP Address: ')
                url = 'http://'+str(target)
                validURL = True
                print ("URL SUCCESSFULLY VALIDATED") #for debugging
                print('\nCurrent Target: '+url)

                initial(validURL,url)
                
            else:
                print(colored('\nInvalid Input.','red', attrs=['bold']))
                
except:
    print(colored('Whoops! Something went wrong. Please try again.', 'red',))
    
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