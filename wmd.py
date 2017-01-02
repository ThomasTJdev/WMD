#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#


import argparse
from datetime import datetime
import dateutil.relativedelta
import os
import readline  # Used for historical inputs (arrow up possibility)
import signal
import sys
import time
from time import sleep
from core.colors import bc as bc
from core.banners import loadBanner as banner
import core.commands as comm
import core.modules as cmodules
import core.tools as ctools
import core.www as cwww


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--module", help="Run module.", metavar='CALL')
parser.add_argument("-a", "--add", help="Add module.", metavar='PATH.py')
parser.add_argument("-d", "--delete", help="Delete module.", metavar='PATH.py')
parser.add_argument("-w", "--www", action='store_true', help="Start webserver interface.")
parser.add_argument("-nc", "--nocheck", action='store_true', help="Don\'t check for any requirements")
parser.add_argument("-q", "--quite", action='store_true', help="Stay quite. No banner.")
args = parser.parse_args()


def currPath():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    return dname


def timeSinceUpdate():
    try:
        with open('logs/lasttoolupdate.txt', 'r') as f:
            timeString = f.read()
        timeString = datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S").timestamp()
        dt1 = datetime.fromtimestamp(int(timeString))
        dt2 = datetime.fromtimestamp(int(time.time()))
        rd = dateutil.relativedelta.relativedelta(dt2, dt1)
        print('\t[!]  Time since running command "updatetools": %d years, %d months, %d days, %d hours, %d minutes and %d seconds' % (rd.years, rd.months, rd.days, rd.hours, rd.minutes, rd.seconds))
    except:
        print('\t[!]  Tools hasn\'t been updated from within WMD')


def updatetools():
    print('')
    gitinstalled = comm.checkInstalled('git')
    print('')
    if gitinstalled != 'ERROR':
        ctools.clonegits('u')
    else:
        print(bc.FAIL + '\n\t[-] git is not installed and therefore its not possible to automate the update of the tools' + bc.ENDC)
    print('')


def installtools():
    print('')
    gitinstalled = comm.checkInstalled('git')
    print('')
    print('[!]  If the tool is already installed it will NOT BE updated. Use the "updatetools" for updating.')
    print('')
    if gitinstalled != 'ERROR':
        ctools.clonegits('i')
    else:
        print(bc.FAIL + '\n\t[-] git is not installed and therefore its not possible to automate the update of the tools' + bc.ENDC)
    print('')


def runModule():
    module = cmodules.loadModule(str(args.module))
    try:
        print(' ')
        module.main()
    except KeyboardInterrupt:
        print(bc.WARN + '  -> Exiting' + bc.ENDC)
        sleep(1)
    except:
        print(bc.WARN + '  -> ERROR, no module call found with: ' + str(args.module).strip('[]\'') + bc.ENDC)
        sleep(1)
    print(' ')


def usemodule(userinput):
    module = cmodules.loadModule(str(userinput[1:2]))
    try:
        print(' ')
        module.main()
    except KeyboardInterrupt:
        print(bc.WARN + '  -> Exiting' + bc.ENDC)
        sleep(1)
    except:
        print(bc.WARN + '    ERROR, no module call found with: ' + str(userinput[1:2]).strip('[]\'') + bc.ENDC)
    print(' ')


def welcome():
    banner()
    showCommands()


def showCommands():
    print(
        "\n"
        + "   " + bc.OKBLUE + "COMMANDS:" + bc.ENDC
        + "\n   " + "---------"
        + "\n   " + ("%-*s ->\t%s" % (15, "fm", "Show info"))
        + "\n   " + ("%-*s ->\t%s" % (15, "so", "Show options"))
        + "\n   " + ("%-*s ->\t%s" % (15, "sm", "Show modules"))
        + "\n   " + ("%-*s ->\t%s" % (15, "www", "Start webserver menu"))
        + "\n   " + ("%-*s ->\t%s" % (15, "use [module]", "Run the script"))
        + "\n   " + ("%-*s ->\t%s" % (15, "invoke [module]", "Open module in new xterm"))
        + "\n   " + ("%-*s ->\t%s" % (15, "updatetools", "Clone/Install and update tools from local repo and git repos"))
        + "\n   " + ("%-*s ->\t%s" % (15, "installtools", "Clone/Install tools from local repo and git repos"))
        + "\n   " + ("%-*s ->\t%s" % (15, ":[command]", "Run shell commands from within the WMD"))
        + "\n   " + ("%-*s ->\t%s" % (15, "exit", "Exit"))
        + "\n"
        )


# CONSOLE
def console(path):
    value = input("  " + bc.FAIL + "wmd" + bc.ENDC + "@" + bc.FAIL + "console:" + bc.ENDC + " ")
    userinput = value.split()
    if 'fm' in userinput[:1]:
        welcome()
    elif 'so' in userinput[:1]:
        showCommands()
    elif 'sm' in userinput[:1]:
        cmodules.showModules()
    elif 'use' in userinput[:1]:
        usemodule(userinput)
    elif 'invoke' in userinput[:1]:
        comm.invokeModule(str(userinput[1:2]))
    elif 'www' in userinput[:1]:
        print('\t[*]  Start WWW - go look and see "127.0.0.1:5000"' + bc.ENDC)
        cwww.startWWW()
    elif 'updatetools' in userinput[:1]:
        updatetools()
    elif 'installtools' in userinput[:1]:
        installtools()
    elif 'exit' in userinput[:1]:
        sys.exit()
    elif ':' in value[:1]:
        print('')
        os.system(str(value[1:]))
        print('')
    else:
        print(bc.WARN + "\n    error\t> " + str(userinput[:1]) + "\n" + bc.ENDC)
    # Always return to current path:
    os.chdir(path)
    # Always return to console:
    console(path)
# END CONSOLE


# Capture Ctrl+c and exit
def sigint_handler(signum, frame):
    try:
        console()
    except:
        print("  Exiting")
        sys.exit()


def main():
    if args.add:
        cmodules.addModule(args.add)
        print('\n\n')
        return None
    if args.delete:
        cmodules.removeModule(args.delete)
        print('\n\n')
        return None
    if args.module:
        runModule()
        return None
    if not args.nocheck:
        print('\n\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
        timeSinceUpdate()
        comm.checkNetConnectionV()
        comm.getPublicIPV()
        comm.getLocalIP_interfaceV()
        comm.checkNetVPNV()
        comm.checkTorV()
        sleep(1.5)
    if args.www:
        banner()
        cwww.startWWW()
        return None
    if not args.quite:
        print(bc.WARN)
        welcome()
    else:
        print('')
    if os.getuid() != 0:
        print('   ' + bc.WARN + '[!]  You are not running WMDframe as root. You\'ll might encounter some problems.. You have been warned!\n')

    path = currPath()
    console(path)


signal.signal(signal.SIGINT, sigint_handler)    # Capture Ctrl+c and exit
main()
