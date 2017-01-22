#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#
# Module for WMDframe
# This modules is a plain interaction with changeme by ztgrace.
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
parser.add_argument('-i', '--ip', help='IP or subnet to scan', metavar='IP')  # Example. Use with "args.lanip"
parser.add_argument('-r', '--run', action='store_true', help='Start monitoring')
args, unknown = parser.parse_known_args()
# ==========================
# Parser END
# ==========================


# ==========================
# Core START
# ==========================
config = core.config()
CHANGEME_SYM = (config['TOOLS']['CHANGEME_SYM'])
CHANGEME_GIT = (config['TOOLS']['CHANGEME_GIT'])
CHANGEME_GITNAME = (config['TOOLS']['CHANGEME_GITNAME'])
CHANGEME_GITRUN = (config['TOOLS']['CHANGEME_GITRUN'])
program = ''
# logger = core.log()
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
    Name = 'Default creds scan'
    Call = 'changeme'
    Modulename = 'creds_changeme'  # Filename
    Category = 'bruteforce'
    Type = 'creds'
    Version = '0.1'
    License = 'MIT'
    Description = 'Scan IP\'s for services and try logging in with default credentials (Arthur: ztgrace)'
    Datecreation = '2017/02/01'
    Lastmodified = '2017/02/01'

    def __init__(self, ip, debug):
        """Define variables and show options on run."""
        self.ip = ip
        self.debug = debug
        self.show_all()

    def poss_opt(self):
        """Possible options. These variables are checked when the user tries to 'set' an option."""
        return ('ip', 'debug')

    def show_opt(self):
        """Show the possible options."""
        print(
            ''
            '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 8, 'RQ', 18, 'VALUE', 'DESCRIPTION')) + bc.ENDC +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 8, '--', 18, '-----', '-----------')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'ip:', 8, 'y', 18, self.ip, 'IP or subnet to scan (192.168.1.100 or 192.168.1.1/24')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'debug:', 8, 'n', 18, self.debug, 'Turn debugging on (y/n)')) +
            '\n'
        )

    def show_commands(self):
        """Show the possible commands."""
        print(
            ''
            '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC +
            '\n\t' + '---------' +
            '\n\t' + ('%-*s ->\t%s' % (9, 'run', 'Run the script')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'runcom', 'Run program with specific arguments <runcom [ARGS]>')) +
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
    print('')

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir('tools/' + CHANGEME_GITNAME)
    if sop.debug.lower() == 'y':
        comm.runCommand('python2 ' + program + ' -s ' + sop.ip + ' -d', 'ChangeMe')
    else:
        comm.runCommand('python2 ' + CHANGEME_GITRUN + ' -s ' + sop.ip, 'ChangeMe')
    os.chdir(dname)


# OPTIONAL
def runcom(arguments):
    """The run function with special arguments - optional."""
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir('tools/' + CHANGEME_GITNAME)
    print('')
    print('\tRunning with: ' + str(arguments))
    comm.runCommand('python2 ' + CHANGEME_GITRUN + ' ' + str(arguments), 'ChangeMe')
    os.chdir(dname)
    print('')


# OPTIONAL
def info():
    """Show the modules info - optional."""
    print("""
        Module for use in WMDframe. Just an interaction with the git
        repo changeme by ztgrace.

        "Getting default credentials added to commercial scanners is
        often difficult and slow. changeme is designed to be simple
        to add new credentials without having to write any code or modules."

        Checkout the git repo: https://github.com/ztgrace/changeme
        """)
    # Delete the parser info, if args.parse is not used.
    if parser.format_help():
        print('\n\t' + bc.OKBLUE + 'COMMANDLINE ARGUMENTS:' + bc.ENDC)
        for line in parser.format_help().strip().splitlines():
            print('\t' + line)
    print('')


# OPTIONAL
def helpMe():
    """Show a help menu - optional."""
    print('')
    os.system('python2 ' + program + ' -h')
    print('')


# CONSOLE
def console():
    """The main console for the module."""
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'changeme:' + bc.ENDC + ' ')
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
    # Show help
    elif 'help' in userinput[:1]:
        helpMe()
    # Run special command from userinput
    elif 'runcom' in userinput[:1]:
        runcom(value.split(' ', 1)[1])
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + '\n    Error, no options for: ' + command + '\n' + bc.ENDC)
    console()
# END console


def main():
    """The first function to run."""
    print('\n')
    print('\t        __                                          ')
    print('\t  _____/ /_  ____ _____  ____ ____  ____ ___  ___   ')
    print('\t / ___/ __ \/ __ `/ __ \/ __ `/ _ \/ __ `__ \/ _ \  ')
    print('\t/ /__/ / / / /_/ / / / / /_/ /  __/ / / / / /  __/  ')
    print('\t\___/_/ /_/\__,_/_/ /_/\__, /\___/_/ /_/ /_/\___/   ')
    print('\t                      /____/                        ')
    print(bc.ITALIC + '\tchangeme by ztgrace')
    print('\trun "info" for git information' + bc.ENDC)
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkInstalled('python2')
    global program
    program = comm.checkInstalledFull(CHANGEME_SYM, CHANGEME_GITNAME, CHANGEME_GITRUN)
    print('')
    global sop
    if args.ip:
        ip = args.ip
    else:
        ip = comm.getLocalIP_interface() + '/24'
    sop = Options(ip, 'n')
    if args.run:
        run()
    else:
        console()


if args.run:
    main()


# For testing uncomment "main()", place module in root directory and run module with "python3 modulename.py"
# main()
