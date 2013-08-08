

from scapy.all import *

def parse(database, filename):
    """
    Parses pcap file into sqlite database
    """
    pcap = rdpcap(filename)
    
    for pkt in pcap:
        ip = pkt.getlayer(IP)
        
        proto = ''
        src = ()
        dst = ()
        if ip.proto == 6:
            proto = 'tcp'
            if ip.haslayer(TCP):
                tcp = ip.getlayer(TCP)
                src = ip.src, tcp.sport
                dst = ip.dst, tcp.dport
        else:
            pass
            
        packet = {}
        packet['id'] = ip.id
        packet['proto'] = proto
        packet['src'] = src
        packet['dst'] = dst
        
        database.insert_packet(packet)
        
    

