import socket as Socket
import time
import sys
import pygame
import threading


def UI():
        pygame.init()






socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
print("socketmake")
Host = "0.0.0.0"
Port = 55555
num = 0

socket.bind((Host, Port))
print("socket bind")
socket.listen(5)
print("waiting")
conn, adress = socket.accept()

print("connected by: " + adress[0])

while True:
        give = "amongus"+ str(num)
        final = give.encode()
        conn.send(final)

        respond = conn.recv(1024)
        print(respond)
        num +=1
        time.sleep(0.1)
        
        


