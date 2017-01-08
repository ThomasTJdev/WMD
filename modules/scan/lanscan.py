#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import subprocess
import shlex
import os
import random
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
# Log files
nmap_hostsonline = 'tmp/nmap_hostsonline'
nmap_lanscan_results = 'logs/nmap_lanscan_results'

config = core.config()
global nmap
NMAP_SYM = (config['TOOLS']['NMAP_SYM'])
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = "Thomas TJ (TTJ)"
    Name = 'Lan scan'
    Call = 'lanscan'
    Modulename = "lanscan"
    Category = 'scan'
    Type = 'sin'
    Version = "0.1"
    License = "MIT"
    Description = "Scan local net - recon"
    Datecreation = "04/12/2016"
    Lastmodified = "04/12/2016"

    def __init__(self, target, zombie, decoy, timing):
        self.target = target
        self.zombie = zombie
        self.decoy = decoy
        self.timing = timing
        self.show_all()

    # Possible options
    def poss_opt(self):
        return ('target', 'zombie', 'decoy', 'timing')

    # Show options
    def show_opt(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + ("%-*s %-*s %-*s %s" % (15, "OPTION", 8, "RQ", 18, "VALUE", "DESCRIPTION")) + bc.ENDC
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "------", 8, "--", 18, "-----", "-----------"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "target:", 8, "y", 18, self.target, 'Target IP(s)'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "zombie:", 8, "n", 18, self.zombie, 'Idle scan, use zombie to go through. [See online hosts, run \'hosts\']'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "decoy:", 8, "n", 18, self.decoy, 'Cloak a scan with decoys. lha (all lan IP), lh5 (5 rnd lan ip), rnd (10 random ip), <decoy,decoy>'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "timing:", 8, "n", 18, self.timing, 'Timing: T0 (paranoid, 5min/pkt), T1, T2, T3, T4, T5 (insane, detected by FW/IPS)'))
            + "\n"
            )

    # Show commands
    def show_commands(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + "COMMANDS:" + bc.ENDC
            + "\n\t" + "---------"
            + "\n\t" + ("%-*s ->\t%s" % (9, "run", "Run the script"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "hosts", "Check live hosts with ping"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "runcom", "Run program with specific arguments <runcom [args]>"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "info", "Information"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "help", "Help"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "pd", "Predefined arguments for 'runcom'"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "so", "Show options"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "sa", "Show module info"))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'invoke', 'Invoke module'))
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


def pingScan():
    # Online hosts
    local_ip = comm.getLocalIP('')
    lanNet = local_ip[0] + '/24'
    call = (nmap + ' -sn -oG ' + nmap_hostsonline + ' ' + lanNet)
    args = shlex.split(call)
    return subprocess.check_output(args)


def printHosts():
    # Print online hosts
    interface = comm.getInterfaces()
    localip = comm.getLocalIP(interface)
    hosts = ''
    counter = 0
    print(bc.OKBLUE + '\tID   HOST\t\tNAME' + bc.ENDC)
    print(bc.OKBLUE + '\t---  ----\t\t----' + bc.ENDC)
    with open(nmap_hostsonline, 'rb') as file:
        for line in file:
            host = str(line.split()[1]).strip('()b\'').replace('Nmap', '')
            host2 = str(line.split()[2]).strip('()b\'').replace('Nmap', '')
            if host == localip[0]:
                counter += 1
                hosts += host + ','
                print(bc.FAIL + '\t' + '[' + str(counter) + ']  ' + host + '\t' + host2 + bc.ENDC)
            elif host:
                counter += 1
                hosts += host + ','
                print('\t' + '[' + str(counter) + ']  ' + host + '\t' + host2)
    hosts = hosts[:-1]
    filename = 'tmp/onlinehosts'
    if not os.path.isfile(filename):
        os.mknod(filename)
    with open(filename, 'w') as file:
        file.write(hosts)


def hostsLive():
    print('')
    pingScan()
    printHosts()
    print('')


def run():
    call_opt = ''
    if sop.zombie:
        call_opt = ' -Pn -sI ' + sop.zombie
    else:
        call_opt = ' -Pn '
    if sop.decoy:
        if sop.decoy == 'lh5':
            with open('tmp/onlinehosts', 'r') as file:
                lh = file.read()
                lh = lh.split(',')
            lhNr = ''
            for i in range(0, 5):
                lhNr += random.choice(lh) + ','
            lhNr = lhNr[:-1]
            call_opt += ' -D ' + lhNr
        elif sop.decoy == 'lha':
            with open('tmp/onlinehosts', 'r') as file:
                lh = file.read()
            call_opt += ' -D ' + lh
        elif sop.decoy == 'rnd':
            call_opt += ' -D RND:10'
        else:
            call_opt += ' -D ' + sop.decoy
    if sop.timing:
        call_opt += ' -' + sop.timing
    # Add scripts
    # --spoof-mac 0
    #
    call = (nmap + ' --randomize-hosts -g 53 -oG ' + nmap_lanscan_results + call_opt + ' ' + sop.target)
    print('\t[*]  Running: \n\t  -> ' + call)
    os.system(call)
    print('')


def fullScan():
    # Full scan with ignores
    #call = ('sudo nmap -T1 -v -Pn -sU -PE -PP -g 53 --script 'default or (discovery and safe)'')
    #call = ('nmap --spoof-mac --randomize-hosts --badsum -oG ' + nmap_hostsonline + ' 192.168.1.0/24')
    print(call)
    args = shlex.split(call)
    return subprocess.check_output(args)


def runcom(arguments):
    os.system(nmap + ' ' + arguments)


def predefinedCommands():
    print(
        ''
        + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
        + '\n\t' + '---------'
    )
    print("""         -> Intense scan                    = -T4 -A -v
         -> Intense scan plus UDP           = -sS -sU -T4 -A -v
         -> Intense scan, all TCP ports     = -p 1-65535 -T4 -A -v
         -> Intense scan, no ping           = -T4 -A -v -Pn
         -> Ping scan                       = -sn
         -> Quick scan                      = -T4 -F
         -> Quick scan plus                 = -sV -T4 -O -F --version-light
         -> Quick traceroute                = -sn --traceroute
         -> Slow comprehensive scan         = -sS -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 --script 'default or (discovery and safe)'
    """)
    print(
        '\t' + bc.ITALIC + 'Use \'runcom\' followed by arguments' + bc.ENDC
        + '\n'
    )


def info():
    pass


# CONSOLE
def console():
    value = input("   -> " + bc.FAIL + "wmd" + bc.ENDC + "@" + bc.FAIL + "lanscan:" + bc.ENDC + " ")
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
        try:
            printHosts()
            print('')
        except:
            print(bc.ITALIC + '\tFor viewing online hosts run \'hosts\'\n' + bc.ENDC)
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'help' in userinput[:1]:
        print('\n\n###########################################################')
        print('#  NMAP HELP')
        print('###########################################################\n')
        os.system(nmap + ' -h')
        print('\n\n###########################################################\n\n')
    elif 'info' in userinput[:1]:
        info()
    elif 'pd' in userinput[:1]:
        predefinedCommands()
    elif 'run' in userinput[:1]:
        run()
    elif 'hosts' in userinput[:1]:
        hostsLive()
    elif 'runcom' in userinput[:1]:
        runcom(str(userinput[1:]).strip('[]\''))
    elif 'set' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        uservalue = str(userinput[2:3]).strip('[]\'')
        if useroption not in sop.poss_opt():
            print(bc.WARN + "\n    Error, no options for: " + useroption + "\n" + bc.ENDC)
        elif useroption in sop.poss_opt():
            setattr(sop, useroption, uservalue)
            print('\n      ' + useroption + '\t> ' + uservalue + "\n")
    elif 'invoke' in userinput[:1]:
        comm.invokeModule(options.Call)
        return None
    elif 'back' in userinput[:1] or 'exit' in userinput[:1]:
        filename = 'tmp/onlinehosts'
        if os.path.isfile(filename):
            os.remove('tmp/onlinehosts')
        return None
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + "\n    Error, no options for: " + command + "\n" + bc.ENDC)
    console()
# END console


def main():
    print('\n')
    print('      _   __                            _____                                        _         __  ')
    print('     / | / /____ ___   ____ _ ____     / ___/ _____ ____ _ ____   _____ _____ _____ (_)____   / /_ ')
    print('    /  |/ // __  __ \ / __  // __ \    \__ \ / ___// __  // __ \ / ___// ___// ___// // __ \ / __/ ')
    print('   / /|  // / / / / // /_/ // /_/ /   ___/ // /__ / /_/ // / / /(__  )/ /__ / /   / // /_/ // /_   ')
    print('  /_/ |_//_/ /_/ /_/ \__ _//  ___/   /____/ \___/ \__ _//_/ /_//____/ \___//_/   /_//  ___/ \__/   ')
    print('                          /_/                                                      /_/             ')
    print('\n')
    if os.getuid() != 0:
        print("r00tness is needed due to packet sniffing!")
        print("Run the script again as root/sudo")
        return None
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkInstalled(NMAP_SYM)
    global nmap
    nmap = NMAP_SYM
    local_ip = comm.getLocalIP('')
    lanNet = local_ip[0] + '/24'
    global sop
    sop = options(lanNet, '', 'lh5', 'T2')
    console()
