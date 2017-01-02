#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import configparser
import os
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


config = configparser.ConfigParser()
config.read('core/config.ini')


# START Log files, global variables, etc.
configfile = 'core/config.ini'
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Change settings'
    Call = 'settings'
    Modulename = 'env_settings'  # Filename
    Category = 'other'
    Type = 'settings'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Change your environment settings, e.g. interface'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    def __init__(self):
        self.show_all()

    # Show options
    def show_opt(self):
        print(
            ''
            + '\t' + bc.OKBLUE + ('CONFIGFILE - TAKE CARE:') + bc.ENDC
            + '\n\t' + ('-------------------------------')
            + '\n\t' + ('%-*s ->\t%s' % (16, 'set "old" "new"', 'Change setting. E.g. set "INTERFACE_NET = eno1" "INTERFACE_NET = wlan0"'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'see [section]', 'See the options for section, e.g. "see network"'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'seeall', 'See data in configfile'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'sections', 'List all sections'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'so', 'Show options'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'sa', 'Show module info'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'invoke', 'Invoke module'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'exit', 'Exit'))
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print('')

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


def set(uservalue):
    print('')
    try:
        input = [line for line in [line.strip() for line in uservalue.split('\"')] if line]
        if not input[0] or not input[1]:
            print('\t[!]  There\'s an error in your input. Inclose both old and new line in double qoutes.')
        if '[' in input[0] or 'AUTHOR' in input[0]:
            print('\t[!]  There\'s an error in your input. Dont change sections!')
        changes = comm.changeLineInFile(configfile, input[0], input[1])
        print(bc.OKGREEN + '\t[+]  Changing: ' + str(changes))
        print(bc.OKGREEN + '\t[+]  To      : ' + str(input[1]) + '\n')
    except:
        print(bc.FAIL + '\t[!]  There\'s an error in your input.\n' + bc.ENDC)


def see(section):
    print('')
    head = section.upper()
    doit = False
    with open(configfile, 'r') as file:
        for f in file.readlines():
            if f.startswith('[' + head + ']'):
                print('\t' + bc.OKBLUE + '[' + head + ']' + bc.ENDC)
                doit = True
                continue
            if f.startswith('[') and not f.startswith(head):
                doit = False

            if doit:
                if f.startswith('# '):
                    colorLine = bc.ENDC + bc.BOLD
                elif f.startswith('#'):
                    colorLine = bc.HEADER
                else:
                    colorLine = bc.OKGREEN
                print(colorLine + '\t' + f.strip('\n') + bc.ENDC)
    print('')


def seeall():
    print('')
    doit = False
    with open(configfile, 'r') as file:
        for f in file.readlines():
            if f.startswith('['):
                print('\t' + bc.OKBLUE + f + bc.ENDC)
                doit = True
                continue
            if doit:
                if f.startswith('# '):
                    colorLine = bc.ENDC + bc.BOLD
                elif f.startswith('#'):
                    colorLine = bc.HEADER
                else:
                    colorLine = bc.OKGREEN
                print(colorLine + '\t' + f.strip('\n') + bc.ENDC)
    print('')


def sections():
    print('')
    doit = False
    with open(configfile, 'r') as file:
        for f in file.readlines():
            if f.startswith('[') and not f.startswith('[FRAMEWORK]'):
                doit = True
            else:
                doit = False
            if doit:
                print(bc.ENDC + bc.BOLD + '\t' + f.strip('\n'))
    print('' + bc.ENDC)


def info():
    print("""
        Module for use in WMDframe.""")


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'settings:' + bc.ENDC + ' ')
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'info' in userinput[:1]:
        info()
    elif 'set' in userinput[:1]:
        uservalue = value.split(' ', 1)[1]
        set(uservalue)
    elif 'see' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        see(useroption)
    elif 'seeall' in userinput[:1]:
        seeall()
    elif 'sections' in userinput[:1]:
        sections()
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
    print('     _____      __  __  _                   ')
    print('    / ___/___  / /_/ /_(_)___  ____ ______  ')
    print('    \__ \/ _ \/ __/ __/ / __ \/ __ `/ ___/  ')
    print('   ___/ /  __/ /_/ /_/ / / / / /_/ (__  )   ')
    print('  /____/\___/\__/\__/_/_/ /_/\__, /____/    ')
    print('                            /____/          ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    if os.getuid() != 0:
        print(bc.WARN + '\t[-]  Only a warning - you are not running as root. You\'ll might encounter problems with user priviliges' + bc.ENDC)
    else:
        print(bc.OKGREEN + '\t[+]  You are running as root. No user priviliges problems')
    print('')
    global sop
    # The parameters to be passed to the module on init
    sop = options()
    console()


# For testing uncomment "main()" and run module with "python3 modulename.py"
# main()
