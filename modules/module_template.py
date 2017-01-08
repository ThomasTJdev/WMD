#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import argparse
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


# Parser
parser = argparse.ArgumentParser()
# parser.add_argument('-ip', '--lanip', help='IP to monitor', metavar='IP') # Example. Use with "args.lanip"
parser.add_argument('-r', '--run', action='store_true', help='Start monitoring')
args, unknown = parser.parse_known_args()

# Core
config = core.config()
logger = core.log()


# START Log files, global variables, etc.

# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Template module'
    Call = 'tempmod'
    Modulename = 'templatemodule'  # Filename
    Category = 'cracktheWWW'
    Type = 'sin'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Showing structure of modules'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    def __init__(self, req_var1, req_var2):
        self.req_var1 = req_var1
        self.req_var2 = req_var2
        self.show_all()

    # Possible options. These variables are checked when the user tries to 'set' an option
    def poss_opt(self):
        return ('req_var1', 'req_var2')

    # Show options
    def show_opt(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 8, 'RQ', 18, 'VALUE', 'DESCRIPTION')) + bc.ENDC
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 8, '--', 18, '-----', '-----------'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'req_var1:', 8, 'y', 18, self.req_var1, 'Setting1'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'req_var2:', 8, 'n', 18, self.req_var2, 'Setting2'))
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s ->\t%s' % (9, 'run', 'Run the script'))
            # + '\n\t' + ('%-*s ->\t%s' % (9, 'custom', 'Custom extra function'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'runcom', 'Run program with specific arguments <runcom [args]>'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'info', 'Information'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'help', 'Help'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'pd', 'Predefined arguments for "runcom"'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'so', 'Show options'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'sa', 'Show module info'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'set', 'Set options, set [PARAMETER] [VALUE]'))
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
    print('\tRunning running')


def runcom(arguments):
    print('\tRunning special with arguments')
    print(arguments)


def predefinedCommands():
    print(
        ''
        + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
        + '\n\t' + '---------'
    )
    print("""         -> Super args                    = -T4 -A -v
         -> Super duber           = -sS -sU -T4 -A -v
         -> Better args           = -p 1-65535 -T4 -A -v
    """)
    print(
        '\t' + bc.ITALIC + 'Use \'runcom\' followed by arguments' + bc.ENDC
        + '\n'
    )


def info():
    print("""
        Module for use in WMDframe.""")

    if parser.format_help():
        print('\n\t' + bc.OKBLUE + 'COMMANDLINE ARGUMENTS:' + bc.ENDC)
        for line in parser.format_help().strip().splitlines():
            print('\t' + line)
    print('')


def helpMe():
    pass


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'tmpmod:' + bc.ENDC + ' ')
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'help' in userinput[:1]:
        helpMe()
    elif 'info' in userinput[:1]:
        info()
    elif 'pd' in userinput[:1]:
        predefinedCommands()
    elif 'run' in userinput[:1]:
        run()
    elif 'runcom' in userinput[:1]:
        runcom(str(userinput[1:]).strip('[]\''))
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
    print('    ______                   __  ___          __      __     ')
    print('   /_  __/___ ___  ____     /  |/  /___  ____/ /_  __/ /__   ')
    print('    / / / __ `__ \/ __ \   / /|_/ / __ \/ __  / / / / / _ \  ')
    print('   / / / / / / / / /_/ /  / /  / / /_/ / /_/ / /_/ / /  __/  ')
    print('  /_/ /_/ /_/ /_/ .___/  /_/  /_/\____/\__,_/\__,_/_/\___/   ')
    print('               /_/                                           ')
    print('\n')
    # if os.getuid() != 0:
    #    print('r00tness is needed due to XXX!')
    #    print('Run the script again as root/sudo')
    #    return None
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    # comm.checkInstalled('nmap')
    # program = comm.checkInstalledFull('hashid', 'hashID', 'hashid.py')  # symlink, gitFolderName, fileToRun
    global sop
    # The parameters to be passed to the module on init
    sop = options('FIRST', 'SECOND')
    if args.run:
        run()
    else:
        console()


if args.run:
    main()


# For testing uncomment "main()" and run module with "python3 modulename.py"
# main()
