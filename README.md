network-visualizaton-tool
======================

Overview:

Network forensics tool to parse pcap and provide visualizations using D3.js.

Pre-requisites:
- Python 2.6+
- ipcalc: https://pypi.python.org/pypi/ipcalc
- web.py: http://webpy.org/  (or sudo apt-get install python-webpy)

Import and parsing pcap file:


- Usage: python python/main.py -n <local_network> <path_to_pcap>
- Example: python python/main.py -n 192.168.1.0/24 /home/user/example.pcap

Viewing the results:

- python python/server.py

Resources used:

- http://d3js.org/
- https://github.com/mbostock/d3/wiki/Gallery
- http://bl.ocks.org/benjchristensen/2579599
- http://bl.ocks.org/mbostock/4063269
- http://www.d3noob.org/2012/12/adding-axis-labels-to-d3js-graph.html
