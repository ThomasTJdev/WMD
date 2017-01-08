#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe

import argparse
import subprocess
from datetime import datetime
from time import sleep
try:
    import core.core as core
    import core.commands as comm
    import core.modules as cmodules
    from core.colors import bc as bc
except:
    import sys
    sys.path.append('././')
    import core.core as core
    import core.commands as comm
    import core.modules as cmodules
    from core.colors import bc as bc


# START Log files, global variables, etc.
parser = argparse.ArgumentParser()
parser.add_argument('-hwa', '--hwaddress', help='Router IP.', metavar='HWA')
parser.add_argument('-r', '--run', action='store_true', help='Start monitoring.')
args, unknown = parser.parse_known_args()

config = core.config()
global arpprogram
ARP_SYM = (config['TOOLS']['ARP_SYM'])
ARP_GITNAME = (config['TOOLS']['ARP_GITNAME'])
ARP_GITRUN = (config['TOOLS']['ARP_GITRUN'])
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'ARP monitor alert'
    Call = 'arpmon'
    Modulename = 'mon_arpmonitoralert'
    Category = 'monitor'
    Type = 'arp'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Monitor ARP table and alert for changes'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    def __init__(self, hwa, time):
        self.hwa = hwa
        self.time = time
        self.show_all()

    # Possible options. These variables are checked when the user tries to 'set' an option
    def poss_opt(self):
        return ('hwa', 'time')

    # Show options
    def show_opt(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 8, 'RQ', 18, 'VALUE', 'DESCRIPTION')) + bc.ENDC
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 8, '--', 18, '-----', '-----------'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'hwa:', 8, 'n', 18, self.hwa, 'Monitor only single HW address. (e.g. 54:d2:fd:s1:9l:8d)'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'time:', 8, 'n', 18, self.time, 'Loop time. Check ARP every nth second'))
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s ->\t%s' % (9, 'run', 'Run the script'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'hosts', 'Check current ARP table'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'info', 'Information'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'so', 'Show options'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'sa', 'Show module info'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'invoke', 'Invoke module'))
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


def run():
    print('\n\t[*]  Scanning for duplicates in ARP every ' + sop.time + ' second')
    if sop.hwa:
        print('\t[*]  Only monitoring HWaddress: ' + sop.hwa)

    firstRun = ''
    counter = 0
    while True:
        counter += 1
        call = arpprogram + ' -v'
        arptable = subprocess.check_output(call, shell=True)
        arptable = arptable.decode()
        arptable = arptable.strip().splitlines()

        if not firstRun:
            print('\t[+]  First dry run:')
            for line in arptable:
                print('\t     -> ' + line)
                firstRun = 'Done'
            print('\n\t[*]  Monitoring started:')

        data = ''
        for line in arptable:
            for prefix in ('Address', 'Entries'):
                if prefix in line:
                    break
            else:
                # If HWA specified, only monitor this
                if sop.hwa:
                    if sop.hwa in line.split()[2]:
                        data += line.split()[2] + '\n'
                else:
                    data += line.split()[2] + '\n'
        data = data.split()
        seen = set()
        for x in data:
            if x not in seen:
                seen.add(x)
                pass
            else:
                print(bc.FAIL + '\t[!]  ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '  Duplicated HW address found for: ' + x + bc.ENDC)
                for line in arptable:
                    if x in line:
                        print(bc.WARN + '\t     -> ' + line.split()[2] + '  ' + line.split()[4] + '  ' + line.split()[3] + '  ' + line.split()[0] + '  ' + line.split()[1] + '  ' + bc.ENDC)

        if counter % 30 == 0 and counter != 0:
            print('\t[*]  ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '  I\'m still alive. Just finished ' + str(counter) + ' checks.')

        sleep(int(sop.time))


def hosts():
    print('')
    call = arpprogram + ' -v'
    arptable = subprocess.check_output(call, shell=True)
    arptable = arptable.decode()
    arptable = arptable.strip().splitlines()
    for line in arptable:
        print('\t     -> ' + line)
    print('')


def info():
    print("""
        This modules scans your ARP table and checking for duplicates,
        which could indicate a MITM attack (Man In The Middle).
        When a duplicate is detected, you\'ll get a warning!

        See more about ARP spoofing here: https://en.wikipedia.org/wiki/ARP_spoofing

        Requirements: arp""")

    if parser.format_help():
        print('\n\t' + bc.OKBLUE + 'COMMANDLINE ARGUMENTS:' + bc.ENDC)
        for line in parser.format_help().strip().splitlines():
            print('\t' + line)
    print('')


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'arpmon:' + bc.ENDC + ' ')
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'info' in userinput[:1]:
        info()
    elif 'run' in userinput[:1]:
        run()
    elif 'hosts' in userinput[:1]:
        hosts()
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
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + '\n    Error, no options for: ' + command + '\n' + bc.ENDC)
    console()
# END console


def main():
    print('\n')
    print('      ___    ____  ____                           ')
    print('     /   |  / __ \/ __ \   ____ ___  ____  ____   ')
    print('    / /| | / /_/ / /_/ /  / __ `__ \/ __ \/ __ \  ')
    print('   / ___ |/ _, _/ ____/  / / / / / / /_/ / / / /  ')
    print('  /_/  |_/_/ |_/_/      /_/ /_/ /_/\____/_/ /_/   ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    global arpprogram
    arpprogram = comm.checkInstalledFull(ARP_SYM, ARP_GITNAME, ARP_GITRUN)
    print('')
    global sop
    # The parameters to be passed to the module on init
    if args.hwaddress:
        sop = options(str(args.hwaddress), '30')
    else:
        sop = options('', '30')
    if args.run:
        run()
    else:
        console()


if args.run:
    main()


# For testing uncomment "main()" and run module with "python3 modulename.py"
# main()
