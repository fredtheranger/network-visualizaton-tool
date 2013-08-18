"""

Resources:
    - http://pymotw.com/2/json/
    - http://stackoverflow.com/questions/5766230/select-from-sqlite-table-where-rowid-in-list-using-python-sqlite3-db-api-2-0
    
"""
import sqlite3
import utils
import json
import csv
import os

from datetime import datetime

class DAO:

    def __init__(self, filename, clear=False):
        """
        Initializes the database tables and returns a connection
        """
        conn = sqlite3.connect(filename)
        
        if clear:
            conn.execute("DROP TABLE IF EXISTS packets")
            conn.execute("CREATE TABLE IF NOT EXISTS packets ( \
                            id INTEGER, \
                            ts datetime, \
                            proto TEXT NOT NULL, \
                            src TEXT NOT NULL, \
                            sport INTEGER, \
                            dst TEXT NOT NULL, \
                            dport INTEGER, \
                            payload TEXT \
                         );")
                         
            conn.execute("DROP TABLE IF EXISTS info")
            conn.execute("CREATE TABLE IF NOT EXISTS info ( \
                            local TEXT NOT NULL, \
                            filename TEXT NOT NULL, \
                            date_processed TEXT, \
                            total_packets INTEGER \
                        );")
                        
        self.conn = conn
        
    def populate_info(self, filename, network, total_packets):
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute("INSERT INTO info (local, filename, date_processed, \
                        total_packets) VALUES (?, ?, ?, ?)",
                            (network, filename, today, total_packets))
        self.conn.commit()
                            
    def get_info(self, output_json=False):
        c = self.conn.cursor()
        c.execute("SELECT local, filename, date_processed, total_packets FROM info")
        return json.dumps(c.fetchone()) if output_json else c.fetchone()
        
         
    def insert_packet(self, packet):
        """
        Inserts a packet into the packets table
        """
        
        # Check to see if id is already in database, so this is an ip fragment
        #data = self.conn.execute("SELECT id FROM packets WHERE id = ?", (packet["id"],))

        try:
            self.conn.execute("INSERT INTO packets \
                              (id, ts, proto, src, sport, dst, dport) \
                              VALUES(?, ?, ?, ?, ?, ?, ?)", (
                              packet["id"],
                              packet["ts"],
                              packet["proto"],
                              packet["src"][0],
                              packet["src"][1],
                              packet["dst"][0],
                              packet["dst"][1]
                         ))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print e
        
    def get_sources_data(self):
        """
        Generates the json for the treemap by protoco, then source IP
        """
        network = utils.get_ip_range(self.get_info()[0])
                 
        c1 = list()
        q1 = "SELECT src, count(*) \
                FROM packets \
                GROUP BY src"
        for level1 in self.conn.execute(q1):
            if not level1[0] in network:
                continue
                
            c2 = list()
            q2 = "SELECT dst, count(*) \
                FROM packets \
                WHERE src = ? \
                GROUP BY dst"
            for level2 in self.conn.execute(q2, (level1[0],)):
                child = { "name":level2[0], "value":level2[1] }
                c2.append(child)
            
            child = { "name":level1[0], "value":level1[1], "children":c2 }
            c1.append(child)
               
            
        data = { "name": "root", "value":len(c1), "children":c1 }
        return json.dumps(data, indent=2)
        
    def get_sources_detail(self, src, dst):
        """
        Generates the data to display in the destination by source tab
        """
        data = list()
        q = "SELECT proto, src, sport, dst, dport \
            FROM packets \
            WHERE src = ? and dst = ? \
            ORDER BY src, dst, dport"
        for row in self.conn.execute(q, (src, dst)):
            data.append(row)
        
        print json.dumps(data) 
        return json.dumps(data)      
            
    def generate_data_for_protocol_chart(self):
        """
        Generates the data to display protocol counts by (local) source IP
        """
        network = utils.get_ip_range(self.get_info()[0])
        
        data = {}
        q = "SELECT src, proto, count(*) \
            FROM packets \
            WHERE src IN ( {seq} ) \
            GROUP BY src, proto".format( seq=",".join(["?"]*len(network)))
        for row in self.conn.execute(q, network):
            src = row[0]
            proto = row[1]
            cnt = row[2]
            
            if src not in data:
                data[src] = list()
                
            data[src].append( {"proto":proto, "value":cnt} )
            
        print json.dumps( data ) 
        return json.dumps( data )    
               
    def get_protocol_details(self, src, proto):
        """
        Generates the data to display for the protocol details view
        """
        data = list()
        q = "SELECT src, sport, dst, dport \
             FROM packets \
             WHERE src = ? AND proto = ? \
             ORDER BY dst, dport, sport"
        for row in self.conn.execute(q, (src, proto)):
            data.append(row)
        
        print json.dumps(data) 
        return json.dumps(data)
        
    def get_destination_data(self):
        
        network = utils.get_ip_range(self.get_info()[0])
                 
        c1 = list()
        q1 = "SELECT src, count(*) \
                FROM packets \
                GROUP BY src"
        for level1 in self.conn.execute(q1):
            if not level1[0] in network:
                continue
                
            c2 = list()
            q2 = "SELECT proto, count(*) \
                FROM packets \
                WHERE src = ? \
                GROUP BY proto"
            for level2 in self.conn.execute(q2, (level1[0],)):
                
                c3 = list()
                q3 = "SELECT dst, count(*) \
                      FROM packets \
                      WHERE src = ? AND proto = ? \
                      GROUP BY dst"
                for level3 in self.conn.execute(q3, (level1[0], level2[0],)):
                    child = { 
                        "name":level3[0],"size":level3[1] 
                    }
                    c3.append(child)
            
                child = { "name":level2[0], "children":c3 }
                c2.append(child)
            
            child = { "name":level1[0], "children":c2 }
            c1.append(child)
               
            
        data = { "name": "root", "children":c1 }
        return json.dumps(data, indent=2)
            
        
             
           
    def get_timeline_data(self):
        """
        Generates the data to create the timeline visualization
        GROUP BY strftime('%Y-%m-%d %H:%M', ts) \
        """
        data = list()
        q = "SELECT count(ts) \
             FROM packets  \
             GROUP BY datetime(ts) \
             ORDER BY ts" 
        for row in self.conn.execute(q):
            data.append(row[0])
             
        return json.dumps(data)
                        
      
