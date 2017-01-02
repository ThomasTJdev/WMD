#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import configparser
import os
try:
    import core.core as core
    import core.modules as cmodules
    import core.commands as comm
    from core.colors import bc as bc
except:
    import sys
    sys.path.append('././')
    import core.core as core
    import core.modules as cmodules
    import core.commands as comm
    from core.colors import bc as bc


# Core
config = core.config()
logger = core.log()


# START Log files, global variables, etc.
EDITOR = (config['ENVIRONMENT']['EDITOR'])
INSTABOT_SYM = (config['TOOLS']['INSTABOT_SYM'])
INSTABOT_GITNAME = (config['TOOLS']['INSTABOT_GITNAME'])
INSTABOT_GITRUN = (config['TOOLS']['INSTABOT_GITRUN'])
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Instagram bot'
    Call = 'instabot'
    Modulename = 'se_instabot'  # Filename
    Category = 'socialeng'
    Type = 'instagram'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Instagram bot for performing various activities (Arthur: LevPasha)'
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
            + '\n\t' + ('%-*s ->\t%s' % (16, 'run', 'Run in new xterm'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'set "old" "new"', 'Change setting. E.g. set "follow_per_day=300" "follow_per_day=400"'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'edit', 'Edit file with local editor'))
            + '\n\t' + ('%-*s ->\t%s' % (16, 'see', 'See the options for section, e.g. "see network"'))
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


def run():
    print('')
    try:
        comm.runCommand(('python3 ' + INSTABOT_GITRUN), 'INSTABOT')
        print(bc.OKGREEN + '\t[+]  Running instabot in new xterm\n' + bc.ENDC)
    except:
        print(bc.FAIL + '\t[!]  There\'s an error in your input.\n' + bc.ENDC)


def set(uservalue):
    print('')
    try:
        input = [line for line in [line.strip() for line in uservalue.split('\"')] if line]
        if not input[0] or not input[1]:
            print('\t[!]  There\'s an error in your input. Inclose both old and new line in double qoutes.')
        changes = comm.changeLineInFile(configfile, input[0], input[1])
        print(bc.OKGREEN + '\t[+]  Changing: ' + str(changes))
        print(bc.OKGREEN + '\t[+]  To      : ' + str(input[1]) + '\n')
    except:
        print(bc.FAIL + '\t[!]  There\'s an error in your input.\n' + bc.ENDC)


def edit():
    print('')
    try:
        os.system(EDITOR + ' ' + INSTABOT_GITRUN)
    except:
        print(bc.FAIL + '\t[!]  There\'s an error in your input.\n' + bc.ENDC)


def see():
    print('')
    doit = False
    with open(INSTABOT_GITRUN, 'r') as file:
        for f in file.readlines():
            if f.startswith('bot = InstaBot'):
                doit = True
            if f.startswith('while True:'):
                doit = False

            if doit:
                if f.strip(' ').startswith('#'):
                    colorLine = bc.HEADER
                else:
                    colorLine = bc.OKGREEN
                print(colorLine + '\t' + f.strip('\n') + bc.ENDC)
    print('')


def info():
    print("""
        Module for use in WMDframe.

        Checkout the git: https://github.com/LevPasha/instabot.py""")


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
    elif 'run' in userinput[:1]:
        run()
    elif 'set' in userinput[:1]:
        uservalue = value.split(' ', 1)[1]
        set(uservalue)
    elif 'edit' in userinput[:1]:
        edit()
    elif 'see' in userinput[:1]:
        see()
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
    print('\t    ____           __        __          __   ')
    print('\t   /  _/___  _____/ /_____ _/ /_  ____  / /_  ')
    print('\t   / // __ \/ ___/ __/ __ `/ __ \/ __ \/ __/  ')
    print('\t _/ // / / (__  ) /_/ /_/ / /_/ / /_/ / /_    ')
    print('\t/___/_/ /_/____/\__/\__,_/_.___/\____/\__/    ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkInstalledFull(INSTABOT_SYM, INSTABOT_GITNAME, INSTABOT_GITRUN)
    comm.checkNetConnectionV()
    print('')
    global sop
    # The parameters to be passed to the module on init
    sop = options()
    console()


# For testing uncomment "main()" and run module with "python3 modulename.py"
# main()
