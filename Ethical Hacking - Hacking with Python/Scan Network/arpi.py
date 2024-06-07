
from scapy.all import *

network_interface = "wlan0"
ip_range = "192.168.1.1/24"
broadcast_mac = "ff:ff:ff:ff:ff:ff"

packet = Ether(dst=broadcast_mac)/ARP(pdst = ip_range) 

ans, unans = srp(packet, timeout=5, iface=network_interface, inter=0.1)

for send,receive in ans:
    print(receive.sprintf(r"%Ether.src% - %ARP.psrc%"))     
