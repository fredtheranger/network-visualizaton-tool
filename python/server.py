# simple python server to serve html/javascript and restful service
import web
from netviz import dao, utils

urls = ( "/service/protocols", "protocols",
         "/service/protocol/details/(.*)/(.*)", "protocol_details",
         "/service/sources", "sources",
         "/service/source/details/(.*)/(.*)", "source_details",
         "/service/destinations", "destinations",
         "/service/info", "info",
         "/service/timeline", "timeline" )

class protocols:
    def GET(self):  
        database = dao.DAO("sqlite.db")
        return database.generate_data_for_protocol_chart()
        
class protocol_details:
    def GET(self, proto, src):
        database = dao.DAO("sqlite.db")
        return database.get_protocol_details(src, proto)
        
class sources:
    def GET(self):
        database = dao.DAO("sqlite.db")
        return database.get_sources_data()
        
class source_details:
    def GET(self, src, dst):
        database = dao.DAO("sqlite.db")
        return database.get_sources_detail(src, dst)
        
class destinations:
    def GET(self):
        database = dao.DAO("sqlite.db")
        return database.get_destination_data()
        
class info:
    def GET(self):
        database = dao.DAO("sqlite.db")
        return database.get_info(True)
        
class timeline:
    def GET(self):
        database = dao.DAO("sqlite.db")
        return database.get_timeline_data()

if __name__ == "__main__":
    
    app = web.application(urls, globals())
    app.run() 

