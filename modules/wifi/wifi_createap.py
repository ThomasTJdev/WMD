#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


# LIBRARIES
import configparser
import os                   # Running bettercap
from time import sleep      # Just counting down before launch
try:
    from core.colors import bc as bc
    import core.modules as cmodules
    import core.commands as comm
except:
    import sys
    sys.path.append('././')
    from core.colors import bc as bc
    import core.modules as cmodules
    import core.commands as comm
# END LIBRARIES


config = configparser.ConfigParser()
config.read('core/config.ini')


# VARIABLES
CREATEAP = (config['TOOLS']['CREATEAP_SYM'])
INTERFACE_NET = (config['NETWORK']['INTERFACE_NET'])
INTERFACE_MON = (config['NETWORK']['INTERFACE_MON'])
# END VARIABLES


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Create an Accesspoint'
    Call = 'createap'
    Modulename = 'wifi_createap'
    Category = 'wifi'
    Type = 'accesspoint'
    Version = '0.1'
    License = 'MIT'
    Description = 'Create an Accesspoint'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    def __init__(self, INTERFACE_NET, INTERFACE_MON, gateway, mode, name, daemon, logfile):
        self.int_net = INTERFACE_NET
        self.int_mon = INTERFACE_MON
        self.gateway = gateway
        self.mode = mode
        self.name = name
        self.daemon = daemon
        self.logfile = logfile
        self.show_all()

    # Possible options
    def poss_opt(self):
        return ('int_net', 'int_mon', 'gateway', 'mode', 'name', 'daemon', 'logfile')

    # Show options
    def show_opt(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 6, 'RQ', 15, 'VALUE', 'DESCRIPTION')) + bc.ENDC
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 6, '--', 15, '-----', '-----------'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'int_net:', 6, 'y', 15, self.int_net, 'Active interface for net-connection'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'int_mon:', 6, 'y', 15, self.int_mon, 'WIFI device which can goto to monitor mode'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'gateway:', 6, 'y', 15, self.gateway, 'Gateway, e.g. 192.168.1.1'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'mode:', 6, 'n', 15, self.mode, 'Mode empty=auto (bridge/nat)'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'name:', 6, 'n', 15, self.name, 'Access Point name'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'daemon:', 6, 'n', 15, self.daemon, 'Run as daemon (y/N)'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'logfile:', 6, 'n', 15, self.logfile, 'Logfile for connections'))
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s ->\t%s' % (9, 'run', 'Run the script'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'ap', 'Show running AP\'s (showing ID\'s)'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'clients [AP id]', 'Show connected clients'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'stop [AP id]', 'Stop daemon'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'info', 'Information'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'so', 'Show options'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'sa', 'Show module info'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'exit', 'Exit'))
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


# RUN BETTERCAP
def run():
    # Start the AP
    command = (CREATEAP + ' ' + sop.int_mon + ' ' + sop.int_net + ' ' + sop.name)

    if.sop_gateway:
        command + ' -g ' + sop.gateway
    if sop.mode:
        command += ' -m ' + sop.mode

    if sop.daemon == 'y':
        command += ' --daemon'

    if sop.logfile:
        command += ' >> ' + sop.logfile

    print(
        '\n'
        + '\t' + 'Loading     : Create_ap'
        + '\n\t' + 'Command     : ' + bc.BOLD + command + bc.ENDC
        + '\n\t' + 'Starting in : 2 seconds'
        + '\n\t'
        )
    sleep(2)

    if sop.daemon == 'y':
        os.system(command)
    else:
        comm.runCommand(command, 'Create_AP')
# END


def ap():
    print('')
    os.system('create_ap --list-running')
    print('')


def clients(id):
    print('')
    os.system('create_ap --list-clients ' + id)
    print('')


def stop(id):
    print('')
    os.system('create_ap --stop ' + id)
    print('')


def info():
    print("""
        Module for use in WMDframe.""")


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'APsniff:' + bc.ENDC + ' ')
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'help' in userinput[:1]:
        print('\n\n###########################################################')
        print('#  CREATE_AP')
        print('###########################################################\n')
    elif 'info' in userinput[:1]:
        info()
    elif 'run' in userinput[:1]:
        run()
    elif 'ap' in userinput[:1]:
        ap()
    elif 'clients' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        clients(useroption)
    elif 'stop' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        stop(useroption)
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
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + '\n    Error, no options for: ' + command + '\n' + bc.ENDC)
    console()
# END console


# STARTER
def main():
    print('\n')
    print('\t   ______                __          ___    ____   ')
    print('\t  / ____/_______  ____ _/ /____     /   |  / __ \  ')
    print('\t / /   / ___/ _ \/ __ `/ __/ _ \   / /| | / /_/ /  ')
    print('\t/ /___/ /  /  __/ /_/ / /_/  __/  / ___ |/ ____/   ')
    print('\t\____/_/   \___/\__,_/\__/\___/  /_/  |_/_/        ')
    print('\n')
    if os.getuid() != 0:
        print('r00tness is needed due to packet sniffing!')
        print('Run the script again as root/sudo')
        return None
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkInstalled(CREATEAP)
    comm.checkNetConnectionV()
    print('\n')
    gateway = comm.getGateway()
    global sop
    sop = options(INTERFACE_NET, INTERFACE_MON, '', '', 'FreeWifi', '', '')
    console()
