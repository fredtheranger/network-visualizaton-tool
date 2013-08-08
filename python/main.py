"""
Network Visualization and Exploration Tool

CS6393 Final Project

Network forensics tool that takes a pcap file, parses the network data into a 
sqlite database, generates JSON, and allows the data to be visualized using the
D3.js library.  
"""

from netviz import dao, parser, utils

# parse the command line args
args = utils.getargs()

# initialize the database
database = dao.DAO("sqlite.db")


# parse pcap into sqlite db
parser.parse(database, args.pcap)

# generate json file(s)

# start python server to serve javascript application
