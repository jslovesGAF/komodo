# KOMODO All-in-one Hacking Tool
# Joshua Sloves / Ethan Tomford

####### SAMPLE TARGET https://google-gruyere.appspot.com/593948396113602183495718301495133174940/
####### SAMPLE TARGET scanme.nmap.org
#######

import os, warnings, sys, re, datetime, socket, subprocess, urllib.request, json, requests, time
from termcolor import colored, cprint
from art import *
from Wappalyzer import Wappalyzer, WebPage
key = ""

def refreshPage(key,webpage):
    webpageTemp = webpage
    url = requests.get(webpageTemp)
    text = url.text
    data = json.loads(text)
    scan_metricsDict = data['scan_metrics']
    return scan_metricsDict

def loadData(key,webpage):
    webpageTemp = webpage
    url = requests.get(webpageTemp)
    text = url.text
    data = json.loads(text)
    return data

def api():
    global key
    print('Current API Key: '+key)
    key = input("Please enter your Burpsuite API Key: ")
    validAPI = True
    os.system('clear')
    storeKey()
    
    burpSelections()
    
def storeKey():
    global key
    if key == "":
        return key
    else:
        keyTemp = key
        return keyTemp

def refreshBurpScan(key):
    for i in range(50):
        webpage = 'http://127.0.0.1:1337/'+key+'/v0.1/scan/'+str(i)
        data = loadData(api,webpage)
        
        if "error" in data:
            #print('error found!')
            if data['error']=="Task ID not found":
                #print('task ID not found error')
                continue
            elif data['error']=="Unauthorized":
                #print('unauth error')
                continue

        elif "scan_status" in data:
            if data['scan_status'] == "succeeded":
                print('Task_ID '+data['task_id']+' scan successful.\n')
                continue
            elif data['scan_status'] == "failed":
                print('Task_ID '+data['task_id']+' scan failed. Check Burp.\n')
                continue
            
            print('Task_ID '+data['task_id']+' status:')
            progress = 0

            while progress < 100:
                scan_metricsDict = refreshPage(api,webpage)
                progress = scan_metricsDict['crawl_and_audit_progress']
                os.system('clear')
                print('Scanning... '+str(scan_metricsDict['crawl_and_audit_progress'])+'%')
                print('Scan progress: '+str(scan_metricsDict['crawl_and_audit_progress'])+'% complete.\n')
                time.sleep(5)
                if progress == 100:
                    print('Task_ID '+data['task_id']+' scan successful.\n')

def startBurpScan(key,url,scopeURLTemp,configTypeTemp):
    global scopeURL
    global configType
    #targetURL = 'https://google-gruyere.appspot.com/593948396113602183495718301495133174940'
    targetURL = url

    scopeURL = scopeURLTemp
    configType = configTypeTemp
    
    burpURL = str('\'http://127.0.0.1:1337/'+key+'/v0.1/scan\'')
    cmdURL = str('curl -vgw "\\n" -X POST {url} -d '.format(url=burpURL))
    cmdScope = str(',"scope":{"include":[{"rule":"'+'{url}'.format(url=targetURL)+'"}],'+'"type":"SimpleScope"},"urls":["'+'{url}'.format(url=targetURL)+'"]}\'')
    
    cmdConfig = str('\''+'{"scan_configurations":[{"name":"Crawl and Audit - Fast","type":"NamedConfiguration"''}]')
    cmd = str(cmdURL+cmdConfig+cmdScope)
    announcement = 'echo '+'\''+configType+' scan on '+targetURL+' with a scope of '+scopeURL+'\' | lolcat'
    os.system(announcement)
    confirm = input('Would you like to proceed? y/n \n')
    if confirm == 'y':
        os.system(cmd)
    elif confirm == 'n':
        os.system('clear')
        burpSelections()
    else:
        print('\n['+str(selected)+']'+colored(' Invalid selection. Please try again!\n','red',attrs=['bold']))
        

def burpSelections():
    global key
    global scopeURL
    global configType
    scopeURL = url
    configType = "None"
    if key == "":
        burpLanding()
    else:
        validURL = True
        validAPI = True
        while validAPI == True:
            #print(colored('Burp Key is: ','white', attrs=['bold'])+storeKey())
            print(colored('Target URL is: ','white', attrs=['bold'])+url)
            print(colored('Scan Scope is: ','white', attrs=['bold'])+scopeURL)
            print(colored('Scan Configuration is: ','white', attrs=['bold'])+configType)


            print(colored('\n*** Preparing BURPSUITE ***','yellow',
                          attrs=['bold','blink']))
            print('1. Launch Scan')
            print('2. Change Scope (Default is Target URL)')
            print('3. Change Scan Configuration')
            print('4. View Report')
            print('5. Update API Key ')
            print(colored('99.','red', attrs=['bold']) + ' Go Back')

            selected = input('\nChoose an option to proceed: ')
            if selected == '1':
                os.system('clear')
                print(colored('*** Launching Burp Scan (NOTE: 30s scan progress refresh interval) ***','yellow',
                              attrs=['bold']))
                startBurpScan(key,url,scopeURL,configType)
                refreshBurpScan(key)
                
            elif selected == '2':
                os.system('clear')
                print(colored('*** Enter new Target Scope URL or "',attrs=['bold'])+(colored('99','red', attrs=['bold'])+colored('" to go back: ***','white',attrs=['bold'])))
                scopeURL = input()
                if scopeURL == '99':
                    os.system('clear')
                    burpSelections()
                os.system('clear')

            elif selected == '3':
                os.system('clear')
                print(colored('*** Change Scan Configuration ***','white',
                              attrs=['bold']))
                print('1. Crawl and Audit - Fast')
                print('2. Crawl and Audit - Balanced')
                print('3. Crawl and Audit - Deep')
                print('4. Crawl and Audit - Lightweight')
                os.system("echo 'More configurations coming soon! :-)\n' | lolcat")
                print(colored('99.','red', attrs=['bold']) + ' Go Back')

                selected = input('\nChoose an option to proceed: ')
                
                if selected == '1':
                    os.system('clear')
                    configType = 'Crawl and Audit - Fast'
                elif selected == '2':
                    os.system('clear')
                    configType = 'Crawl and Audit - Balanced'
                elif selected == '3':
                    os.system('clear')
                    configType = 'Crawl and Audit - Deep'
                elif selected == '4':
                    os.system('clear')
                    configType = 'Crawl and Audit - Lightweight'
                elif selected == '99':
                    os.system('clear')
                    burpSelections()
                else:
                    print('\n['+str(selected)+']'+colored(' Invalid selection. Please try again!\n','red',attrs=['bold']))

            elif selected == '4':
                os.system('clear')
                print('viewing report')
                
            elif selected == '5':
                os.system('clear')
                validAPI = False
                api()
                
            elif selected == '99':
                os.system('clear')
                initial(validURL,url,output)

            else:
                print('\n['+str(selected)+']'+colored(' Invalid selection. Please try again!\n','red',attrs=['bold']))
                burpSelections(storedKey())

def burpLanding():
    global key
    validURL = True
    if key == "":
        validAPI = False
        while validAPI == False:
            #print(colored('Burp Key is: ','white', attrs=['bold'])+storeKey(key))
            print(colored('Target URL is: ','white', attrs=['bold'])+url)

            print(colored('\n***Preparing BURPSUITE***','yellow',
                          attrs=['bold','blink']))
            print('1. Start Scan')
            print('2. Change Scope')
            print('3. Change Scan Type')
            print('4. View Report')
            print('5. Update API Key '+colored('*IMPORTANT: KEY IS CLEARED AFTER KOMODO TERMINATES. DO THIS FIRST.','red', attrs=['bold','underline']))
            print(colored('99.','red', attrs=['bold']) + ' Go Back')

            selected = input('\nChoose an option to proceed: ')
            if selected == '5':
                api()
            
            elif selected == '99':
                os.system('clear')
                initial(validURL,url,output)
                
            else:
                os.system('clear')
                print(colored('Error. Did you forget your API key?\n','red',
                              attrs=['bold']))
                continue
    else:
        burpSelections()
        
def wappalyzer():
    global output
    global url

    try:   
        os.chdir('html')
        with open(output, "a") as f:
            webpage = WebPage.new_from_url(url)
            warnings.filterwarnings('ignore', message="""Caught 'unbalanced parenthesis at position 119' compiling regex""", category=UserWarning )

            wappalyzer = Wappalyzer.latest()
            print(wappalyzer.analyze_with_versions_and_categories(webpage))

            f.write(str(wappalyzer.analyze_with_versions_and_categories(webpage)))
            print('Running Wappalyzer technology detector on {}'.format(url))
            f.close()
        os.chdir('..')
        print('Wappalyzer Successfully Executed')

    except:
        os.chdir('..')
        print(colored('Whoops! Something went wrong. Please try again.', 'red',))

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
            #regular expression to replace all link issues i.e. / & .
            rep = {"https://": "", "http://": ""} #define desired replacements here

            #these three lines do the replacing
            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            new = (pattern.sub(lambda m: rep[re.escape(m.group(0))], orig))
            ip = socket.gethostbyname(new)
            
            cmd = str('msfconsole -q -p wmap -x '+"'"+'wmap_sites -d 0;wmap_targets -c;wmap_sites -a '+ip+';wmap_targets -d 0;wmap_run -p /home/kali/komodo/fav_modules;exit'+"'"+"| tee /dev/stderr | txt2html -extract -8 >> html/{file}".format(file=output))
            os.system(cmd)
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))
                      
##class TECHNOLOGY_LOOKUP:
##    def __init__(self):
##        self.url = url
##        self.output = output

##    # Discover WebApp underlying technology
  
##    def cmseek(self):
##        global url
##        global output
##        url = self.url
##        output = self.output
##
##        try:
##            print('Lauching CMSeeK Detection on {}'.format(self.url))
##            os.chdir('CMSeeK')
##            cmd = str('python cmseek.py -u {url} | tee /dev/stderr | txt2html -extract -8 >> ../html/{file} '.format(url=self.url,file=self.output))
##            os.system(cmd)
##            os.chdir('..')
##            print('CMSeeK Successfully Executed')
##        except:
##            os.chdir('..')
##            print(colored('Whoops! Something went wrong. Please try again.', 'red',))
  
class VULNERABILITY:
    def __init__(self):
        self.url = url
        self.output = output

    # Open Source Vulnerability Scanner
    def nikto(self):
        global url
        global output
        url = self.url
        output = self.output

        try:
            print('Lauching Nikto Vulnerability Scanner on {}'.format(self.url))
            cmd = str('nikto -h {url} | tee /dev/stderr | txt2html -extract -8 >> html/{file} '.format(url=self.url,file=self.output))
            os.system(cmd)
            print('Nikto Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))
            
    # Wordpress WebApp Vulnerability Scanner
    def WPScan(self):
        global url
        global output
        url = self.url
        output = self.output
        
        try:
            print('Running WPScan Against {}'.format(self.url))
            cmd = str('wpscan --url {url} --no-update --no-banner | tee /dev/stderr | txt2html -extract -8 >> html/{file}'.format(url=self.url,file=self.output))
            os.system(cmd)
            print('WPScan Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

    # Directory Traversal Exploiter
    def dotdotpwn(self):
        global url
        global output
        url = self.url
        output = self.output
        
        orig = str(self.url)
        
        try:
            if 'https://' in orig:
                new = orig.replace('https://',"",1)
            elif 'http://' in orig:
                new = orig.replace('http://',"",1)
                
            print('Running DotDotPwn Against {}'.format(new))
            cmd = str('dotdotpwn -m http -h {url} | tee /dev/stderr | txt2html -extract -8 >> html/{file}'.format(url=new, file=output))
            os.system(cmd)
            print('DotDotPwn Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

    def sqlmap(self):
        global url
        global output
        url = self.url
        output = self.output
        
        try:
            print('Running SQLmap Against {}'.format(self.url))
            cmd = str('sqlmap {url} --disable-coloring | tee /dev/stderr | txt2html -extract -8 >> html/{file}'.format(url=self.url,file=self.output))
            os.system(cmd)
            print('SQLmap Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

    def nuclei(self):
        global url
        global output
        url = self.url
        output = self.output
        
        try:
            print('Running Nuclei Against {}'.format(self.url))
            cmd = str('nuclei -u {url} | tee /dev/stderr | txt2html -extract -8 >> html/{file}'.format(url=self.url,file=self.output))
            os.system(cmd)
            print('Nuclei Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

class INFORMATION_GATHERING:
    def __init__(self):
        self.url = url
        self.output = output

    # Network Mapper
    def nmap(self):
        global url
        global output
        url = self.url
        output = self.output

        try:
            print("Launching aggressive NMAP Scan\n")
            orig = str(self.url)

            if 'https://' in orig:
                new = orig.replace('https://',"",1)
            elif 'http://' in orig:
                new = orig.replace('http://',"",1)

            cmd = str('nmap -v -A -T5 {url} --stats-every 30m| tee /dev/stderr | txt2html -extract -8 >> html/{file}'.format(url=new, file=output))
            os.system(cmd)
            print('Nmap Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))


    # Network Mapper
    def traceroute(self):
        global url
        global output
        url = self.url
        output = self.output

        try:
            print("Launching aggressive Traceroute Scan\n")
            orig = str(self.url)

            if 'https://' in orig:
                new = orig.replace('https://',"",1)
            elif 'http://' in orig:
                new = orig.replace('http://',"",1)

            cmd = str('traceroute {url}| tee /dev/stderr | txt2html -extract -8 >> html/{file}'.format(url=new, file=output))
            os.system(cmd)
            print('Traceroute Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

    # Test TLS/SSL Encryption
    def testssl(self):
        global url
        global output
        url = self.url
        output = self.output
        
        try:
            print("Launching TestSSL Scan\n")
            os.chdir('testssl.sh')
            cmd = str('./testssl.sh -s -p -h --vulnerabilities {url} | tee /dev/stderr | txt2html -extract -8 >> ../html/{file}'.format(url=self.url, file=output))
            os.system(cmd)
            os.chdir('..')
            print('TestSSL Successfully Executed')
        except:
            os.chdir('..')
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

    # Whatweb Lookup
    def whatweb(self):
        global url
        global output
        url = self.url
        output = self.output
        
        try:
            print("Launching WhatWeb Scan\n")
            cmd = str('whatweb {url} --color=never| tee /dev/stderr | txt2html -extract -8 >> html/{file}'.format(url=self.url, file=output))
            os.system(cmd)
            print('WhatWeb Successfully Executed')
        except:

            print(colored('Whoops! Something went wrong. Please try again.', 'red',))
            
    # WHOIS Lookup
    def whois(self):
        global url
        global output
        url = self.url
        orig = str(self.url)
        output = self.output

        try:
            print("Launching WHOIS Scan\n")
            #regular expression to replace all link issues i.e. / & .
            rep = {"https://": "", "http://": ""} #define desired replacements here

            #these three lines do the replacing
            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            new = (pattern.sub(lambda m: rep[re.escape(m.group(0))], orig))
            ip = socket.gethostbyname(new)
            
            cmd = str('whois '+ip+'| tee /dev/stderr | txt2html -extract -8 >> html/{file}'.format(file=output))
            os.system(cmd)
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))
            
    # URL Reputation Checker
    def checkURL(self):
        global url
        global output
        url = self.url
        output = self.output
        
        try:
            print("Launching CheckURL Scan\n")
            os.chdir('checkURL')
            cmd = str('python checkURL.py --url {url}| tee /dev/stderr | txt2html -extract -8 >> ../html/{file}'.format(url=self.url, file=output))
            os.system(cmd)
            os.chdir('..')
            print('CheckURL Successfully Executed')
        except:
            os.chdir('..')
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))
        
    # Brute force directories and file names on web application servers
    def gobuster(self):
        global url
        global output
        url = self.url
        output = self.output
        
        try:
            print("Launching GoBuster Scan\n")
            cmd = str('gobuster dir -u {url} -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -q| tee /dev/stderr | txt2html -extract -8 >> html/{file}'.format(url=self.url, file=output))
            os.system(cmd)
            print('WhatWeb Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

class QUALYS: 
    def qualysLanding(self):
        
        print(colored('\n1. "Run Monday"','white',
                      attrs=['bold']))
        print(colored('2. "Run Friday"','white',
                      attrs=['bold']))
        print(colored('3. Create New Sets','green',
                      attrs=['bold']))

        print(colored('99.','red', attrs=['bold']) + ' Go Back')

        selection = input('Choose an option to proceed: ')

        #Run Monday Script
        if selection == "1":
            os.chdir('/home/kali/Desktop/Qualys Scripts/For_Elizabeth/')
            os.system('sh run_monday')
            
        #Run Friday Script
        elif selection == "2":
            os.chdir('/home/kali/Desktop/Qualys Scripts/For_Elizabeth/')
            os.system('sh run_friday')

        #Create New Sets & Delete Old
        elif selection == "3":
            if len(os.listdir('/home/kali/Desktop/Qualys Scripts/For_Elizabeth/BMI_XMLs/')) == 0:
                print("Directory is empty")
            else:    
                os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/*')

            os.chdir('/home/kali/Desktop/Qualys Scripts/Test/')

            os.system('sh create_set1')
            os.system('sh create_set2')

            os.system('cp -a /home/kali/Desktop/Qualys\ Scripts/Test/. /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/')
            os.chdir('/home/kali/Desktop/Qualys Scripts/For_Elizabeth/BMI_XMLs/')
            os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/create_set1')
            os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/create_set2')
            os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/file1.txt')
            os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/file2.txt')
            os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/README.txt')
            os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/update_test.xml')

            os.chdir('/home/kali/Desktop/Qualys Scripts/Test/')
            for file in os.listdir('/home/kali/Desktop/Qualys Scripts/Test/'):
                if file.startswith("update1_") or file.startswith("update2_"):
                    command = 'rm '+str(file)
                    os.system(command)

        elif selection == '99':
            os.system('clear')
            return
            
        else:
            print('\n['+str(response)+']'+colored(' Invalid tool option. Please try again!\n','red',
                attrs=['bold']))
            x = QUALYS
            x.qualysLanding(self)

def header(tool):
    seperator = str("<p>" + ("-"*40) + "<br>" + "</p>")
    current_time = "<p>Ran on: <i>"+ str(datetime.datetime.now()) + "</i></p>"
    os.chdir('html')
    #open the output file & append to it
    with open(output, "a") as f:
        f.write(seperator)
        if tool == "nmap":
            f.write(str("<h1 style='color: red;'>NMAP</h1>"))
            f.write(current_time)
        elif tool == "traceroute":
            f.write(str("<h1 style='color: red;'>Traceroute</h1>"))
            f.write(current_time)
        elif tool == "testssl":
            f.write(str("<h1 style='color: red;'>TESTSSL</h1>"))
            f.write(current_time)
        elif tool == "whatweb":
            f.write(str("<h1 style='color: red;'>WhatWeb</h1>"))
            f.write(current_time)
        elif tool == "whois":
            f.write(str("<h1 style='color: red;'>WHOIS</h1>"))
            f.write(current_time)
        elif tool == "checkURL":
            f.write(str("<h1 style='color: red;'>CheckURL</h1>"))
            f.write(current_time)
        elif tool == "gobuster":
            f.write(str("<h1 style='color: red;'>GoBuster</h1>"))
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
        elif tool == "sqlmap":
            f.write(str("<h1 style='color: red;'>SQLmap</h1>"))
            f.write(current_time)
        elif tool == "nuclei":
            f.write(str("<h1 style='color: red;'>Nuclei</h1>"))
            f.write(current_time)
        elif tool == "wappalyzer":
            f.write(str("<h1 style='color: red;'>Wappalyzer</h1>"))
            f.write(current_time)
##        elif tool == "cmseek":
##            f.write(str("<h1 style='color: red;'>CMSeek</h1>"))
##            f.write(current_time)
        elif tool == "MSWmap":
            f.write(str("<h1 style='color: red;'>MS Wmap</h1>"))    
            f.write(current_time)
        f.write(seperator)
        f.close()
    os.chdir('..')
  
def landing(prompt,url_temp,output_temp):
    global url
    global output
    global key
    
    output = output_temp
    validURL = True
    url = str(url_temp)
    
    if prompt.lower() == 'b':
        burpLanding()
        
    if prompt.lower() == 'w':
        header("wappalyzer")
        wappalyzer()

    elif prompt == '1':
        print(colored('\nCurrent Target: '+url,
                      attrs=['bold']))
        print(colored('\n***Preparing INFORMATION GATHERING Scans***','cyan',
                      attrs=['bold','blink']))
        print('1. Nmap - Network Mapper')
        print('2. Traceroute - Packet Routing')
        print('3. Testssl.sh - Test TLS/SSL Encryption')
        print('4. WhatWeb - Modern Web Scanner')
        print('5. WHOIS - IP Lookup')        
        print('6. CheckURL - URL Reputation Checker')
        print('7. GoBuster - Brute Force Directories ')
        print(colored('99.','red', attrs=['bold']) + ' Go Back')

        print(colored("-- syntax: 1245 --\n", "yellow"))
        options = input('Choose an option to proceed: ')
        
        if options == '99':
            os.system('clear')
            initial(validURL,url,output)

        else:
            for selection in options:
                if selection == '1':
                    obj = INFORMATION_GATHERING() # call the class
                    header("nmap")
                    obj.nmap() #Start nmap scan
                    
                elif selection == '2':
                    obj = INFORMATION_GATHERING() # call the class
                    header("traceroute")
                    obj.traceroute() #Start testssl.sh scan
                    
                elif selection == '3':
                    obj = INFORMATION_GATHERING() # call the class
                    header("testssl")
                    obj.testssl() #Start testssl.sh scan
                    
                elif selection == '4':
                    obj = INFORMATION_GATHERING() # call the class
                    header("whatweb")
                    obj.whatweb() #Start WhatWeb scan
                    
                elif selection == '5':
                    obj = INFORMATION_GATHERING() # call the class
                    header("whois")
                    obj.whois() #Start WHOIS scan
                    
                elif selection == '7':
                    obj = INFORMATION_GATHERING() # call the class
                    header("gobuster")
                    obj.gobuster() #Start GoBuster scan
     
                else:
                    print('\n['+str(resp)+']'+colored(' Invalid tool option. Please try again!\n','red',
                        attrs=['bold']))

    elif prompt == '2':
        print(colored('\nCurrent Target: '+url,
                      attrs=['bold']))
        print(colored('\n***Preparing VULNERABILITY Scans***','yellow',
                      attrs=['bold','blink']))
        print('1. Nikto - Open Source Vulnerability Scanner')
        print('2. WPScan - Wordpress WebApp Vulnerability Scanner')
        print('3. DotDotPwn - Directory Traversal Exploiter '+
              colored('(Warning: Likely Long Run Time)','red'))
        print('4. SQLmap - Detect & Exploit SQL injection flaws')
        print('5. Nuclei - Template Based Vulnerability Scanner')
        print(colored('99.','red', attrs=['bold']) + ' Go Back')

        print(colored("\n-- syntax: 1245 --", "yellow"))
        options = input('Choose an option to proceed: ').lower()
        
        if options == '99':
            os.system('clear')
            initial(validURL,url,output)

        else:
            for selection in options:
                if selection == '1':
                    obj = VULNERABILITY() # call the class
                    header("nikto")
                    obj.nikto() #Start Nikto Scan

                elif selection == '2':
                    obj = VULNERABILITY() # call the class
                    header("WPscan")
                    obj.WPScan() #Start WPScan Scan

                elif selection == '3':
                    obj = VULNERABILITY() # call the class
                    header("dotdotpwn")
                    obj.dotdotpwn() #Start DotDotPwn Scan
                    
                elif selection == '4':
                    obj = VULNERABILITY() # call the class
                    header("sqlmap")
                    obj.sqlmap() #Start SQLmap Scan
                    
                elif selection == '5':
                    obj = VULNERABILITY() # call the class
                    header("nuclei")
                    obj.nuclei() #Start Nuclei Scan

                else:
                    print('\n['+str(resp)+']'+colored(' Invalid tool option. Please try again!\n','red',
                        attrs=['bold']))

##    elif prompt == '3':
##        print(colored('\nCurrent Target: '+url,
##                      attrs=['bold']))
##        print(colored('\n***Preparing TECHNOLOGY LOOKUP Scans***','green',
##                      attrs=['bold','blink']))
##        print('1. Wappalyzer - Underlying Technology Lookup')
##        print('2. CMSeeK - Basic CMS Detection')
##        print(colored('99.','red', attrs=['bold']) + ' Go Back')
##
##        print(colored("\n-- syntax: 1245 --", "yellow"))
##        options = input('Choose an option to proceed: ')
##        
##        if options == '99':
##            os.system('clear')
##            initial(validURL,url,output)
##
##        else:
##            for selection in options:
##                if selection == '1':
##                    obj = TECHNOLOGY_LOOKUP() # call the class
##                    header("wappalyzer")
##                    obj.wappalyzer() #Start Wappalyzer Scan
##
##                elif resp == '2':
##                    url = TECHNOLOGY_LOOKUP() # call the class
##                    header("cmseek")
##                    url.cmseek() #Start CMSeeK Scan
##                    
##                else:
##                    print('\n['+str(resp)+']'+colored(' Invalid tool option. Please try again!\n','red',
##                        attrs=['bold']))

    elif prompt == '3':
        print(colored('\nCurrent Target: '+url,
                      attrs=['bold']))
        print(colored('\n***Preparing EXPLOIT Scans***','magenta'
                      ,attrs=['bold','blink']))
        print('1. Metasploit: WMAP - Web App Vuln. Scanner Conducted Within Metasploit framework')
        print(colored('99.','red', attrs=['bold']) + ' Go Back')

        print(colored("\n-- syntax: 1245 --", "yellow"))
        options = input('Choose an option to proceed: ')
        
        if options == '99':
            os.system('clear')
            initial(validURL,url,output)

        else:
            for selection in options:
                if selection == '1':
                    obj = EXPLOITS() # call the class
                    header("MSWmap")
                    obj.MSWmap() #Start WMAP scan
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
        
        # API tool selection
        text = colored('\n- - - - - APIs - - - - -','red', attrs=['bold'])
        cprint(text, "yellow", "on_white")
        print(colored('b. BurpSuite','white'))
        print(colored('w. Wappalyzer','white'))


        # other tool selection
        text = colored('\n- - - - - RECON | LIGHTWEIGHT VULN. SCANS | EXPLOITS - - - - -','red', attrs=['bold'])
        cprint(text, "yellow", "on_white")
        print(colored('1. Information Gathering','white'))
        print(colored('2. Vulnerability','white'))
        #print(colored('3. Technology Lookup','white'))
        print(colored('3. Exploits','white'))
        print(colored('\n0. Change Target', 'red', attrs=['bold']))
        print(colored('99. Exit', 'red', attrs=['bold']))

        prompt = input('\nChoose a category to proceed: ')
        os.system('clear')
        landing(prompt,url,output)

def validateURL(validURL, url_temp, output_temp):
    global url
    url = url_temp
    global output
    output = output_temp

    #User input for URL Prefix and Target
    while validURL == False:
        prefix = input('Enter "1" for '+colored('HTTPS','yellow')+' or "2" for '+colored('HTTP','yellow')+': ')
        if prefix == '1':
            target = input('('+colored('HTTPS','yellow')+' Selected) Enter the target URL or IP Address: ')
            
            #regular expression to replace all link issues i.e. / & . for html files
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

            #regular expression to replace all link issues i.e. / & . for html files
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

def validateIntent(validURL,url,output):
    validIntent = False

    while validIntent == False:
        response = input('\nEnter "1" for '+colored('Qualys Script Management','yellow')+' or "2" for '+colored('Penetrating Testing','red')+': ')
        if response == '1':
            os.system('clear')
            validIntent = True
            x = QUALYS()
            x.qualysLanding()
            validateIntent(validURL,url,output)
        elif response == '2':
            os.system('clear')
            validateURL(validURL,url,output) 
        else:
            print('\n['+str(response)+']'+colored(' Invalid tool option. Please try again!\n','red',
                attrs=['bold']))
#Main
def main():
    os.system('clear')
    #Print KOMODO Title
    print((('*' * 50) + '\n') * 3)
    tprint('    KOMODO')
    print((('*' * 50) + '\n') * 3)

    global url
    global output
    
    os.system("echo 'NEW FEATURES ALERT!\nIntroducing... \n- Full BurpSuite REST API support!\n- Reworked Tool Selection!\n- Friendlier (and fancier) UI!' | lolcat")

    url = ""
    output = ""
    validURL = False
    
    #Initial Screen
    validateIntent(validURL,url,output)

if __name__ == '__main__':
    main()
