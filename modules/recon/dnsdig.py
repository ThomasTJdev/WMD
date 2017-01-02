#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import os
try:
    import core.core as core
    import core.modules as cmodules
    import core.commands as comm
    from core.colors import bc as bc
except:
    import sys
    sys.path.append('././')
    import core.core as core
    import core.modules as cmodules
    import core.commands as comm
    from core.colors import bc as bc


# START Log files, global variables, etc.
config = core.config()
logger = core.log()


DIG_SYM = (config['TOOLS']['DIG_SYM'])
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'Domain info groper'
    Call = 'dig'
    Modulename = 'dnsdig'
    Category = 'recon'
    Type = 'dns'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Using dig command you can query DNS name servers for your DNS lookup related tasks'
    Datecreation = '01/01/2017'
    Lastmodified = '01/01/2017'

    def __init__(self, domain, arguments):
        self.domain = domain
        self.arg = arguments
        self.show_all()

    # Possible options. These variables are checked when the user tries to 'set' an option
    def poss_opt(self):
        return ('domain', 'arg')

    # Show options
    def show_opt(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 8, 'RQ', 18, 'VALUE', 'DESCRIPTION')) + bc.ENDC
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 8, '--', 18, '-----', '-----------'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'domain:', 8, 'y', 18, self.domain, 'Target domain (no WWW!)'))
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'arg:', 8, 'n', 18, self.arg, 'Arguments, e.g. "-t ANY"'))
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s ->\t%s' % (9, 'run', 'Run simple'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'runmx', 'Run MX'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'runns', 'Run NS'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'runany', 'Run ANY'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'runrev', 'Run reverse on IP'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'help', 'Help'))
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
    if sop.arg:
        os.system(DIG_SYM + ' ' + sop.domain + ' ' + sop.arg)
    else:
        os.system(DIG_SYM + ' ' + sop.domain)
    print('')


def runmx():
    print('')
    if sop.arg:
        os.system(DIG_SYM + ' -t MX ' + sop.domain + ' ' + sop.arg)
    else:
        os.system(DIG_SYM + ' -t MX ' + sop.domain)
    print('')


def runns():
    print('')
    if sop.arg:
        os.system(DIG_SYM + ' -t NS ' + sop.domain + ' ' + sop.arg)
    else:
        os.system(DIG_SYM + ' -t NS ' + sop.domain)
    print('')


def runany():
    print('')
    if sop.arg:
        os.system(DIG_SYM + ' -t ANY ' + sop.domain + ' ' + sop.arg)
    else:
        os.system(DIG_SYM + ' -t ANY ' + sop.domain)
    print('')


def runrev():
    print('')
    if sop.arg:
        os.system(DIG_SYM + ' -x ' + sop.domain + ' ' + sop.arg)
    else:
        os.system(DIG_SYM + ' -x ' + sop.domain)
    print('')


def helpMe():
    print('')
    os.system(DIG_SYM + ' -h')
    print('')


# CONSOLE
def console():
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'dig:' + bc.ENDC + ' ')
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'help' in userinput[:1]:
        helpMe()
    elif 'run' in userinput[:1]:
        run()
    elif 'runmx' in userinput[:1]:
        run()
    elif 'runns' in userinput[:1]:
        run()
    elif 'runany' in userinput[:1]:
        run()
    elif 'runrev' in userinput[:1]:
        run()
    elif 'set' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        uservalue = value.split(' ', 2)[2]
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
    print('\t    ____  __________   _ __     ___   ')
    print('\t   / __ \/  _/ ____/  (_) /_   /__ \  ')
    print('\t  / / / // // / __   / / __/    / _/  ')
    print('\t / /_/ // // /_/ /  / / /_     /_/    ')
    print('\t/_____/___/\____/  /_/\__/    (_)     ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkNetConnectionV()
    comm.checkInstalled(DIG_SYM)
    print('')
    global sop
    # The parameters to be passed to the module on init
    sop = options('apple.com', '')
    console()
