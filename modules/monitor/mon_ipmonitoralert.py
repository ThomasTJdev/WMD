#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import argparse
import difflib
import os
import re
import subprocess
from datetime import datetime
from time import sleep
from core.colors import bc as bc
import core.modules as cmodules
import core.commands as comm


parser = argparse.ArgumentParser()
parser.add_argument('-ip', '--lanip', help='IP\'s to monitor', metavar='IP')
parser.add_argument('-ig', '--ignore', help='IP\'s to ignore', metavar='IP')
parser.add_argument('-r', '--run', action='store_true', help='Start monitoring.')
args, unknown = parser.parse_known_args()


# START Log files, global variables, etc.


# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'IP monitor alert'
    Call = 'ipmon'
    Modulename = 'mon_ipmonitoralert'
    Category = 'monitor'
    Type = 'ip'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Monitor IP\'s and alert for changes'
    Datecreation = '01/01/2017'
    Lastmodified = '01/01/2017'

    def __init__(self, lanIP, time, ignore):
        self.lanIP = lanIP
        self.time = time
        self.ignore = ignore
        self.show_all()

    # Possible options. These variables are checked when the user tries to 'set' an option
    def poss_opt(self):
        return ('lanIP', 'time', 'ignore')

    # Show options
    def show_opt(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 8, 'RQ', 18, 'VALUE', 'DESCRIPTION')) + bc.ENDC
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 8, '--', 18, '-----', '-----------'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'lanIP:', 8, 'y', 18, self.lanIP, 'Network IP\'s to monitor (e.g. 192.168.1.0/24)'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'time:', 8, 'n', 18, self.time, 'Loop time. Check lan IP\'s every nth second'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'ignore:', 8, 'n', 18, self.ignore, 'Ignore IP\'s. (e.g. <host1>,<host2>)'))
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s ->\t%s' % (9, 'run', 'Run the script'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'hosts', 'Check lan IP\'s'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'info', 'Information'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'so', 'Show options'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'sa', 'Show module info'))
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
    hosts_old = ''
    counter = 0
    if sop.ignore:
        ignore = ' --exclude ' + sop.ignore + ' '
    else:
        ignore = ''
    # If user is not sudo/root - less information is available
    if os.getuid() != 0:
        print('\t[!]  You are running as a normal user. Less information will be available.')
    print('\n\t[*]  Monitoring started:')
    while True:
        out = ''
        counter += 1
        hosts_now = ''
        call = 'nmap -T5 -sP ' + ignore + sop.lanIP
        hosts = subprocess.check_output(call, shell=True)
        hosts = hosts.decode()
        hosts_now = hosts.strip().splitlines()

        for line in difflib.unified_diff(hosts_old, hosts_now, fromfile='', tofile='', fromfiledate='', tofiledate='', n=0, lineterm=''):
            for prefix in ('---', '+++', '@@', 'Host is up', 'Starting Nmap', 'Nmap done'):
                if prefix in line:
                    break
            else:
                # Normal user
                if os.getuid() != 0:
                    if line.startswith('+'):
                        print(bc.OKGREEN + '\t     -> ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '  ' + line + bc.ENDC)
                    if line.startswith('-'):
                        print(bc.WARN + '\t     -> ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '  ' + line + bc.ENDC)
                # Sudo/root user
                else:
                    if 'MAC Address' not in line:
                        out += '\n'
                    else:
                        out += ' ' + line.replace('MAC Address:', '')
                    if line.startswith('+Nmap'):
                        out += (bc.OKGREEN + '\t     -> ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '  ' + ('%-*s' % (40, line.replace('Nmap scan report for', ''))) + bc.ENDC)
                    if line.startswith('-Nmap'):
                        out += (bc.WARN + '\t     -> ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '  ' + ('%-*s' % (40, line.replace('Nmap scan report for', ''))) + bc.ENDC)
        if os.getuid() == 0 and out:
            print(out)
        hosts_old = hosts_now

        if counter % 30 == 0 and counter != 0:
            print('\t[*]  ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '  I\'m still alive. Just finished ' + str(counter) + ' checks.')

        sleep(int(sop.time))


def hosts():
    if sop.ignore:
        ignore = ' --exclude ' + sop.ignore + ' '
    else:
        ignore = ''
    print('')
    print('\t[*]  Please while scanning ' + sop.lanIP + '\n')
    call = 'nmap -T5 -sP ' + ignore + sop.lanIP
    arptable = subprocess.check_output(call, shell=True)
    arptable = arptable.decode()
    arptable = arptable.strip().splitlines()
    out = ''
    ips = ''
    for line in arptable:
        for prefix in ('---', '+++', '@@', 'Host is up', 'Starting Nmap', 'Nmap done'):
            if prefix in line:
                break
        else:
            if os.getuid() != 0:
                print('\t     -> ' + line)
            else:
                if 'MAC Address' not in line:
                    out += '\n'
                else:
                    out += ' ' + line.replace('MAC Address:', '')
                if 'Nmap scan report for' in line:
                    out += (bc.OKGREEN + '\t     -> ' + '  ' + ('%-*s' % (40, line.replace('Nmap scan report for', ''))) + bc.ENDC)
                    ips += re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line).group() + ','
    if os.getuid() == 0:
        print(out)
    print('\n\tWant to ignore known IP\'s? Then set ignore parameter with the following line:')
    print('\t-> ' + ips[:-1])
    print('')


def info():
    print("""
        This modules ping scans the target IP\'s and alerts
        when new IP\'s are identified or existings IP\'s are lost.

        Current online IP\'s can be found with \"hosts\"

        Please be aware, that an attacker can change MAC address and
        wait for device to go online and then snap the corresponding IP""")

    if parser.format_help():
        print('\n\t' + bc.OKBLUE + 'COMMANDLINE ARGUMENTS:' + bc.ENDC)
        for line in parser.format_help().strip().splitlines():
            print('\t' + line)
    print('')


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'arpmon:' + bc.ENDC + ' ')
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'info' in userinput[:1]:
        info()
    elif 'run' in userinput[:1]:
        run()
    elif 'hosts' in userinput[:1]:
        hosts()
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
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + '\n    Error, no options for: ' + command + '\n' + bc.ENDC)
    console()
# END console


def main():
    print('\n')
    print('      ________                           ')
    print('     /  _/ __ \   ____ ___  ____  ____   ')
    print('     / // /_/ /  / __ `__ \/ __ \/ __ \  ')
    print('   _/ // ____/  / / / / / / /_/ / / / /  ')
    print('  /___/_/      /_/ /_/ /_/\____/_/ /_/   ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkInstalled('arp')
    localIP = comm.getLocalIP('')
    print(bc.OKGREEN + '\t[+]  Local IP: ' + localIP[0] + bc.ENDC)
    print('')
    global sop
    # The parameters to be passed to the module on init
    if args.lanip:
        localIPsubnet = args.lanip
    else:
        localIPsubnet = localIP[0] + '/24'
    if args.ignore:
        ignore = args.ignore
    else:
        ignore = localIP[0]
    sop = options(localIPsubnet, '30', ignore)
    if args.run:
        run()
    else:
        console()


if args.run:
    main()


# For testing uncomment "main()" and run module with "python3 modulename.py"
# main()
