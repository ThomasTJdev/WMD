#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import os
from core.colors import bc as bc
import core.modules as cmodules
import core.commands as comm


# START Log files, global variables, etc.


# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Spoofcheck email domain'
    Call = 'mspoofcheck'
    Modulename = 'spoofcheckemail'
    Category = 'mail'
    Type = 'sin'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Check if a domain can be spoofed for e.g. emailing'
    Datecreation = '01/01/2017'
    Lastmodified = '01/01/2017'

    def __init__(self, domain):
        self.domain = domain
        self.show_all()

    # Possible options. These variables are checked when the user tries to 'set' an option
    def poss_opt(self):
        return ('domain')

    # Show options
    def show_opt(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + ("%-*s %-*s %-*s %s" % (15, "OPTION", 8, "RQ", 18, "VALUE", "DESCRIPTION")) + bc.ENDC
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "------", 8, "--", 18, "-----", "-----------"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "domain:", 8, "y", 18, self.domain, 'Domain to check'))
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


def run():
    print('\t[*] Running spoofcheck on domain.. please wait.\n\n')
    command = 'spoofcheck ' + sop.domain
    os.system(command)
    print('\n')


def info():
    print("""
        A program that checks if a domain can be spoofed from. The program checks SPF and DMARC records for weak configurations that allow spoofing.

        Additionally it will alert if the domain has DMARC configuration that sends mail or HTTP requests on failed SPF/DKIM emails.

        Domains are spoofable if any of the following conditions are met:
        - Lack of an SPF or DMARC record
        - SPF record never specifies ~all or -all
        - DMARC policy is set to p=none or is nonexistent

        Arthur: https://github.com/BishopFox/spoofcheck
""")


# CONSOLE
def console():
    value = input("   -> " + bc.FAIL + "wmd" + bc.ENDC + "@" + bc.FAIL + "mailspoofchc:" + bc.ENDC + " ")
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


def main():
    print('\n')
    print('    _______           __                _ __                   ___  ')
    print('   / ___/ /  ___ ____/ /__  __ _  ___ _(_) /__ ___  ___  ___  / _/  ')
    print('  / /__/ _ \/ -_) __/  \'_/ /  \' \/ _ `/ / (_-</ _ \/ _ \/ _ \/ _/   ')
    print('  \___/_//_/\__/\__/_/\_\ /_/_/_/\_,_/_/_/___/ .__/\___/\___/_/     ')
    print('                                            /_/                     ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkInstalled('spoofcheck')
    comm.checkNetConnectionV()
    print('')
    global sop
    sop = options('www.apple.com')
    console()
