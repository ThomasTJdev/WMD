#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import rarfile
from multiprocessing import Process
from core.colors import bc as bc
import core.modules as cmodules
import core.commands as comm


# START Log files, global variables, etc.


# END Log files, global variables, etc.


# OPTIONS
class Options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'BF RAR'
    Call = 'bfrar'
    Modulename = 'bruteforcerar'
    Category = 'bruteforce'
    Type = 'rar'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Bruteforce a RAR file'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

    def __init__(self, file, pwdlist, threads):
        self.file = file
        self.pwdlist = pwdlist
        self.threads = threads
        self.show_all()

    # Possible options. These variables are checked when the user tries to 'set' an option
    def poss_opt(self):
        return ('file', 'pwdlist', 'threads')

    # Show options
    def show_opt(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + ("%-*s %-*s %-*s %s" % (15, "OPTION", 8, "RQ", 18, "VALUE", "DESCRIPTION")) + bc.ENDC
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "------", 8, "--", 18, "-----", "-----------"))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "file:", 8, "y", 18, self.file, 'Path to ZIP file'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "pwdlist:", 8, "y", 18, self.pwdlist, 'Path to passwordlist'))
            + "\n\t" + ("%-*s %-*s %-*s %s" % (15, "threads:", 8, "y", 18, self.threads, 'Number of threads to use'))
            + "\n"
            )

    # Show commands
    def show_commands(self):
        print(
            ""
            + "\n\t" + bc.OKBLUE + "COMMANDS:" + bc.ENDC
            + "\n\t" + "---------"
            + "\n\t" + ("%-*s ->\t%s" % (9, "run", "Run the script"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "so", "Show options"))
            + "\n\t" + ("%-*s ->\t%s" % (9, "sa", "Show module info"))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'invoke', 'Invoke module'))
            + "\n\t" + ("%-*s ->\t%s" % (9, "exit", "Exit"))
            + "\n"
            )

    # Show all info
    def show_all(self):
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


def extract_file(passwords):
    global waitpwd
    with rarfile.RarFile(sop.file) as rf:
        for password in passwords:
            try:
                rf.extractall(path='tmp/', pwd=password)
                print('[+] Found password: ' + str(password))
                print('[*] Ctrl+c to exit bruteforce')
                return None
            except Exception as e:
                pass
    print('No password for this thread')


def run():
    with open(sop.pwdlist, 'rb') as pass_file:
        passwords = [i.strip() for i in pass_file]

    N_PROC = int(sop.threads)
    for i in range(N_PROC):
        p = Process(target=extract_file, args=[passwords[i::N_PROC]])
        p.start()


# CONSOLE
def console():
    value = input("   -> " + bc.FAIL + "wmd" + bc.ENDC + "@" + bc.FAIL + "bfrar:" + bc.ENDC + " ")
    userinput = value.split()
    if 'so' in userinput[:1]:
        sop.show_opt()
    elif 'sa' in userinput[:1]:
        sop.show_all()
    elif 'run' in userinput[:1]:
        run()
        input("   -> " + bc.FAIL + "wmd" + bc.ENDC + "@" + bc.FAIL + "bfrar:" + bc.ENDC + " [*] Please wait while bruteforcing with " + sop.threads + " threads")
    elif 'set' in userinput[:1]:
        useroption = str(userinput[1:2]).strip('[]\'')
        uservalue = str(userinput[2:3]).strip('[]\'')
        if useroption not in sop.poss_opt():
            print(bc.WARN + "\n    Error, no options for: " + useroption + "\n" + bc.ENDC)
        elif useroption in sop.poss_opt():
            setattr(sop, useroption, uservalue)
            print('\n      ' + useroption + '\t> ' + uservalue + "\n")
    elif 'invoke' in userinput[:1]:
        comm.invokeModule(Options.Call)
        return None
    elif 'back' in userinput[:1] or 'exit' in userinput[:1]:
        return None
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + "\n    Error, no options for: " + command + "\n" + bc.ENDC)
    console()
# END console


def main():
    print('\n')
    print('     ___  ____  ___  ___   ___   ')
    print('    / _ )/ __/ / _ \/ _ | / _ \  ')
    print('   / _  / _/  / , _/ __ |/ , _/  ')
    print('  /____/_/   /_/|_/_/ |_/_/|_|   ')
    print('')
    print('\n')
    global sop
    sop = Options('', 'files/pwd_john.txt', '8')
    console()
