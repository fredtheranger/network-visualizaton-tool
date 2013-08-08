
import argparse, os

def getargs():   
    
    parser = argparse.ArgumentParser()
    parser.add_argument("pcap", help="Path to pcap file")
    args = parser.parse_args()
    
    # Check if pcap is a valid file
    if not os.path.exists(args.pcap):
        print "Invalid pcap file. Quitting."
        exit(1)
    
    return args
