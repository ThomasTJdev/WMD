#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#


import os
import subprocess
import shlex
import shutil
import http.client
import psutil
import netifaces
import random
import requests
from bs4 import BeautifulSoup
from core.colors import bc as bc
import core.core as core


config = core.config()
logger = core.log()


# VARIABLES START
MACS = (config['FILES']['MACS'])
PROXYLIST = (config['FILES']['PROXYLIST'])
USERAGENTS = (config['FILES']['USERAGENTS'])
# VARIABLES END


def invokeModule(call):
    """Open module in new xterm window."""
    logger.debug('Invoking module')
    subprocess.Popen(['xterm', '-T', 'Module: ' + call, '-bg', 'black', '-fg', 'white', '-geometry', '120x30+1280+0', '-e', 'python', 'wmd.py', '-m', call, '-q'])


def runCommand(call, module_name):
    """Run command in new xterm window placed up right."""
    call = ('xterm -hold -T ' + module_name + ' -bg black -fg white -geometry 120x30+1280+0 -e ' + call)
    args = shlex.split(call)
    logger.debug('Running os.system command: ' + call)
    subprocess.Popen(args)


def runCommand2(call, module_name):
    """Run command in new xterm window placed down right."""
    call = ('xterm -hold -T ' + module_name + ' -bg black -fg white -geometry 120x30+1280+1000 -e ' + call)
    args = shlex.split(call)
    logger.debug('Running os.system command: ' + call)
    subprocess.Popen(args)


def runCommand3(call, module_name):
    """Run command in new xterm window placed up left."""
    call = ('xterm -hold -T ' + module_name + ' -bg black -fg white -geometry 120x30+0+0 -e ' + call)
    args = shlex.split(call)
    logger.debug('Running os.system command: ' + call)
    print(str(args))
    subprocess.Popen(args)


def checkInstalledFull(sym, gitname, gitrun):
    """Check weather a program is installed on system or in GIT folder.

    This function first checks weather the program is installed as an
    executable on system. If it's not, the function will check the specified
    git folder to find the executable.

    If none of the above returns a positive result, "ERROR" will be returned.
    If the aboe returns a positive result, the path to the executable will be returned.

    Call to function should be formatted like this:
    program = checkInstalledFull('hashid', 'hashID', 'hashid.py') <-- Symlink, Git_Folder_Name, File_To_Run_In_Git_Folder
    """
    print('\t[*]  Checking ' + sym)
    if shutil.which(sym) is None:
        print(bc.FAIL + '\t[-]  ERR! ' + sym + ' not found as executable! Checking tools/ folder' + bc.ENDC)
        if os.path.isdir('tools/' + gitname):
            print(bc.OKGREEN + '\t[+]  OK! Don\'t worry, repo exists in tools/' + bc.ENDC)
            return ('tools/' + gitname + '/' + gitrun)
        else:
            print(bc.FAIL + '\t[-]  ERR! ' + sym + ' not in tools folder.' + bc.ENDC)
            return 'ERROR'
    else:
        print(bc.OKGREEN + '\t[+]  OK! Found sym for ' + sym + bc.ENDC)
        return sym


def checkInstalledFullOpt(sym, gitname, gitrun):
    """See the function checkInstalledFull(). This function just prints "optional"."""
    print('\t[*]  Checking ' + sym)
    if shutil.which(sym) is None:
        print(bc.WARN + '\t[-]  WARN! ' + sym + ' not found as executable! Checking tools/ folder.  Optional!' + bc.ENDC)
        if os.path.isdir('tools/' + gitname):
            print(bc.OKGREEN + '\t[+]  OK! Don\'t worry, repo exists in tools/' + bc.ENDC)
            return ('tools/' + gitname + '/' + gitrun)
        else:
            print(bc.WARN + '\t[-]  WARN! ' + sym + ' not in tools folder. Optional!' + bc.ENDC)
            return 'ERROR'
    else:
        print(bc.OKGREEN + '\t[+]  OK! Found sym for ' + sym + bc.ENDC)
        return sym


def checkInstalled(program):
    """Check if a program is installed as an executable."""
    print('\t[*]  Checking ' + program)
    if shutil.which(program) is None:
        print(bc.FAIL + '\t[-]  ERR! ' + program + ' not found as executable! Manual edit this moduel with the path or run the installtools from the main menu.' + bc.ENDC)
        return 'ERROR'
    else:
        print(bc.OKGREEN + '\t[+]  OK! Found ' + program + bc.ENDC)
        return None


# Silent check
def checkInstalledS(program):
    """Check if a program is installed as an executable. Silent check."""
    if shutil.which(program) is None:
        print(bc.FAIL + '\t[-]  ERR! ' + program + ' not found as executable! Manual edit this moduel with the path or run the installtools from the main menu.' + bc.ENDC)
        return 'ERROR'
    else:
        logger.debug('Program installed: ' + program)
        return None


def checkInstalledOpt(program):
    """Check if a program is installed as an executable. Optional check."""
    print('\t[*]  Checking ' + program)
    if shutil.which(program) is None:
        print(bc.WARN + '\t[-]  WARN! ' + program + ' not found as executable! Optional..' + bc.ENDC)
        return 'ERROR'
    else:
        print(bc.OKGREEN + '\t[+]  OK! Found ' + program + bc.ENDC)
        return None


def checkInstalledGit(program):
    """Check if a gitfolder exists."""
    print('\t[*]  Checking ' + program)
    if not os.path.isdir(program):
        print(bc.FAIL + '\t[-]  ERR! ' + program + ' not found! Manual edit this scripts with path or install.' + bc.ENDC)
        return 'ERROR'
    else:
        print(bc.OKGREEN + '\t[+]  OK! Found ' + program + bc.ENDC)
        return None


def checkNetConnectionV():
    """Check if there's a working network connection. Verbose."""
    # Header request for net connectivity
    print(bc.ENDC + "\t[*]  Checking network connection" + bc.ENDC)
    conn = http.client.HTTPConnection("www.microsoft.com", 80)
    try:
        conn.request("HEAD", "/")
        print(bc.OKGREEN + "\t[+]  OK! Network connection seems OK" + bc.ENDC)
        return None
    except:
        print(bc.WARN + "\t[-]  WARN! Network connection seems down" + bc.ENDC)
        return 'ERROR'


def checkNetConnection():
    """Check if there's a working network connection. Silent."""
    # Header request for net connectivity
    conn = http.client.HTTPConnection("www.microsoft.com", 80)
    try:
        conn.request("HEAD", "/")
        logger.debug('Network connection working')
        return None
    except:
        logger.debug('Network connection not working')
        return 'ERROR'


def checkNetVPNV():
    """Check if there's a working VPN connection. Verbose."""
    # Checking for VPN interfaces
    INTERFACE_VPN = (config['NETWORK']['INTERFACE_VPN'])
    print(bc.ENDC + '\t[*]  Checking if VPN connection is active' + bc.ENDC)
    for s in psutil.net_if_addrs():
        if any(f in s for f in INTERFACE_VPN.split(',')):
            print(bc.OKGREEN + '\t[+]  Indications of a VPN. Good. Will continue.' + bc.ENDC)
            return None
    else:
        print(bc.WARN + '\t[-]  WARN! No indication of a VPN connection on "tun" or "ppp" found.')
        return 'ERROR'


def checkTorV():
    """Check if there's a working TOR connection. Verbose."""
    # Check if current connections goes through Tor
    print(bc.ENDC + '\t[*]  Checking if TOR connection is active' + bc.ENDC)
    publicIP = getPublicIP()
    try:
        torNodes = requests.get('https://check.torproject.org/exit-addresses', timeout=5)
        logger.debug('Requesting torproject.org for exit-addresses')
    except:
        print(bc.WARN + '\t[-]  WARN! Connection to torproject.org timed out in 5 sec. Couldn\'t verify connection.' + bc.ENDC)
        return 'ERROR'
    soup = BeautifulSoup(torNodes.text, 'html.parser')
    torNodes = soup.findAll(text=True)
    for torIP in torNodes:
        torIP = torIP.replace('\n', '')
        if publicIP in torIP:
            print(bc.OKGREEN + '\t[+]  Your public IP is a TOR exit node' + bc.ENDC)
            return None
    print(bc.WARN + '\t[-]  WARN! Your public IP is ' + bc.BOLD + 'NOT a TOR exit node' + bc.ENDC)
    return 'ERROR'


def getInterfaces():
    """Get all network interfaces."""
    interfaces = subprocess.getoutput("netstat -i | awk '{print $1}'")
    interfaces = str(interfaces)
    interfaces = interfaces.replace("\n", ",")
    interfaces = interfaces.replace("Kernel,Iface,", "")
    interfaces = interfaces.split(",")
    if len(interfaces) >= 0:
        logger.debug('Returning list of interfaces')
        return interfaces
    else:
        print(bc.WARN + '\t[-]  WARN! No network interfaces found' + bc.ENDC)
        return None


def getPublicIP():
    """Get users public IP. Silent."""
    try:
        url = 'http://ipinfo.io/ip'
        try:
            r = requests.get(url, timeout=5)
            logger.debug('Requesting ip from ipinfo.io')
        except:
            print(bc.WARN + '\t[-]  WARN! Connection to ipinfo.io timed out in 5 sec. Couldn\'t verify public IP.' + bc.ENDC)
            return 'ERROR'
        soup = BeautifulSoup(r.text, 'html.parser')
        r = soup.findAll(text=True)
        return str(r).strip('\\n\'[]')
    except:
        logger.debug('Error in requesting and parsing ip from ipinfo.io')
        return 'ERROR'


def getPublicIPV():
    """Get users public IP. Verbose."""
    try:
        url = 'http://ipinfo.io/ip'
        try:
            r = requests.get(url, timeout=5)
            logger.debug('Requesting ip from ipinfo.io')
        except:
            print(bc.WARN + '\t[-]  WARN! Connection to ipinfo.io timed out in 5 sec. Couldn\'t verify public IP.' + bc.ENDC)
            return 'ERROR'
        soup = BeautifulSoup(r.text, 'html.parser')
        r = soup.findAll(text=True)
        print(bc.OKGREEN + '\t[+]  Your public IP is: ' + str(r).strip('\\n\'[]') + bc.ENDC)
        return None
    except:
        print(bc.WARN + '\t[-]  Couldn\'t get public IP' + bc.ENDC)
        return 'ERROR'


def getLocalIP(interface):
    """Get users local ip.

    Pass interface if known, else just parse empty ''.
    For accessing IP use: local_ip[0]
    """
    ip = ''
    try:
        ip = netifaces.ifaddresses(interface)[2][0]['addr']
        logger.debug('Returning ip from netifaces: ' + str([ip]))
        return ([ip])
    except:
        interfaces = getInterfaces()
        for interf in interfaces:
            try:
                ip = netifaces.ifaddresses(interf)[2][0]['addr']
                if ip and ip != '127.0.0.1':
                    logger.debug('Returning ip and interface from netifaces. IP: ' + str(ip) + ' INT: ' + str(interf))
                    return ([ip, interf])
            except:
                pass
    return ''


def getLocalIP_interface():
    """Get local IP with interface from CONFIG (config.ini). Silent."""
    INTERFACE_NET = (config['NETWORK']['INTERFACE_NET'])
    try:
        ip = netifaces.ifaddresses(INTERFACE_NET)[2][0]['addr']
        logger.debug('Returning local ip: ' + ip)
        return (ip)
    except:
        return 'ERROR'


def getLocalIP_interfaceV():
    """Print local IP with interface from CONFIG (config.ini). Verbose."""
    INTERFACE_NET = (config['NETWORK']['INTERFACE_NET'])
    try:
        ip = netifaces.ifaddresses(INTERFACE_NET)[2][0]['addr']
        print(bc.OKGREEN + '\t[+]  Your local IP is: ' + ip + bc.ENDC)
        return None
    except:
        logger.debug('Error in getting local IP')
        return 'ERROR'


def getGateway():
    """Get gateway address."""
    gws = netifaces.gateways()
    gateway = gws['default'][netifaces.AF_INET]
    logger.debug('Returning gateway')
    return gateway[0]


def getRandomProxy(conn_type):
    """Get random proxy from list.

    conn_type should be set to either HTTP or HTTPS.
    Proxylist is defined in CONFIG (config.ini).
    """
    uas = []
    with open(PROXYLIST, 'r') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua)
    random.shuffle(uas)
    proxy = random.choice(uas)
    proxy = proxy.strip('\n')
    proxy = {conn_type.lower(): proxy}
    try:
        r1 = requests.get('https://www.google.com', proxies=proxy, timeout=5)
        # r2 = BeautifulSoup(r1.text, 'html.parser')
        # nogo = r2.findAll(text=re.compile('forbidden'))
        # if r1.status_code == 200 and not nogo:
        # if r1.status_code in (200, 204, 400, 401, 403, 404, 500, 502, 301) and not nogo:
        # Change below just to check 200. Multiple fault check not needed
        if r1.status_code not in (204, 400, 401, 403, 404, 500, 502, 301):
            print('\tUsing proxy: ' + str(proxy))
            return proxy
        else:
            print('\tShitty proxy')
    except (KeyboardInterrupt, SystemExit):
        print('\t[!] User stopped the loop')
        return '0.0.0.0:0'
    except:
        print('\tError' + str(proxy))

    getRandomProxy(conn_type)


def getRandomProxyUserlist(conn_type, uproxyfile):
    """Get random proxy from list.

    conn_type should be set to either HTTP or HTTPS.
    Proxylist is defined with: uproxyfile
    The list (uproxyfile) shall contain the proxies in the format url:port.
    """
    uas = []
    with open(uproxyfile, 'r') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua)
    random.shuffle(uas)
    proxy = random.choice(uas)
    proxy = proxy.strip('\n')
    proxy = {conn_type.lower(): proxy}
    try:
        r1 = requests.get('https://www.google.com', proxies=proxy, timeout=5)
        # r2 = BeautifulSoup(r1.text, 'html.parser')
        # nogo = r2.findAll(text=re.compile('forbidden'))
        if r1.status_code not in (204, 400, 401, 403, 404, 500, 502, 301):
            print('\tUsing proxy: ' + str(proxy))
            return proxy
        else:
            print('\tShitty proxy')
    except (KeyboardInterrupt, SystemExit):
        print('\t[!] User stopped the loop')
        return '0.0.0.0:0'
    except:
        print('\tError' + str(proxy))

    getRandomProxy(conn_type, uproxyfile)


def getUserAgentHeader():
    """Get random user agent."""
    uas = []
    with open(USERAGENTS, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)
    ua = random.choice(uas)  # select a random user agent
    headers = {"Connection": "close", "User-Agent": ua}
    return headers


def getMac():
    """Get MAC address."""
    addrs = netifaces.ifaddresses('eno1')
    maca = addrs[netifaces.AF_LINK][0]['addr']
    return maca


def getNewMac(searchterm):
    """Find a new MAC address based on user search criteria."""
    uas = []
    with open(MACS, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua and searchterm:
                try:
                    if searchterm.lower() in str(ua).lower():
                        uas.append(ua.strip())
                except:
                    pass
            elif ua and not searchterm:
                uas.append(ua.strip())
    if uas:
        random.shuffle(uas)
        maca = random.choice(uas)  # select a random user agent
        maca = str(maca).strip('\'b')[:8]
        macrnd = ("%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        maca += ':' + macrnd
    else:
        maca = 'None found'
    return maca


def findLineInFile(filename, searchterm):
    """Find specific line in file.

    filename = The name of the file.
    searchterm = What the line needs to include.
    """
    with open(filename, 'r') as file:
        for line in file.readlines():
            if line and searchterm in line:
                return line


def changeLineInFile(filename, old_text, new_text):
    """Change specific line in file if line match.

    filename = The name of the file.
    old_text = The current line in file (to be replaced).
    new_text = The new line (replace with).
    """
    filenameTmp = (filename + '.tmp')
    orgText = None
    with open(filename, 'r') as input_file, open(filenameTmp, 'w') as output_file:
        for line in input_file:
            if line.strip() == str(old_text):
                output_file.write(str(new_text) + '\n')
                orgText = line.strip()
            else:
                output_file.write(line)
    os.system('mv ' + filenameTmp + ' ' + filename)
    return orgText


def changeLineInFileFirstWord(filename, new_text):
    """Change specific line in file if first word match.

    filename = The name of the file.
    new_text = The new line (replace with).
    """
    filenameTmp = (filename + '.tmp')
    orgText = None
    with open(filename, 'r') as input_file, open(filenameTmp, 'w') as output_file:
        for line in input_file:
            if line.strip().startswith(str(new_text.split()[:1]).strip('[]\'')):
                output_file.write(str(new_text) + '\n')
                orgText = line.strip()
            else:
                output_file.write(line)
    os.system('mv ' + filenameTmp + ' ' + filename)
    return orgText
