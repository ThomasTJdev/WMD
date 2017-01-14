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
global routersploit
ROUTERSPLOIT_SYM = (config['TOOLS']['ROUTERSPLOIT_SYM'])
ROUTERSPLOIT_GITNAME = (config['TOOLS']['ROUTERSPLOIT_GITNAME'])
ROUTERSPLOIT_GITRUN = (config['TOOLS']['ROUTERSPLOIT_GITRUN'])
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Routersploit'
    Call = 'rsploit'
    Modulename = 'gitroutersploit'
    Category = 'router'
    Type = 'framework'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Framework for routers with exploits and getting creds. (Arthur: Reverse Shell Security)'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    def __init__(self):
        self.show_all()

    # Show options
    def show_opt(self):
        print('\n\t' + bc.OKBLUE + 'OPTIONS (only available after the command "run")' + bc.ENDC)
        print(
            ''
            + bc.BOLD + '\tAutopwn router:' + bc.ENDC
            + '\n\t  - use scanners/autopwn'
            + '\n\t  - show options'
            + '\n\t  - set target 192.168.1.1'
            + '\n\t  - run'
            + '\n\t  - use exploit/routerexploitname'
            + '\n\t  - show options'
            + '\n\t  - set target 192.168.1.1'
            + '\n\t  - check'
            + '\n\t  - run'
            + '\n\n'
            + bc.BOLD + '\n\tCreds:' + bc.ENDC
            + '\n\t  - use creds/ftp_default (ftp_bruteforce, ssh, telnet, http basic auth, http form auth, snmp)'
            + '\n\t  - show options'
            + '\n\t  - set target 192.168.1.1'
            + '\n\t  - run'
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s ->\t%s' % (17, 'run', 'Run the script'))
            + '\n\t' + ('%-*s ->\t%s' % (17, 'lsexp', 'Show main folders for exploits'))
            + '\n\t' + ('%-*s ->\t%s' % (17, 'lsexpsin {input}', 'Show exploits in folder'))
            + '\n\t' + ('%-*s ->\t%s' % (17, 'lscreds', 'Show modules for use creds/{input}'))
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
    os.system('python2 ' + routersploit)


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'exploitdb:' + bc.ENDC + ' ')
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'run' in userinput[:1]:
        run()
    elif 'lsexp' in userinput[:1]:
        print('')
        os.system('ls tools/routersploit/routersploit/modules/exploits')
        print('')
    elif 'lsexpsin' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        print('')
        os.system('ls tools/routersploit/routersploit/modules/exploits/' + useroption)
        print('')
    elif 'lscreds' in userinput[:1]:
        print('')
        os.system('ls tools/routersploit/routersploit/modules/creds')
        print('')
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
    print('      ____             __      _ __   ')
    print('     / __ \_________  / /___  (_) /_  ')
    print('    / /_/ / ___/ __ \/ / __ \/ / __/  ')
    print('   / _, _(__  ) /_/ / / /_/ / / /_    ')
    print('  /_/ |_/____/ .___/_/\____/_/\__/    ')
    print('            /_/                       ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkInstalled('python2')
    global routersploit
    routersploit = comm.checkInstalledFull(ROUTERSPLOIT_SYM, ROUTERSPLOIT_GITNAME, ROUTERSPLOIT_GITRUN)
    print('')
    global sop
    sop = options()
    console()
