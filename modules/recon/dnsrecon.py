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
global dnsrecon
DNSRECON_SYM = (config['TOOLS']['DNSRECON_SYM'])
DNSRECON_GITNAME = (config['TOOLS']['DNSRECON_GITNAME'])
DNSRECON_GITRUN = (config['TOOLS']['DNSRECON_GITRUN'])
# END Log files, global variables, etc.


# OPTIONS
class options():
    Author = 'Thomas TJ (TTJ)'
    Name = 'dnsrecon'
    Call = 'dnsrecon'
    Modulename = 'dnsrecon'
    Category = 'recon'
    Type = 'dns'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Multiple DNS recon abilities.'
    Datecreation = '2017/01/01'
    Lastmodified = '2017/01/01'

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
            + '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'arg:', 8, 'n', 18, self.arg, 'Arguments, e.g. "-w files/wordlist.txt"'))
            + '\n'
            )

    # Show commands
    def show_commands(self):
        print(
            ''
            + '\n\t' + bc.OKBLUE + 'COMMANDS:' + bc.ENDC
            + '\n\t' + '---------'
            + '\n\t' + ('%-*s ->\t%s' % (9, 'run', 'Run the script'))
            + '\n\t' + ('%-*s ->\t%s' % (9, 'help', 'Help'))
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
    print('')
    if sop.args:
        os.system(dnsrecon + ' -d ' + sop.domain + ' ' + sop.arg)
    else:
        os.system(dnsrecon + ' -d ' + sop.domain)
    print('')


def helpMe():
    print("""
        arguments:
        -h, --help                  Show this help message and exit
        -d, --domain      <domain>  Domain to Target for enumeration.
        -r, --range       <range>   IP Range for reverse look-up brute force in formats (first-last) or in (range/bitmask).
        -n, --name_server <name>    Domain server to use, if none is given the SOA of the target will be used
        -D, --dictionary  <file>    Dictionary file of sub-domain and hostnames to use for brute force.
        -f                          Filter out of Brute Force Domain lookup records that resolve to the wildcard defined IP Address when saving records.
        -t, --type        <types>   Specify the type of enumeration to perform:
                                    std      To Enumerate general record types, enumerates. SOA, NS, A, AAAA, MX and SRV if AXRF on the NS Servers fail.
                                    rvl      To Reverse Look Up a given CIDR IP range.
                                    brt      To Brute force Domains and Hosts using a given dictionary.
                                    srv      To Enumerate common SRV Records for a given domain.
                                    axfr     Test all NS Servers in a domain for misconfigured zone transfers.
                                    goo      Perform Google search for sub-domains and hosts.
                                    snoop    To Perform a Cache Snooping against all NS servers for a given domain, testing all with
                                             file containing the domains, file given with -D option.
                                    tld      Will remove the TLD of given domain and test against all TLD's registered in IANA
                                            zonewalk Will perform a DNSSEC Zone Walk using NSEC Records.

        -a                          Perform AXFR with the standard enumeration.
        -s                          Perform Reverse Look-up of ipv4 ranges in the SPF Record of the targeted domain with the standard enumeration.
        -g                          Perform Google enumeration with the standard enumeration.
        -w                          Do deep whois record analysis and reverse look-up of IP ranges found thru whois when doing standard query.
        -z                          Performs a DNSSEC Zone Walk with the standard enumeration.
        --threads          <number> Number of threads to use in Range Reverse Look-up, Forward Look-up Brute force and SRV Record Enumeration
        --lifetime         <number> Time to wait for a server to response to a query.
        --db               <file>   SQLite 3 file to save found records.
        --xml              <file>   XML File to save found records.
        --iw                        Continua bruteforcing a domain even if a wildcard record resolution is discovered.
        -c, --csv          <file>   Comma separated value file.
        -j, --json         <file>   JSON file.
        -v                          Show attempts in the bruteforce modes.
    """)


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
    elif 'run' in userinput[:1]:
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
    print('      ____  _   _______                            ')
    print('     / __ \/ | / / ___/________  _________  ____   ')
    print('    / / / /  |/ /\__ \/ ___/ _ \/ ___/ __ \/ __ \  ')
    print('   / /_/ / /|  /___/ / /  /  __/ /__/ /_/ / / / /  ')
    print('  /_____/_/ |_//____/_/   \___/\___/\____/_/ /_/   ')
    print('                                                   ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    global dnsrecon
    dnsrecon = comm.checkInstalledFull(DNSRECON_SYM, DNSRECON_GITNAME, DNSRECON_GITRUN)
    print('')
    global sop
    # The parameters to be passed to the module on init
    sop = options('apple.com', '')
    console()
