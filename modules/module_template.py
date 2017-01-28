#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#
# Module for WMDframe
# This modules is used for XXX
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
parser = argparse.ArgumentParser(description='', prog='modulename.py')
# parser.add_argument('-ip', '--lanip', help='IP to monitor', metavar='IP')  # Required parameter when metavar is specified.
parser.add_argument('-r', '--run', action='store_true', help='Run')
args, unknown = parser.parse_known_args()
# ==========================
# Parser END
# ==========================


# ==========================
# Core START
# ==========================
config = core.config()
# INTERFACE_NET = (config['NETWORK']['INTERFACE_NET'])

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
    Name = 'Template module'
    Call = 'tempmod'
    Modulename = 'templatemodule'  # Filename
    Category = 'cracktheWWW'
    Type = 'sha512'
    Version = '0.1'
    License = 'MIT'
    Description = 'Showing structure of modules'
    Datecreation = '2017/02/01'
    Lastmodified = '2017/02/01'

    def __init__(self, req_var1, req_var2):
        """Define variables and show options on run."""
        self.req_var1 = req_var1
        self.req_var2 = req_var2
        self.show_all()

    def poss_opt(self):
        """Possible options. These variables are checked when the user tries to 'set' an option."""
        return ('req_var1', 'req_var2')

    def show_opt(self):
        """Show the possible options."""
        print(
            ''
            '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 8, 'RQ', 18, 'VALUE', 'DESCRIPTION')) + bc.ENDC +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 8, '--', 18, '-----', '-----------')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'req_var1:', 8, 'y', 18, self.req_var1, 'Setting1')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'req_var2:', 8, 'n', 18, self.req_var2, 'Setting2')) +
            '\n'
        )

    def show_commands(self):
        """Show the possible commands."""
        print(
            ''
            '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC +
            '\n\t' + '---------' +
            '\n\t' + ('%-*s ->\t%s' % (9, 'run', 'Run the script')) +
            # '\n\t' + ('%-*s ->\t%s' % (9, 'custom', 'Custom extra function')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'runcom', 'Run program with specific arguments <runcom [ARGS]>')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'info', 'Information')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'help', 'Help')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'pd', 'Predefined arguments for "runcom"')) +
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


# OPTIONAL
def runcom(arguments):
    """The run function with special arguments - optional."""
    print('\tRunning special with arguments')
    print(arguments)


# OPTIONAL
def predefinedCommands():
    """Show predifined commands - optional."""
    print(
        '' +
        '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC +
        '\n\t' + '---------'
    )

    print("""
         -> Super args            = -T4 -A -v
         -> Super duber           = -sS -sU -T4 -A -v
         -> Better args           = -p 1-65535 -T4 -A -v
    """)

    print(
        '\t' + bc.ITALIC + 'Use \'runcom\' followed by arguments' + bc.ENDC +
        '\n'
    )


# OPTIONAL
def info():
    """Show the modules info - optional."""
    print("""
        Module for use in WMDframe.
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
    pass


# CONSOLE
def console():
    """The main console for the module."""
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'tmpmod:' + bc.ENDC + ' ')
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
    # Show predefined commands
    elif 'pd' in userinput[:1]:
        predefinedCommands()
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
    print('\t  ______                   __  ___          __      __     ')
    print('\t /_  __/___ ___  ____     /  |/  /___  ____/ /_  __/ /__   ')
    print('\t  / / / __ `__ \/ __ \   / /|_/ / __ \/ __  / / / / / _ \  ')
    print('\t / / / / / / / / /_/ /  / /  / / /_/ / /_/ / /_/ / /  __/  ')
    print('\t/_/ /_/ /_/ /_/ .___/  /_/  /_/\____/\__,_/\__,_/_/\___/   ')
    print('\t             /_/                                           ')
    print('\n')
    # If module require root:
    # if os.getuid() != 0:
    #     print('r00tness is needed due to XXX!')
    #     print('Run the script again as root/sudo')
    #     return None
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    # comm.checkNetConnectionV()
    # print('')
    global sop
    # The parameters to be passed to the module on run
    sop = Options('FIRST', 'SECOND')
    if args.run:
        run()
    else:
        console()


if args.run:
    main()


# For testing uncomment "main()", place module in root directory and run module with "python3 modulename.py"
# main()
