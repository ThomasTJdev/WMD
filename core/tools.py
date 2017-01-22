#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#


import configparser
import os
import shutil
from datetime import datetime
from core.colors import bc as bc


config = configparser.ConfigParser()
config.read('core/config.ini')
UPDATE_COMM = (config['ENVIRONMENT']['UPDATE_COMM'])
INSTALL_COMM = (config['ENVIRONMENT']['INSTALL_COMM'])


def checkStart(SYM, GIT, GITNAME, ACTION):
    """Start function to check weather a program is installed."""
    print('\t[*] Checking if ' + bc.BOLD + GITNAME + bc.ENDC + ' exists on system')
    checkSym(SYM, GIT, GITNAME, ACTION)


def checkSym(SYM, GIT, GITNAME, ACTION):
    """Check if executable is found on system."""
    if shutil.which(SYM) is None or not SYM:
        if GITNAME:
            print(bc.WARN + '\t[-] No symlink found for ' + SYM + '. Checking for git in tools/' + bc.ENDC)
            checkGit(SYM, GIT, GITNAME, ACTION)
        else:
            print(bc.WARN + '\t[-] No symlink found for ' + SYM + '. Install using:' + bc.ENDC)
            install = input('\t->  ' + INSTALL_COMM + ' ' + SYM + ' (Y/n)')
            if install.lower() != 'n':
                os.system(INSTALL_COMM + ' ' + SYM)
    else:
        print(bc.OKGREEN + '\t[+] Symlink exists' + bc.ENDC)
        if ACTION.lower() == 'u':
            print('\t[*] Updating: ' + GITNAME)
            os.system(UPDATE_COMM + ' ' + SYM)
        print('')


def checkGit(SYM, GIT, GITNAME, ACTION):
    """Check if executable is found in git folder."""
    if not os.path.isdir('tools/' + GITNAME):
        print('\t[-] No repo found for ' + GITNAME)
        print(bc.OKGREEN + '\t[+]' + bc.ENDC + ' Cloning repo to tools\n')
        os.system('git clone ' + GIT + ' tools/' + GITNAME)
    else:
        print(bc.OKGREEN + '\t[+] Repo exists' + bc.ENDC)
        if ACTION.lower() == 'u':
            print('\t[*] Updating repo: ' + GITNAME)
            os.system('git -C tools/' + GITNAME + ' pull origin master')
        print('')


def clonegits(ACTION):
    """Clone git repos."""
    # Admin-Finder
    SYM = (config['TOOLS']['ADMINFINDER_SYM'])
    GIT = (config['TOOLS']['ADMINFINDER_GIT'])
    GITNAME = (config['TOOLS']['ADMINFINDER_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # arp
    SYM = (config['TOOLS']['ARP_SYM'])
    GIT = (config['TOOLS']['ARP_GIT'])
    GITNAME = (config['TOOLS']['ARP_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # beef
    SYM = (config['TOOLS']['BEEF_SYM'])
    GIT = (config['TOOLS']['BEEF_GIT'])
    GITNAME = (config['TOOLS']['BEEF_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # bettercap
    SYM = (config['TOOLS']['BETTERCAP_SYM'])
    GIT = (config['TOOLS']['BETTERCAP_GIT'])
    GITNAME = (config['TOOLS']['BETTERCAP_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # changeme
    SYM = (config['TOOLS']['CHANGEME_SYM'])
    GIT = (config['TOOLS']['CHANGEME_GIT'])
    GITNAME = (config['TOOLS']['CHANGEME_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # create_ap
    SYM = (config['TOOLS']['CREATEAP_SYM'])
    GIT = (config['TOOLS']['CREATEAP_GIT'])
    GITNAME = (config['TOOLS']['CREATEAP_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # crackmapexec
    SYM = (config['TOOLS']['CRACKMAPEXEC_SYM'])
    GIT = (config['TOOLS']['CRACKMAPEXEC_GIT'])
    GITNAME = (config['TOOLS']['CRACKMAPEXEC_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # dnsmap
    SYM = (config['TOOLS']['DNSMAP_SYM'])
    GIT = (config['TOOLS']['DNSMAP_GIT'])
    GITNAME = (config['TOOLS']['DNSMAP_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # dnsrecon
    SYM = (config['TOOLS']['DNSRECON_SYM'])
    GIT = (config['TOOLS']['DNSRECON_GIT'])
    GITNAME = (config['TOOLS']['DNSRECON_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # ExploitDB
    SYM = (config['TOOLS']['EXPLOITDB_SYM'])
    GIT = (config['TOOLS']['EXPLOITDB_GIT'])
    GITNAME = (config['TOOLS']['EXPLOITDB_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # hashID
    SYM = (config['TOOLS']['HASHID_SYM'])
    GIT = (config['TOOLS']['HASHID_GIT'])
    GITNAME = (config['TOOLS']['HASHID_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # instabot.py
    SYM = (config['TOOLS']['INSTABOT_SYM'])
    GIT = (config['TOOLS']['INSTABOT_GIT'])
    GITNAME = (config['TOOLS']['INSTABOT_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # john
    SYM = (config['TOOLS']['JOHN_SYM'])
    GIT = (config['TOOLS']['JOHN_GIT'])
    GITNAME = (config['TOOLS']['JOHN_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # nmap
    SYM = (config['TOOLS']['MACCHANGER_SYM'])
    GIT = (config['TOOLS']['MACCHANGER_GIT'])
    GITNAME = (config['TOOLS']['MACCHANGER_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # nmap
    SYM = (config['TOOLS']['NMAP_SYM'])
    GIT = (config['TOOLS']['NMAP_GIT'])
    GITNAME = (config['TOOLS']['NMAP_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # Routersploit
    SYM = (config['TOOLS']['ROUTERSPLOIT_SYM'])
    GIT = (config['TOOLS']['ROUTERSPLOIT_GIT'])
    GITNAME = (config['TOOLS']['ROUTERSPLOIT_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    # spoofcheck
    SYM = (config['TOOLS']['SPOOFCHECK_SYM'])
    GIT = (config['TOOLS']['SPOOFCHECK_GIT'])
    GITNAME = (config['TOOLS']['SPOOFCHECK_GITNAME'])
    checkStart(SYM, GIT, GITNAME, ACTION)

    updatefile = 'logs/lasttoolupdate.txt'
    if not os.path.isfile(updatefile):
        os.mknod(updatefile)
    with open(updatefile, 'w') as file:
        file.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
