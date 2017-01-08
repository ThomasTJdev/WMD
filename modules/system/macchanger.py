#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import argparse
import os
import random
import string
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
# Parser
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mac', help='MAC address', metavar='MAC') # Example. Use with "args.lanip"
parser.add_argument('-i', '--interface', help='Interface to change', metavar='INT') # Example. Use with "args.lanip"
parser.add_argument('-r', '--run', action='store_true', help='Change MAC')
args, unknown = parser.parse_known_args()

config = core.config()
INTERFACE_NET = (config['NETWORK']['INTERFACE_NET'])
MACS = (config['FILES']['MACS'])
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Macchanger'
    Call = 'macc'
    Modulename = 'macchanger'  # Filename
    Category = 'system'
    Type = 'mac'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Change your MAC address'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    def __init__(self, mac, int):
        self.mac = mac
        self.int = int
        self.show_all()

    # Possible options. These variables are checked when the user tries to 'set' an option
    def poss_opt(self):
        return ('mac', 'int')

    # Show options
    def show_opt(self):
        current_mac = comm.getMac()
        print(
            ''
            + '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 8, 'RQ', 18, 'VALUE', 'DESCRIPTION')) + bc.ENDC
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 8, '--', 18, '-----', '-----------'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'mac:', 8, 'y', 18, self.mac, 'MAC address'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'int:', 8, 'y', 18, self.int, 'Interface to change MAC for'))
            + '\n'
            + '\n\t' + bc.ITALIC + 'Current MAC: ' + current_mac + bc.ENDC
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s ->\t%s' % (15, 'run', 'Run the script'))
            + '\n\t' + ('%-*s ->\t%s' % (15, 'show', 'Show list of MACs'))
            + '\n\t' + ('%-*s ->\t%s' % (15, 'search [term]', 'Search for MAC, e.g. "search Apple"'))
            + '\n\t' + ('%-*s ->\t%s' % (15, 'rnd', 'Get a random MAC'))
            + '\n\t' + ('%-*s ->\t%s' % (15, 'info', 'Information'))
            + '\n\t' + ('%-*s ->\t%s' % (15, 'so', 'Show options'))
            + '\n\t' + ('%-*s ->\t%s' % (15, 'sa', 'Show module info'))
            + '\n\t' + ('%-*s ->\t%s' % (15, 'set', 'Set options, set [PARAMETER] [VALUE]'))
            + '\n\t' + ('%-*s ->\t%s' % (15, 'invoke', 'Invoke module'))
            + '\n\t' + ('%-*s ->\t%s' % (15, 'exit', 'Exit'))
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
    print('')
    current_mac = comm.getMac()
    if not sop.int:
        print(bc.FAIL + '\t[!]  Please define your interface' + bc.ENDC)
    if not sop.mac:
        print(bc.FAIL + '\t[!]  Please define a MAC address' + bc.ENDC)
    else:
        try:
            print('\t[*]  Taking down your interface')
            os.system('ifconfig ' + sop.int + ' down')
            print('\t[*]  Setting your new MAC address')
            os.system('ifconfig ' + sop.int + ' hw ether ' + sop.mac)
            print('\t[*]  Setting your interface up')
            os.system('ifconfig ' + sop.int + ' up')
            print(bc.OKGREEN + '\t[+]  Job done! New MAC address assigned.' + bc.ENDC)
        except:
            print(bc.FAIL + '\t[-]  Something went wrong!' + bc.ENDC)
            print('\t[*]  Setting your interface up again')
            os.system('ifconfig ' + sop.int + ' up')
            print(bc.FAIL + '\t[-]  Take care and recheck your MAC!' + bc.ENDC)

    print('')
    print('\tOriginal mac: ' + current_mac)
    new_mac = comm.getMac()
    print('\tNew mac:      ' + new_mac)
    print('')



def search(searchterm):
    print('')
    line = (comm.findLineInFile(MACS, searchterm))
    print('    ->  ' + str(line))
    maca = str(line).strip('\'b')[:8]
    macrnd = ("%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    maca += ':' + macrnd
    print('    ->  ' + maca + '  <-- Random ending')
    print('')


def show():
    print('')
    with open(MACS, 'r') as file:
        for line in file:
            print('    ->  ' + line.strip('\n'))
    print('')


def rnd():
    rnd = None
    rnd = ("%02x:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    print('\n\t->  ' + str(rnd) + '\n')


def info():
    print("""
        Module for use in WMDframe.

        Changing MAC address""")

    if parser.format_help():
        print('\n\t' + bc.OKBLUE + 'COMMANDLINE ARGUMENTS:' + bc.ENDC)
        for line in parser.format_help().strip().splitlines():
            print('\t' + line)
    print('')


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'macchange:' + bc.ENDC + ' ')
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'info' in userinput[:1]:
        info()
    elif 'show' in userinput[:1]:
        show()
    elif 'search' in userinput[:1]:
        searchterm = str(userinput[1:2]).strip('[]\'')
        search(searchterm)
    elif 'rnd' in userinput[:1]:
        rnd()
    elif 'run' in userinput[:1]:
        run()
    elif 'set' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        uservalue = str(userinput[2:3]).strip('[]\'')  # Use single word after "set parameter"
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
    print('\t    __  ______   ______        __                           ')
    print('\t   /  |/  /   | / ____/  _____/ /_  ____ _____  ____ ____   ')
    print('\t  / /|_/ / /| |/ /      / ___/ __ \/ __ `/ __ \/ __ `/ _ \  ')
    print('\t / /  / / ___ / /___   / /__/ / / / /_/ / / / / /_/ /  __/  ')
    print('\t/_/  /_/_/  |_\____/   \___/_/ /_/\__,_/_/ /_/\__, /\___/   ')
    print('\t                                             /____/         ')
    print('\n')
    if os.getuid() != 0:
        print('r00tness is needed!')
        print('Run the script again as root/sudo')
        return None
    print('')

    if args.mac:
        maca = args.mac
    else:
        maca = comm.getNewMac('')
    if args.interface:
        int = args.interface
    else:
        int = INTERFACE_NET

    global sop
    sop = options(maca, int)
    if args.run:
        run()
    else:
        console()


if args.run:
    main()


# For testing uncomment "main()" and run module with "python3 modulename.py"
# main()
