#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import netifaces
import os
from time import sleep
try:
    import core.core as core
    import core.commands as comm
    import core.modules as cmodules
    import core.wifi as cwifi
    from core.colors import bc as bc
except:
    import sys
    sys.path.append('././')
    import core.core as core
    import core.commands as comm
    import core.modules as cmodules
    import core.wifi as cwifi
    from core.colors import bc as bc


# START Log files, global variables, etc.
config = core.config()
logger = core.log()
INTERFACE_MON = (config['NETWORK']['INTERFACE_MON'])
AIRMONNG_SYM = (config['TOOLS']['AIRMONNG_SYM'])
AIRODUMPNG_SYM = (config['TOOLS']['AIRODUMPNG_SYM'])
AIREPLAYNG_SYM = (config['TOOLS']['AIREPLAYNG_SYM'])
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'WiFi utils'
    Call = 'wifiutils'
    Modulename = 'wifi_utils'  # Filename
    Category = 'wifi'
    Type = 'wifi'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Utilities for WiFi, e.g. deauth, WiFi\'s, clients, probes, etc.'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    def __init__(self, int_mon):
        self.int_mon = int_mon
        self.show_all()

    # Possible options. These variables are checked when the user tries to 'set' an option
    def poss_opt(self):
        return ('int_mon')

    # Show options
    def show_opt(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 8, 'RQ', 18, 'VALUE', 'DESCRIPTION')) + bc.ENDC
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 8, '--', 18, '-----', '-----------'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'int_mon:', 8, 'y', 18, self.int_mon, 'Monitoring interface'))
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            '\n\t' + bc.BOLD + bc.WARN + 'REMEMBER TO SET YOU DEVICE INTO MONITORING MODE!! RUN "setmon"' + bc.ENDC
            + '\n'
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s ->\t%s' % (14, 'run', 'Run the script'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'setmon', 'Set interface in monitoring mode'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'setc [channel]', 'Problems with your monitoring device on wrong channel?'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'wifi', 'Show WiFi\'s'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'probes', 'Show probes (only unique values are shown)'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'beacons', 'Show beacons (only unique values are shown)'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'probea', 'Show probes and beacons'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'clients', 'Show connected clients, requires: [AP BSSID] [AP CHANNEL]'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'clientslog', 'Show connected clients and logs handshake to logfile, requires: [AP BSSID] [AP CHANNEL] [LOGFILE]'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'deauth', 'Deauth client from AP, requires: [AP BSSID] [CLIENT BSSID]'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'info', 'Information'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'set', 'Set interface in monitoring mode'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'so', 'Show options'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'sa', 'Show module info'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'invoke', 'Invoke module'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'exit', 'Exit'))
            + '\n'
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
    print('\tRunning running')


def defineMon(interface):
    setattr(sop, 'int_mon', interface)


def setmon():
    os.system(cwifi.setDeviceMon(sop.int_mon, ''))
    sleep(0.5)
    print('')


def setc():
    i_channel = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'Specify channel or leave blanck:' + bc.ENDC + ' ')
    print('\t[*]  Setting interface in monitoring mode')
    os.system(cwifi.setDeviceMon(sop.int_mon, i_channel))
    sleep(0.5)
    print('')



def wifi():
    print('')
    comm.runCommand(cwifi.showWifis(sop.int_mon), 'WiFis')
    print('')


def clients():
    print('')
    i_bssid = ''
    i_channel = ''
    print('\n\t[!]  Insert the BSSID and channel for target')
    while not i_bssid:
        i_bssid = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert BSSID:' + bc.ENDC + ' ')
    while not i_channel:
        i_channel = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert channel:' + bc.ENDC + ' ')
    print('\t[*]  Starting xterm showing client\'s')
    print('\t[!]  Locate the BSSID for the client connected to the target accesspoint')
    print('\t[!]  Freeze the display in new xterm with "Ctrl+c"')
    comm.runCommand2(cwifi.showConnClients(sop.int_mon, i_bssid, i_channel, ''), 'Find_CLIENTS')
    print('')


def clientslog():
    print('')
    i_bssid = ''
    i_channel = ''
    i_logfile = ''
    if i_logfile:
        print('\t[*]  Using logfile:' + str(i_logfile))
    print('\n\t[!]  Insert the BSSID and channel for target')
    while not i_bssid:
        i_bssid = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert BSSID:' + bc.ENDC + ' ')
    while not i_channel:
        i_channel = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert channel:' + bc.ENDC + ' ')
    while not i_logfile:
        i_logfile = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert channel:' + bc.ENDC + ' ')
    print('\t[*]  Starting xterm showing client\'s')
    print('\t[!]  Locate the BSSID for the client connected to the target accesspoint')
    print('\t[!]  Freeze the display in new xterm with "Ctrl+c"')
    comm.runCommand2(cwifi.showConnClients(sop.int_mon, i_bssid, i_channel, i_logfile), 'MONITORING_HANDSHAKE')
    print('')


def deauth():
    print('')
    i_bssid = ''
    i_client = ''
    print('\n\t[!]  Insert the BSSID and channel for target')
    while not i_bssid:
        i_bssid = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert BSSID:' + bc.ENDC + ' ')
    while not i_client:
        i_client = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert client STATION:' + bc.ENDC + ' ')
    print('\t[*]  Starting deauthing client')
    gotWPA = 'd'
    while gotWPA.lower() == 'd':
        os.system(cwifi.deauthClient(sop.int_mon, i_bssid, i_client, '1'))
        print('\t[!]  Deauth with 1 package done. Got the handshake in the monitoring xterm?')
        gotWPA = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + '(d)eauth again or (e)nd:' + bc.ENDC + ' ')


def probes():
    print('')
    cwifi.runProbes(sop.int_mon)
    print('')


def beacons():
    print('')
    cwifi.runBeacons(sop.int_mon)
    print('')


def probea():
    print('')
    cwifi.runBeaconNProbes(sop.int_mon)
    print('')


def info():
    print("""
        Module for use in WMDframe.

        Various tools for WiFi""")


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'WiFiutils:' + bc.ENDC + ' ')
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'setmon' in userinput[:1]:
        setmon()
    elif 'wifi' in userinput[:1]:
        wifi()
    elif 'deauth' in userinput[:1]:
        deauth()
    elif 'clients' in userinput[:1]:
        clients()
    elif 'clientslog' in userinput[:1]:
        clientslog()
    elif 'probes' in userinput[:1]:
        probes()
    elif 'beacons' in userinput[:1]:
        beacons()
    elif 'probea' in userinput[:1]:
        probea()
    elif 'info' in userinput[:1]:
        info()
    elif 'pd' in userinput[:1]:
        predefinedCommands()
    elif 'run' in userinput[:1]:
        run()
    elif 'runcom' in userinput[:1]:
        runcom(str(userinput[1:]).strip('[]\''))
    elif 'set' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        uservalue = str(userinput[2:3]).strip('[]\'')  # Use single word after "set parameter"
        # uservalue = value.split(' ', 2)[2]  # Use all text after "set parameter"
        if useroption not in sop.poss_opt():
            print(bc.WARN + '\n    Error, no options for: ' + useroption + '\n' + bc.ENDC)
        elif useroption in sop.poss_opt():
            setattr(sop, useroption, uservalue)
            print('\n      ' + useroption + '\t> ' + uservalue + '\n')
    elif 'invoke' in userinput[:1]:
        comm.invokeModule(options.Call)
        return None
    elif 'back' in userinput[:1] or 'exit' in userinput[:1]:
        return None
    elif ':' in userinput[:1]:
        print('')
        os.system(str(value[1:]))
        print('')
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + '\n    Error, no options for: ' + command + '\n' + bc.ENDC)
    console()
# END console


def main():
    print('\n')
    print('\t _       ___ _____                          _   ')
    print('\t| |     / (_) __(_)  ____ ___  ____  ____  (_)  ')
    print('\t| | /| / / / /_/ /  / __ `__ \/ __ \/ __ \/ /   ')
    print('\t| |/ |/ / / __/ /  / / / / / / /_/ / / / / /    ')
    print('\t|__/|__/_/_/ /_/  /_/ /_/ /_/\____/_/ /_/_/     ')
    print('\n')
    if os.getuid() != 0:
        print(bc.FAIL + '\t[-]  r00tness is needed due to XXX!')
        print('\t[-]  Run the script again as root/sudo' + bc.ENDC)
        return None
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    tmpInt = cwifi.checkDeviceMon(INTERFACE_MON)
    if not tmpInt:
        tmpInt = INTERFACE_MON
        print(bc.FAIL + '\t[-]  Device not found.. Exiting..' + bc.ENDC)
        return None
    else:
        print(bc.OKGREEN + '\t[+]  Device set to: ' + tmpInt + bc.ENDC)
    comm.checkInstalledOpt(AIRMONNG_SYM)
    comm.checkInstalledOpt(AIRODUMPNG_SYM)
    comm.checkInstalledOpt(AIREPLAYNG_SYM)
    print('')
    global sop
    # The parameters to be passed to the module on init
    sop = options(tmpInt)
    console()


# For testing uncomment "main()" and run module with "python3 modulename.py"
# main()
