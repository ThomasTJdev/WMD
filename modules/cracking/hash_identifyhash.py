#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import argparse
import subprocess
from core.colors import bc as bc
import core.modules as cmodules
import core.commands as comm


parser = argparse.ArgumentParser()
parser.add_argument('-hi', '--hashinput', help='Hash to identify', metavar='HASH')  # Example. Use with "args.lanip"
parser.add_argument('-r', '--run', action='store_true', help='Start monitoring.')
args, unknown = parser.parse_known_args()


# START Log files, global variables, etc.
global program

# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Identify hash'
    Call = 'hashid'
    Modulename = 'hash_identifyhash'  # Filename
    Category = 'cracking'
    Type = 'hash'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Identify a hash'
    Datecreation = '01/01/2017'
    Lastmodified = '01/01/2017'

    def __init__(self, hash):
        self.hash = hash
        self.show_all()

    # Possible options. These variables are checked when the user tries to 'set' an option
    def poss_opt(self):
        return ('hash')

    # Show options
    def show_opt(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (9, 'OPTION', 5, 'RQ', 20, 'DESCRIPTION', 'VALUE')) + bc.ENDC
            + '\n\t' + ('%-*s %-*s %-*s %s' % (9, '------', 5, '--', 20, '-----------', '-----'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (9, 'hash:', 5, 'y', 20, 'Hash to identify', self.hash))
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s ->\t%s' % (9, 'run', 'Run the script'))
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
    print('')
    call = program + ' -e -j -m ' + sop.hash
    out = subprocess.check_output(call, shell=True)
    out = out.decode()
    out = out.strip().splitlines()
    for line in out:
        print('\t     -> ' + line)
    print('')


def info():
    print("""
        Module for use in WMDframe. Identify a hash.
        The result will be in this format:
          -> HASH [Hashcat Mode][John the Ripper format]
        MD5 example:
          -> MD5 [Hashcat Mode: 0][JtR Format: raw-md5]""")

    if parser.format_help():
        print('\n\t' + bc.OKBLUE + 'COMMANDLINE ARGUMENTS:' + bc.ENDC)
        for line in parser.format_help().strip().splitlines():
            print('\t' + line)
    print('')


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'hashid:' + bc.ENDC + ' ')
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'info' in userinput[:1]:
        info()
    elif 'run' in userinput[:1]:
        run()
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
    print('\t    __               __    ________   ')
    print('\t   / /_  ____  _____/ /_  /  _/ __ \  ')
    print('\t  / __ \/ __ `/ ___/ __ \ / // / / /  ')
    print('\t / / / / /_/ (__  ) / / // // /_/ /   ')
    print('\t/_/ /_/\__,_/____/_/ /_/___/_____/    ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    global program
    program = comm.checkInstalledFull('hashid', 'hashID', 'hashid.py')
    global sop
    # The parameters to be passed to the module on init
    if args.hashinput:
        hash = args.hashinput
    else:
        hash = ''
    sop = options(hash)
    if args.run:
        run()
    else:
        console()


if args.run:
    main()


# For testing uncomment "main()" and run module with "python3 modulename.py"
# main()
