
import sqlite3

class DAO:

    def __init__(self, filename, clear=True):
        """
        Initializes the database tables and returns a connection
        """
        conn = sqlite3.connect(filename)
        
        if clear:
            conn.execute("DROP TABLE IF EXISTS packets")
            conn.execute("CREATE TABLE IF NOT EXISTS packets ( \
                            id INTEGER PRIMARY KEY, \
                            src_addr TEXT NOT NULL, \
                            src_port INTEGER NOT NULL, \
                            dst_addr TEXT NOT NULL, \
                            dst_port INTEGER NOT NULL \
                         );")
        self.conn = conn
         
    def insert_packet(self, packet):
        """
        Inserts a packet into the packets table
        """
        #conn.execute("INSERT INTO packets (src_addr, src_port, dst_addr, dst_port) \
        #                VALUES(?, ?, ?, ?)", (packet["src"][0]
        print packet                   
      
