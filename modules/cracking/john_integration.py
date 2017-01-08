#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import argparse
import os
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
parser.add_argument('-i', '--input', help='Path to file with hash', metavar='PATH.txt')
parser.add_argument('-p', '--pwdlist', help='Path to pwdlist', metavar='PATH.txt')
parser.add_argument('-f', '--format', help='Format to use', metavar='E.g. Raw-MD5')
parser.add_argument('-a', '--args', help='Arguments to use', metavar='E.g. Raw-MD5')
parser.add_argument('-r', '--run', action='store_true', help='Start monitoring.')
args, unknown = parser.parse_known_args()

config = core.config()
global john
JOHN_SYM = (config['TOOLS']['JOHN_SYM'])
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'ThomasTJ (TTJ)'
    Name = 'John the Ripper'
    Call = 'john'
    Modulename = 'john_integration'
    Category = 'cracking'
    Type = 'sin'
    Version = '0.0.1'
    License = 'MIT'
    Description = 'Python console for John the Ripper'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    # Init
    def __init__(self, pwdFile, pwdList, hashFormat, args):
        self.file = pwdFile
        self.list = pwdList
        self.format = hashFormat
        self.args = args
        self.show_all()

    # Possible options
    def poss_opt(self):
        return ('file', 'list', 'format', 'args')

    # Show options
    def show_opt(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (12, 'OPTION', 6, 'RQ', 14, 'VALUE', 'DESCRIPTION')) + bc.ENDC
            + '\n\t' + ('%-*s %-*s %-*s %s' % (12, '------', 6, '--', 14, '-----', '-----------'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (12, 'file:', 6, 'y', 14, self.file, 'File containing hash'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (12, 'list:', 6, 'y', 14, self.list, 'Passwordlist'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (12, 'format:', 6, 'n', 14, self.format, 'Hashformat'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (12, 'args:', 6, 'n', 14, self.args, 'Userdefined args'))
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s -> %s' % (6, 'run', 'Run the script'))
            + '\n\t' + ('%-*s -> %s' % (6, 'show', 'Show cracked pwd\'s'))
            + '\n\t' + ('%-*s -> %s' % (6, 'info', 'Information'))
            + '\n\t' + ('%-*s -> %s' % (6, 'so', 'Show options'))
            + '\n\t' + ('%-*s -> %s' % (6, 'sa', 'Show module info'))
            + '\n\t' + ('%-*s -> %s' % (6, 'exit', 'Exit'))
            + '\n'
            )

    # Show all data
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
    if not sop.args:
        os.system(john + ' --wordlist=' + sop.list + ' --format=' + sop.format + ' ' + sop.file)
    else:
        os.system(john + ' --wordlist=' + sop.list + ' --format=' + sop.format + ' ' + sop.file + ' ' + sop.args)
    print('')


def show():
    print('')
    os.system(john + ' --format=' + sop.format + ' --show ' + sop.file)
    print('')


def info():
    print("""
        Integration of John the Ripper in WMDframe.""")

    if parser.format_help():
        print('\n\t' + bc.OKBLUE + 'COMMANDLINE ARGUMENTS:' + bc.ENDC)
        for line in parser.format_help().strip().splitlines():
            print('\t' + line)
    print('')


# CONSOLE
def console():
    value = input("   -> " + bc.FAIL + "wmd" + bc.ENDC + "@" + bc.FAIL + "john:" + bc.ENDC + " ")
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'info' in userinput[:1]:
        info()
    elif 'run' in userinput[:1]:
        run()
    elif 'show' in userinput[:1]:
        show()
    elif 'set' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        uservalue = str(userinput[2:3]).strip('[]\'')
        if useroption not in sop.poss_opt():
            print(bc.WARN + "\n    Error, no options for: " + useroption + "\n" + bc.ENDC)
        elif useroption in sop.poss_opt():
            setattr(sop, useroption, uservalue)
            print('\n    ' + useroption + '\t> ' + uservalue + "\n")
    elif 'back' in userinput[:1] or 'exit' in userinput[:1]:
        return None
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + "\n    Error, no options for: " + command + "\n" + bc.ENDC)
    console()
# END CONSOLE


# STARTER
def main():
    print('\n')
    print('         __      __        ________         ____  _                        ')
    print('        / /___  / /_  ____/_  __/ /_  ___  / __ \(_)___  ____  ___  _____  ')
    print('   __  / / __ \/ __ \/ __ \/ / / __ \/ _ \/ /_/ / / __ \/ __ \/ _ \/ ___/  ')
    print('  / /_/ / /_/ / / / / / / / / / / / /  __/ _, _/ / /_/ / /_/ /  __/ /      ')
    print('  \____/\____/_/ /_/_/ /_/_/ /_/ /_/\___/_/ |_/_/ .___/ .___/\___/_/       ')
    print('                                               /_/   /_/                   ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkInstalled(JOHN_SYM)
    global john
    john = JOHN_SYM
    print('')
    global sop
    # The parameters to be passed to the module on init
    if args.input:
        input = args.input
    else:
        input = ''
    if args.pwdlist:
        pwdlist = args.pwdlist
    else:
        pwdlist = ''
    if args.format:
        input = args.format
    else:
        format = ''
    if args.args:
        arguments = args.args
    else:
        arguments = ''
    sop = options(input, pwdlist, format, arguments)
    if args.run:
        run()
    else:
        console()


if args.run:
    main()


# For testing uncomment "main()" and run module with "python3 modulename.py"
main()
