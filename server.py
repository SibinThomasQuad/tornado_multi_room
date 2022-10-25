import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket as ws
from tornado.options import define, options
import time
import logging
logging.basicConfig(filename                    = "server_log.log",
					format                                     = '%(asctime)s %(message)s',
					filemode                                   = 'w')
logger                                          = logging.getLogger()
logger.setLevel(logging.DEBUG)
define('port', default=4041, help='port to listen on')
ROOMS                                           = {}
class Debug                                     : 
    def server_log(self,message)                : 
        logger.debug(message)
class Room                                      : 
    def exit_room(self,room_id,user)            : 
        user_list                               = ROOMS[str(room_id)]
        user_list.remove(user)
        ROOMS[str(room_id)]                     = user_list
    def remove_room(self,room_id)               : 
        del ROOMS[str(room_id)]
    def get_room_members(self,room_id)          : 
        members                                 = ROOMS[str(room_id)]
        return members
    def create_room(self,room,member)           : 
        ROOMS[str(room)]                        = [member]
    def join_room(self,room,member)             : 
        room_members                            = ROOMS[str(room)]
        room_members.append(member)
        ROOMS[str(room)]                        = room_members
class web_socket_handler(ws.WebSocketHandler)   : 
    @classmethod
    def route_urls(cls)                         : 
        return [(r'/',cls, {}),]
    
    def simple_init(self)                       : 
        self.last                               = time.time()
        self.stop                               = False
    
    def open(self)                              : 
        self.simple_init()
        #print("[+] New client connected")
        self.write_message("You are connected")
    def on_message(self, message)               : 
        message_decoded                         = message
        data_set                                = message_decoded.split(":")
        rooms                                   = Room()
        server_obj                              = Debug()
        try                                     : 
            if(data_set[0] == 'create_room'):
		"""Code to create the room"""
                try                             : 
                    rooms.create_room(data_set[1],self)
                    server_obj.server_log("Room created ("+data_set[1]+")")
                    self.write_message("CREATED")
                except                          : 
                    server_obj.server_log("Room creation failed ("+data_set[1]+")")
                    self.write_message("Room creation failed room ("+data_set[1]+")")
            elif(data_set[0] == 'join_room'):
		"""Code to join the room"""
                try                             : 
                    rooms.join_room(data_set[1],self)
                    server_obj.server_log("User joined to room ("+data_set[1]+")")
                    self.write_message("JOINED")
                except                          : 
                    server_obj.server_log("Join to room failed ("+data_set[1]+")")
                    self.write_message("Join to room failed ("+data_set[1]+")")
            elif(data_set[0] == 'remove_room'):
		"""Code to delete the room"""
                rooms.remove_room(data_set[1])
                server_obj.server_log("Room removed ("+data_set[1]+")")
                self.write_message("Room removed ("+data_set[1]+")")
            elif(data_set[0] == 'leave_room'):
		"""Code to exit the room"""
                rooms.exit_room(data_set[1],self)
            else                                : 
                users                           = rooms.get_room_members(data_set[1])
                for x in users                  : 
                    try                         : 
                        if(data_set[2] == 'others'):
                            if(self == x):
                                pass
                            else                : 
                                x.write_message(data_set[0])
                        else                    : 
                            x.write_message(data_set[0])
                        self.last               = time.time()
                    except                      : 
                        rooms.exit_room(data_set[1],x)
                        pass
                        #print("[+] Dead user Ditected")
        except                                  : 
            server_obj.server_log("Invalid message format ("+message+") use like this message:room_id")
            self.write_message("Invalid message format ("+message+") use like this message:room_id")
            
    
    def on_close(self)                          : 
        print("connection is closed")
        #self.stop()
    def check_origin(self, origin)              : 
        return True
def initiate_server()                           : 
    server_obj                                  = Debug()
    print("[+] Server Starting...")
    try                                         : 
        #create a tornado application and provide the urls
        app                                     = tornado.web.Application(web_socket_handler.route_urls())
        #setup the server
        server                                  = tornado.httpserver.HTTPServer(app)
        server.listen(options.port)
        #start io/event loop
        print("[+] Server Started")
        server_obj.server_log("Server Started")
        tornado.ioloop.IOLoop.instance().start()
    except                                      : 
        print("[-] Server Starting failed")
if __name__ == '__main__':
    initiate_server()
