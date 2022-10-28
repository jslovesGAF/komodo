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
import subprocess

key = ""
configType = "None"
scopeURL = ""
home = os.getcwd()

####################################### BEGINNING OF API SECTION #######################################
class BURPSUITE():
    def refreshPage(self,key,webpage):
        webpageTemp = webpage
        url = requests.get(webpageTemp)
        text = url.text
        data = json.loads(text)
        scan_metricsDict = data['scan_metrics']
        return scan_metricsDict

    def loadData(self,key,webpage):
        webpageTemp = webpage
        url = requests.get(webpageTemp)
        text = url.text
        data = json.loads(text)
        return data

    def api(self):
        global key
        print('\nCurrent API Key: '+str(key))
        key = input("Please enter your Burpsuite API Key: ")
        validAPI = True
        os.system('clear')

        burp.storeKey()
        burp.burpSelections()

    def storeKey(self):
        global key
        if key == "":
            return key
        else:
            keyTemp = key
            return keyTemp

    def refreshBurpScan(self,key):
        for i in range(50):
            webpage = 'http://127.0.0.1:1337/'+key+'/v0.1/scan/'+str(i)
            data = burp.loadData(key,webpage)

            if "error" in data:
                if data['error']=="Task ID not found":
                    continue
                elif data['error']=="Unauthorized":
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
                try:
                    while progress < 100:
                        scan_metricsDict = burp.refreshPage(key,webpage)
                        progress = scan_metricsDict['crawl_and_audit_progress']
                        os.system('clear')
                        print('Task_ID '+data['task_id']+' is scanning... Ctrl+C to exit back to main menu.')
                        print('Scan progress: '+str(scan_metricsDict['crawl_and_audit_progress'])+'% complete.\n')
                        time.sleep(10)
                        if progress == 100:
                            print('Task_ID '+data['task_id']+' scan successful.\n')
                except:
                    print(' Check Burp.\n')

    def startBurpScan(self,key,url,scopeURLTemp,configTypeTemp):
        global scopeURL
        global configType
        #targetURL = 'google-gruyere.appspot.com/593948396113602183495718301495133174940'
        targetURL = url
        scopeURL = scopeURLTemp
        configType = configTypeTemp

        burpURL = str('\'http://127.0.0.1:1337/'+str(key)+'/v0.1/scan\'')
        cmdURL = str('curl -vgw "\\n" -X POST {url} -d '.format(url=burpURL))

        if (scopeURL != targetURL) and (scopeURL != ""):
            cmdScope = str(',"scope":{"include":[{"rule":"'+'{url}'.format(url=scopeURL)+'"}],'+'"type":"SimpleScope"},"urls":["'+'{url}'.format(url=scopeURL)+'"]}\'')
        else:
            scopeURL = targetURL
            cmdScope = str(',"scope":{"include":[{"rule":"'+'{url}'.format(url=targetURL)+'"}],'+'"type":"SimpleScope"},"urls":["'+'{url}'.format(url=targetURL)+'"]}\'')
        cmdConfig = str('\''+'{"scan_configurations":[{"name":"Crawl and Audit - Fast","type":"NamedConfiguration"''}]')

        cmd = str(cmdURL+cmdConfig+cmdScope)
        announcement = 'echo '+'\''+configType+' scan on '+targetURL+' with a scope of '+scopeURL+'\' | lolcat'
        os.system(announcement)

        if configType == "None":
            confirm = input('\nWould you like to proceed? y/n '+colored('- Warning, no scan config selected.\n','red',attrs=['bold']))
            if confirm == 'y':
                print(colored('No config type specified. Please try again.\n','red',attrs=['bold']))
                burp.burpSelections()
            elif confirm == 'n':
                os.system('clear')
                burp.burpSelections()
            else:
                os.system('clear')
                invalidSelection(confirm)
                burp.startBurpScan(key,url,scopeURLTemp,configTypeTemp)
        else:
            confirm = input('\nWould you like to proceed? y/n\n')
            if confirm == 'y':
                os.system(cmd)
            elif confirm == 'n':
                os.system('clear')
                burp.burpSelections()
            else:
                os.system('clear')
                invalidSelection(confirm)
                burp.startBurpScan(key,url,scopeURLTemp,configTypeTemp)

    def burpSelections(self):
        global key
        global scopeURL
        global configType

        if key == "":
            burp.burpLanding()
        else:
            validURL = True
            validAPI = True
            while validAPI == True:
                #print(colored('Burp Key is: ','white', attrs=['bold'])+storeKey())
                print(colored('\nTarget URL is: ','white', attrs=['bold'])+url)
                print(colored('Scan Scope is: ','white', attrs=['bold'])+scopeURL)
                print(colored('Scan Configuration is: ','white', attrs=['bold'])+configType)

                print(colored('\n*** Preparing BURPSUITE ***','yellow',attrs=['bold','blink']))
                print('1. Launch Scan')
                print('2. Change Scope (Default is Target URL)')
                print('3. Change Scan Configuration')
                print('4. View Report')
                print('5. Update API Key ')

                print(colored('\n0. Change Target','red', attrs=['bold']))
                print(colored('99. Go Back','red', attrs=['bold']))

                selected = input('\nChoose an option to proceed: ')
                if selected == '1':
                    os.system('clear')
                    print(colored('*** Launching Burp Scan (NOTE: 10s scan progress refresh interval) ***','yellow',
                                  attrs=['bold']))
                    burp.startBurpScan(key,url,scopeURL,configType)
                    burp.refreshBurpScan(key)

                elif selected == '2':
                    os.system('clear')
                    print(colored('*** Enter new Target Scope URL or "',attrs=['bold'])+(colored('99','red', attrs=['bold'])+colored('" to go back: ***','white',attrs=['bold'])))
                    scopeURL = input()

                    if scopeURL == '99':
                        scopeURL = ""
                        os.system('clear')
                        burp.burpSelections()
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
                    print(colored('99. Go Back','red', attrs=['bold']))

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
                        burp.burpSelections()
                    else:
                        invalidSelection(selected)

                elif selected == '4':
                    os.system('clear')
                    print('***REPORT VIEWING IS WIP***\n')

                elif selected == '5':
                    os.system('clear')
                    validAPI = False
                    burp.api()

                elif selected == '99':
                    os.system('clear')
                    initial(validURL,url,output)

                elif selected == '0':
                    changeTarget(validURL,url)

                else:
                    invalidSelection(selected)
                    burp.burpSelections()

    def burpLanding(self):
        global key
        validURL = True
        burp = BURPSUITE()
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
                print(colored('\n0. Change Target','red', attrs=['bold']))
                print(colored('99. Go Back','red', attrs=['bold']))

                selected = input('\nChoose an option to proceed: ')
                if selected == '5':
                    burp.api()

                elif selected == '99':
                    os.system('clear')
                    initial(validURL,url,output)

                elif selected == '0':
                    changeTarget(validURL,url)

                else:
                    os.system('clear')
                    print(colored('Error. Did you forget your API key?\n','red',attrs=['bold']))
                    continue
        else:
            burp.burpSelections()

##class QUALYS:
##    def qualysLanding(self):
##        print(colored('\n1. "Run Monday"','white',attrs=['bold']))
##        print(colored('2. "Run Friday"','white',attrs=['bold']))
##        print(colored('3. Create New Sets','green', attrs=['bold']))
##        print(colored('99. Go Back','red', attrs=['bold']))
##
##        selected = input('Choose an option to proceed: ')
##        try:
##            #Run Monday Script
##            if selected == "1":
##                os.chdir('/home/kali/Desktop/Qualys Scripts/For_Elizabeth/')
##                os.system('sh run_monday')
##
##            #Run Friday Script
##            elif selected == "2":
##                os.chdir('/home/kali/Desktop/Qualys Scripts/For_Elizabeth/')
##                os.system('sh run_friday')
##
##            #Create New Sets & Delete Old
##            elif selected == "3":
##                if len(os.listdir('/home/kali/Desktop/Qualys Scripts/For_Elizabeth/BMI_XMLs/')) == 0:
##                    print("Directory is empty")
##                else:
##                    os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/*')
##
##                os.chdir('/home/kali/Desktop/Qualys Scripts/Test/')
##
##                os.system('sh create_set1')
##                os.system('sh create_set2')
##
##                os.system('cp -a /home/kali/Desktop/Qualys\ Scripts/Test/. /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/')
##                os.chdir('/home/kali/Desktop/Qualys Scripts/For_Elizabeth/BMI_XMLs/')
##                os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/create_set1')
##                os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/create_set2')
##                os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/file1.txt')
##                os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/file2.txt')
##                os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/README.txt')
##                os.system('rm /home/kali/Desktop/Qualys\ Scripts/For_Elizabeth/BMI_XMLs/update_test.xml')
##
##                os.chdir('/home/kali/Desktop/Qualys Scripts/Test/')
##                for file in os.listdir('/home/kali/Desktop/Qualys Scripts/Test/'):
##                    if file.startswith("update1_") or file.startswith("update2_"):
##                        command = 'rm '+str(file)
##                        os.system(command)
##
##            elif selected == '99':
##                os.system('clear')
##
##            else:
##                invalidSelection(selected)
##                obj = QUALYS
##                obj.qualysLanding(self)
##        except:
##               print(colored('Error. Is the directory on your desktop?\n','red',attrs=['bold']))
##
##def wappalyzer():
##    global output
##    global url
##
##    try:
##        os.chdir('html')
##        with open(output, "a") as f:
##            webpage = WebPage.new_from_url(url)
##            warnings.filterwarnings('ignore', message="""Caught 'unbalanced parenthesis at position 119' compiling regex""", category=UserWarning )
##
##            wappalyzer = Wappalyzer.latest()
##            print(wappalyzer.analyze_with_versions_and_categories(webpage))
##
##            f.write(str(wappalyzer.analyze_with_versions_and_categories(webpage)))
##            print('Running Wappalyzer technology detector on {}'.format(url))
##            f.close()
##        os.chdir(home)
##        print('Wappalyzer Successfully Executed')
##
##    except:
##        os.chdir(home)
##        print(colored('Whoops! Something went wrong. Please try again.', 'red',))
##
######################################### END OF API SECTION #######################################
######################################### BEGINNING OF TOOL SECTION #######################################
##
##class EXPLOITS:
##    def __init__(self):
##        self.url = url
##        self.output = output
##
##    def MSWmap(self):
##        global url
##        global output
##        url = self.url
##        orig = str(self.url)
##        output = self.output
##
##        try:
##            print('Lauching WMAP Scanner through Metasploit on {}'.format(self.url))
##            #regular expression to replace all link issues i.e. / & .
##            rep = {"https://": "", "http://": ""} #define desired replacements here
##
##            #these three lines do the replacing
##            rep = dict((re.escape(k), v) for k, v in rep.items())
##            pattern = re.compile("|".join(rep.keys()))
##            new = (pattern.sub(lambda m: rep[re.escape(m.group(0))], orig))
##            ip = socket.gethostbyname(new)
##
##            cmd = str('msfconsole -q -p wmap -x '+"'"+'wmap_sites -d 0;wmap_targets -c;wmap_sites -a '+ip+';wmap_targets -d 0;wmap_run -p /home/kali/komodo/fav_modules;exit'+"'"+"| tee /dev/stderr | txt2html -extract -8 >> html/{file}".format(file=output))
##            os.system(cmd)
##        except:
##            print(colored('Whoops! Something went wrong. Please try again.', 'red',))
##
class VULNERABILITY:
    def __init__(self):
        self.url = url


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

        url = self.url


        try:
            print('Running WPScan Against {}'.format(self.url))
            cmd = str('wpscan --url {url} --no-update --no-banner | tee /dev/stderr | txt2html -extract'.format(url=self.url))
            cmdOutput = pipeHelper(cmd)
            ### OUTPUT MODIFICATION HERE



            ### OUTPUT MODIFICATION HERE
            return cmdOutput
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

    # Network Mapper
    def nmap(self):
        global url
        url = self.url


        try:
            print("Launching aggressive NMAP Scan\n")
            orig = str(self.url)

            if 'https://' in orig:
                new = orig.replace('https://',"",1)
            elif 'http://' in orig:
                new = orig.replace('http://',"",1)

            #cmd = str('nmap -v -A -T5 {url} --stats-every 30m| tee /dev/stderr | txt2html -extract -8 >> html/{file}'.format(url=new, file=output))

            cmd = str('nmap -v -A -T5 {url} --stats-every 30m | tee /dev/stderr | txt2html --extract'.format(url=new))
            cmdOutput = pipeHelper(cmd)
            ### OUTPUT MODIFICATION HERE



            ### OUTPUT MODIFICATION HERE
            print('Nmap Successfully Executed')
            return cmdOutput
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))


    # Network Mapper
    def traceroute(self):
        global url
        url = self.url


        try:
            print("Launching Traceroute Scan\n")
            orig = str(self.url)

            if 'https://' in orig:
                new = orig.replace('https://',"",1)
            elif 'http://' in orig:
                new = orig.replace('http://',"",1)

            cmd = str('traceroute {url} | tee /dev/stderr| txt2html --extract'.format(url=new))
            cmdOutput = pipeHelper(cmd)

            ### OUTPUT MODIFICATION HERE
            rep = {"\\n": "<br>", "b'": "","'":""} # define desired replacements here
            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            cmdOutputClean = pattern.sub(lambda m: rep[re.escape(m.group(0))], str(cmdOutput))
            ### OUTPUT MODIFICATION HERE

            return cmdOutputClean
            print('Traceroute Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

    # Test TLS/SSL Encryption
    def testssl(self):
        global url
        url = self.url


        try:
            print("Launching TestSSL Scan\n")
            os.chdir(home+'/testssl.sh')

            cmd = str('./testssl.sh -s -p -h --vulnerabilities {url} | tee /dev/stderr | txt2html --extract'.format(url=url))
            cmdOutput = pipeHelper(cmd)
            ### OUTPUT MODIFICATION HERE



            ### OUTPUT MODIFICATION HERE
            os.chdir(home)
            return cmdOutput
            print('TestSSL Successfully Executed')
        except:
            os.chdir(home)
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

    # Whatweb Lookup
    def whatweb(self):
        global url
        url = self.url


        try:
            print("Launching WhatWeb Scan\n")

            cmd = str('whatweb {url} --color=never | tee /dev/stderr | txt2html --extract'.format(url=url))
            cmdOutput = pipeHelper(cmd)
            ### OUTPUT MODIFICATION HERE



            ### OUTPUT MODIFICATION HERE
            return cmdOutput
            print('WhatWeb Successfully Executed')
        except:

            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

    # WHOIS Lookup
    def whois(self):
        global url
        url = self.url
        orig = str(self.url)


        try:
            print("Launching WHOIS Scan\n")
            #regular expression to replace all link issues i.e. / & .
            rep = {"https://": "", "http://": ""} #define desired replacements here

            #these three lines do the replacing
            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            new = (pattern.sub(lambda m: rep[re.escape(m.group(0))], orig))
            ip = socket.gethostbyname(new)

            cmd = str('whois '+ip+'| tee /dev/stderr | txt2html --extract')
            cmdOutput = pipeHelper(cmd)
            ### OUTPUT MODIFICATION HERE



            ### OUTPUT MODIFICATION HERE
            return cmdOutput
            print('WHOIS Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

    # URL Reputation Checker
    def checkURL(self):
        global url
        url = self.url

        try:
            print("Launching CheckURL Scan\n")
            os.chdir(home+'/checkURL')

            cmd = str('python checkURL.py --url {url} | txt2html --extract'.format(url=url))
            cmdOutput = pipeHelper(cmd)
            ### OUTPUT MODIFICATION HERE
        except:
            os.chdir(home)
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

        if 'Evil URL NOT detected' in str(cmdOutput):
            cmdOutput = 'Evil URL NOT detected'
            os.chdir(home)
            return cmdOutput
        else:
            cmdOutput = 'Evil URL detected'
            os.chdir(home)
            return cmdOutput

    # Brute force directories and file names on web application servers
    def gobuster(self):
        global url
        url = self.url


        try:
            print("Launching GoBuster Scan\n")

            cmd = str('gobuster dir -u {url} -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -q | tee /dev/stderr | txt2html -extract'.format(url=self.url))
            cmdOutput = pipeHelper(cmd)
            ### OUTPUT MODIFICATION HERE



            ### OUTPUT MODIFICATION HERE
            os.chdir(home)
            return cmdOutput
            print('WhatWeb Successfully Executed')
        except:
            print(colored('Whoops! Something went wrong. Please try again.', 'red',))

####################################### END OF TOOL SECTION #######################################

def write(soup):
    os.chdir(home+'/html')
    with open(outputFile,'w') as f:
        f.write(str(soup))
    os.chdir(home)

def pipeHelper(cmd):
    proc=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, )
    cmdOutput = proc.communicate()[0]
    return cmdOutput

def createHTML(url,fileName):
    os.chdir('html')
    replacements = {'NULL':url}
    outputFile = fileName

    if os.path.isfile(fileName):
        with open(fileName, 'r') as f:
            #outputFile = f.read()
            print('File exists.')
        os.chdir(home)
        return outputFile
    else:
        with open('default.html') as infile, open(fileName, 'w') as outfile:
            for line in infile:
                for src, dest in replacements.items():
                    line = line.replace(src, dest)
                outfile.write(line)
        print('File does not exist.')
        os.chdir(home)
        return outputFile

def toolTagHelper(divName,tools,selection,cmdOutput,headerNumTemp):
    headerNum = headerNumTemp+1
    newHeader = '<h'+str(headerNum)+'>'
##    toolTags = ['\n','<button name='+divName+' type="button" class="collapsible">'+tools[selection]+'</button>',
##                '\n','<div name ='+divName+' class="content"><p>'+str(cmdOutput)+'</p>','<br>','\n',newHeader]
    toolTags = ['\n','<button name='+divName+' type="button" class="collapsible">'+tools[selection]+'</button>',
                '\n','<div name ='+divName+' class="content"><p>'+str(cmdOutput)+'</p>','<br>','</div>','\n',]
    return toolTags

##def scanHeaderHelper(tags):
##
##
##    return initialTags

##def landingHelper(url,outputFileTemp)
##    outputFile = createHTML(url,outputFileTemp)
##    os.chdir(home)
##    return outputFile

def landing(selected,urlTemp,fileNameTemp,outputFileTemp,initialTagsTemp):
    global url
    global outputFile
    global key
    url = str(urlTemp)
    outputFile = outputFileTemp
    fileName = fileNameTemp
    initialTags = initialTagsTemp
    
    validURL = True

    os.chdir(home)
    os.chdir('html')
    
    with open(fileName) as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        divName = 'tool0'

        headerList = soup.find_all(re.compile('^h[1-6]$'))
        headerStr = str(headerList.pop())
        headerStr = headerStr[1:3]
        headerNum = int(headerStr[1:2])
        headerTag = soup.find(headerStr)

        if selected.lower() == 'b':
            burp.burpLanding()

        elif selected.lower() == 'w':
            header("wappalyzer")
            wappalyzer()

        if selected == '1':
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
            print(colored('99. Go Back','red', attrs=['bold']))

            print(colored("-- syntax: 1245 --\n", "yellow"))
            selected = input('Choose an option to proceed: ')

            if selected == '99':
                os.system('clear')
                initial(validURL,url,outputFile)

            else:
                tools = {'1':'NMAP',
                         '2':'Traceroute',
                         '3':'TestSSL',
                         '4':'WhatWeb',
                         '5':'WHOIS',
                         '6':'CheckURL',
                         '7':'GoBuster'}

                for selection in selected:
                    divName = 'tool'+str(selection)
                    if selection == '1':
                        obj = INFORMATION_GATHERING()
                        cmdOutput = obj.nmap() #Start NMAP scan
                        toolTags = toolTagHelper(divName,tools,selection,cmdOutput,headerNum)
                        os.chdir(home)

                    elif selection == '2':
                        obj = INFORMATION_GATHERING()
                        cmdOutput = obj.traceroute() #Start Traceroute scan
                        toolTags = toolTagHelper(divName,tools,selection,cmdOutput,headerNum)
                        os.chdir(home)

                    elif selection == '3':
                        obj = INFORMATION_GATHERING()
                        cmdOutput = obj.testssl() #Start Testssl.sh scan
                        toolTags = toolTagHelper(divName,tools,selection,cmdOutput,headerNum)
                        os.chdir(home)

                    elif selection == '4':
                        obj = INFORMATION_GATHERING()
                        cmdOutput = obj.whatweb() #Start WhatWeb scan
                        toolTags = toolTagHelper(divName,tools,selection,cmdOutput,headerNum)
                        os.chdir(home)

                    elif selection == '5':
                        obj = INFORMATION_GATHERING()
                        cmdOutput = obj.whois() #Start WHOIS scan
                        toolTags = toolTagHelper(divName,tools,selection,cmdOutput,headerNum)
                        os.chdir(home)

                    elif selection == '6':
                        obj = INFORMATION_GATHERING()
                        cmdOutput = obj.checkURL() #Start checkURL scan
                        toolTags = toolTagHelper(divName,tools,selection,cmdOutput,headerNum)
                        os.chdir(home)

                    elif selection == '7':
                        obj = INFORMATION_GATHERING()
                        cmdOutput = obj.gobuster() #Start GoBuster scan
                        toolTags = toolTagHelper(divName,tools,selection,cmdOutput,headerNum)
                        os.chdir(home)

                    else:
                        os.chdir(home)
                        invalidSelection(selected)

                    for k in range(len(toolTags)):
                        #scanHeaderHelper(toolTags[k])

                        initialTags.append(toolTags[k])
                        initialStr = "".join(initialTags)
                headerTag.insert_after(BeautifulSoup(initialStr, 'html.parser'))
                write(soup)
            
            os.chdir(home)

        elif selected == '2':
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
            print(colored('99. Go Back','red', attrs=['bold']))

            print(colored("\n-- syntax: 1245 --", "yellow"))
            selected = input('Choose an option to proceed: ').lower()

            if selected == '99':
                os.system('clear')
                initial(validURL,url,outputFile)

            else:
                tools = {'1':'Nikto',
                         '2':'WPScan',
                         '3':'DotDotPwn',
                         '4':'SQLMap',
                         '5':'Nuclei'}

                for selection in selected:
                    divName = 'tool'+str(selection)
                    if selection == '1':
                        obj = VULNERABILITY() # call the class
                        cmdOutput = obj.nikto() #Start Nikto Scan
                        toolTags = toolTagHelper(divName,tools,selection,cmdOutput)
                        os.chdir(home)
                    elif selection == '2':
                        obj = VULNERABILITY() # call the class
                        cmdOutput = obj.WPScan() #Start WPScan Scan
                        toolTags = toolTagHelper(divName,tools,selection,cmdOutput,headerNum)
                        os.chdir(home)

                    elif selection == '3':
                        obj = VULNERABILITY() # call the class
                        cmdOutput = obj.dotdotpwn() #Start DotDotPwn Scan
                        toolTags = toolTagHelper(divName,tools,selection,cmdOutput)
                        os.chdir(home)

                    elif selection == '4':
                        obj = VULNERABILITY() # call the class
                        cmdOutput = obj.sqlmap() #Start SQLmap Scan
                        toolTags = toolTagHelper(divName,tools,selection,cmdOutput)
                        os.chdir(home)

                    elif selection == '5':
                        obj = VULNERABILITY() # call the class
                        cmdOutput = obj.nuclei() #Start Nuclei Scan
                        toolTags = toolTagHelper(divName,tools,selection,cmdOutput)
                        os.chdir(home)

                    else:
                        os.chdir(home)
                        invalidSelection(selected)

                    for k in range(len(toolTags)):
                        initialTags.append(toolTags[k])
                        initialStr = "".join(initialTags)
                headerTag.insert_after(BeautifulSoup(initialStr, 'html.parser'))
                write(soup)
            os.chdir(home)

        elif selected == '3':
            print(colored('\nCurrent Target: '+url,attrs=['bold']))
            print(colored('\n***Preparing EXPLOIT Scans***','magenta',attrs=['bold','blink']))
            print('1. Metasploit: WMAP - Web App Vuln. Scanner Conducted Within Metasploit framework')
            print(colored('99. Go Back','red', attrs=['bold']))

            print(colored("\n-- syntax: 1245 --", "yellow"))
            selected = input('Choose an option to proceed: ')

            if selected == '99':
                os.system('clear')
                initial(validURL,url,outputFile)

            else:
                for selection in selected:
                    if selection == '1':
                        obj = EXPLOITS() # call the class
                        header("MSWmap")
                        obj.MSWmap() #Start WMAP scan
                        print('Metasploit: WMAP Successfully Executed')

                    else:
                        invalidSelection(selected)

        elif selected == '0':
            os.chdir(home)
            changeTarget(validURL,url)

        elif selected == '99':
            os.chdir(home)
            sys.exit(colored('\nTerminating KOMODO (╯°□°）╯︵ ┻━┻','red', attrs=['bold']))

        else:
            os.chdir(home)
            invalidSelection(selected)



def initial(validURL,urlTemp,fileNameTemp,outputFileTemp):
    x = datetime.datetime.now()
    current_time = "Scan Results: "+ str(x.strftime("%x %I:%M%p"))
    initialTags =['\n','<button name="target" type="button" class="collapsible">'+current_time+'</button>','\n',
                      '<div name="target" class="content">','<p>Please see scan results below.</p>','\n']
    
    while validURL == True:
        global url
        global outputFile
        outputFile = outputFileTemp
        fileName = fileNameTemp
        url = urlTemp
        os.chdir(home)

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
        print(colored('3. Exploits','white'))

        print(colored('\n0. Change Target', 'red', attrs=['bold']))
        print(colored('99. Exit', 'red', attrs=['bold']))

        selection = input('\nChoose a category to proceed: ')
        os.system('clear')

        landing(selection,url,fileName,outputFile,initialTags)
        initialTags = []

def validateURL(validURL, urlTemp):
    global url
    url = urlTemp

    x = datetime.datetime.now()
    current_time = "Scan Results: "+ str(x.strftime("%x %I:%M%p"))
    current_time_adjusted = current_time.replace('/','-')

    #User input for URL Prefix and Target
    while validURL == False:
        selected = input('Enter "1" for '+colored('HTTPS','yellow')+' or "2" for '+colored('HTTP','yellow')+': ')
        if selected == '1':
            target = input('('+colored('HTTPS','yellow')+' Selected) Enter the target URL or IP Address: ')

            #regular expression to replace all link issues i.e. / & . for html files
            rep = {"/": "-", ".com": "", ".": "-"} #define desired replacements here

            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            #output = (pattern.sub(lambda m: rep[re.escape(m.group(0))], target)) + current_time_adjusted+'.html'
            fileName = (pattern.sub(lambda m: rep[re.escape(m.group(0))], target))+'.html'

            url = 'https://'+str(target)
            validURL = True

            print(colored('\nCurrent Target: '+url,attrs=['bold']))
            outputFile = createHTML(url,fileName)
            initial(validURL,url,fileName,outputFile)

        elif selected == '2':
            target = input('('+colored('HTTP','yellow')+' Selected) Enter the target URL or IP Address: ')

            #regular expression to replace all link issues i.e. / & . for html files
            rep = {"/": "-", ".com": "", ".": "-"} #define desired replacements here

            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            #output = (pattern.sub(lambda m: rep[re.escape(m.group(0))], target)) + current_time_adjusted+'.html'
            fileName = (pattern.sub(lambda m: rep[re.escape(m.group(0))], target))+'.html'

            url = 'http://'+str(target)
            validURL = True

            print(colored('\nCurrent Target: '+url,attrs=['bold']))

            outputFile = createHTML(url,fileName)
            initial(validURL,url,fileName,outputFile)
        else:
            invalidSelection(selected)


def validateIntent(validURL,url):
    validIntent = False
    while validIntent == False:
        selected = input('\nEnter "1" for '+colored('Qualys Script Management','yellow')+' or "2" for '+colored('Penetration Testing','red')+': ')
        if selected == '1':
            os.system('clear')
            validIntent = True
            obj = QUALYS()
            obj.qualysLanding()
            validateIntent(validURL,url)
        elif selected == '2':
            validIntent = True
            os.system('clear')
            validateURL(validURL,url)
        else:
            invalidSelection(selected)

def changeTarget(validURL,url):
    os.system('clear')
    validURL = False
    validateURL(validURL,url)

def invalidSelection(selected):
    os.system('clear')
    print('\n['+str(selected)+']'+colored(' Invalid input. Please try again.\n','red',attrs=['bold']))

#Main
def main():
    print('Grabbing latest updates...')
    os.system('git pull')
    os.system('clear')

    #Print KOMODO Title
    print((('*' * 50) + '\n') * 3)
    tprint('    KOMODO')
    print((('*' * 50) + '\n') * 3)

    global url

    os.system("echo 'NEW FEATURES ALERT!\nIntroducing... \n- Full BurpSuite REST API support!\n- Reworked Tool Selection!\n- Friendlier (and fancier) UI!' | lolcat")

    url = ""
    output = ""
    validURL = False

    #Initial Screen
    validateIntent(validURL,url)

if __name__ == '__main__':
    burp = BURPSUITE()
    main()
