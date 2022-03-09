from websocket import create_connection
from threading import Thread
ws = create_connection("ws://localhost:4041/")
def recive():
    while True:
        result =  ws.recv()
        print(">>>"+result)
def short_lived_connection():
    while True:
        data = input("Enter")
        ws.send(data)
        #result =  ws.recv()
        #print("<<Received '%s'" % result)
        #ws.close()
thread1 = Thread(target = short_lived_connection)
thread1.start()
thread2 = Thread(target = recive)
thread2.start()
