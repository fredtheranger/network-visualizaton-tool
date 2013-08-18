
import argparse, os
import ipcalc

def getargs():   
    
    parser = argparse.ArgumentParser()
    parser.add_argument("pcap", help="Path to pcap file")
    parser.add_argument("-n", "--network", help="Network to use as root", default="192.168.0.0/24")
    args = parser.parse_args()
    
    # Check if pcap is a valid file
    if not os.path.exists(args.pcap):
        print "Invalid pcap file. Quitting."
        exit(1)
        
    # TODO: validate network argument using regex
    
    return args
    
def get_ip_range(network):
    return [ str(x) for x in ipcalc.Network(network) ]
