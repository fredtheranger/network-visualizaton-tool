"""
Network Visualization and Exploration Tool

CS6393 Final Project

Network forensics tool that takes a pcap file, parses the network data into a 
sqlite database, generates JSON, and allows the data to be visualized using the
D3.js library.  
"""

from netviz import dao, parser, utils
import web

# parse the command line args
args = utils.getargs()

# initialize the database
print "\nInitializing database..."
database = dao.DAO("sqlite.db", True)

# parse pcap into sqlite db
print "\nParsing %s and inserting into database..." % args.pcap
total = parser.parse(database, args.pcap)

database.populate_info(args.pcap, args.network, total)

print "\nParsing and database population complete, you may start the server now."
