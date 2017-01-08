#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


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
config = core.config()
global adminfinder
ADMINFINDER_SYM = (config['TOOLS']['ADMINFINDER_SYM'])
ADMINFINDER_GITNAME = (config['TOOLS']['ADMINFINDER_GITNAME'])
ADMINFINDER_GITRUN = (config['TOOLS']['ADMINFINDER_GITRUN'])
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Admin Finder'
    Call = 'adminfinder'
    Modulename = 'gitadminfinder'
    Category = 'bruteforce'
    Type = 'loginpath'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'A Simple script to find admin-paths for webpages. (Arthur: Spaddex)'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    def __init__(self):
        self.show_all()

    # Show options
    def show_opt(self):
        print(
            '\n\tUsing standard path file "admin_locations.txt"'
            + '\n\tFor using the biiig file rename it from "admin_locations_big.txt" to "admin_locations.txt"'
            + '\n\tIt\'s found in tools/Admin_Finder'
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s ->\t%s' % (17, 'run', 'Run the script'))
            + '\n\t' + ('%-*s ->\t%s' % (17, 'so', 'Show options'))
            + '\n\t' + ('%-*s ->\t%s' % (17, 'sa', 'Show module info'))
            + '\n\t' + ('%-*s ->\t%s' % (17, 'invoke', 'Invoke module'))
            + '\n\t' + ('%-*s ->\t%s' % (17, 'exit', 'Exit'))
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
    os.system('python3 ' + adminfinder)


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'adminfinder:' + bc.ENDC + ' ')
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'run' in userinput[:1]:
        run()
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
    print('      _______           __   __            _       ')
    print('     / ____(_)___  ____/ /  / /___  ____ _(_)___   ')
    print('    / /_  / / __ \/ __  /  / / __ \/ __ `/ / __ \  ')
    print('   / __/ / / / / / /_/ /  / / /_/ / /_/ / / / / /  ')
    print('  /_/   /_/_/ /_/\__,_/  /_/\____/\__, /_/_/ /_/   ')
    print('                                 /____/            ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    global adminfinder
    adminfinder = comm.checkInstalledFull(ADMINFINDER_SYM, ADMINFINDER_GITNAME, ADMINFINDER_GITRUN)
    print('')
    global sop
    sop = options()
    console()
