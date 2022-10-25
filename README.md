# tornado_multi_room

1 Deploy server.py in to the server and take the public ip address and port of the server

2 and connect client.py to server via socket (with the server ip and port)

3 sent message 

       create_room:room_id     

for room creation

4 sent message 
    
    join_room:room_id 
    
   to join room

5 message

    message:room_id:all 
    
   to sent to all users in that room include room creater
    message:room_id:others
    
   to sent to all users in that room exclude room creater
