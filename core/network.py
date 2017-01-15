#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#


import logging
import sys
from time import sleep
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # Shut up scapy!
from scapy.all import sniff, ARP, Dot11Beacon, Dot11ProbeResp
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


global seen_arp
seen_arp = {}


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
