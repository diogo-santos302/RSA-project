from scapy.all import ARP, Ether, srp

def get_connected_devices(ip_range: str, timeout: int) -> list:
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
    result = srp(arp_request, timeout=timeout, verbose=False)[0]
    devices = []
    for sent, received in result:
        devices.append(received.psrc)
    return devices
