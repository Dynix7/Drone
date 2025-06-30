import socket as Socket
import time
import sys
import pygame
import threading

#Communication variables
respond = "deez"

#Pygame Variables
running = True


#Mixed
fwd = False
right = False
left = False
Down = False
Lower = False
Up = False


def UI():
        pygame.init()
        #Variables and Stuff
        clock = pygame.time.Clock()
        x,y = (500,500)
        Font = pygame.font.Font("Font.ttf", 23)
        textSurface = Font.render(str(respond), True, "Black")


        global running
        #sets the running variable global so u can change
        
        screen = pygame.display.set_mode((x,y))
        pygame.display.set_caption("Drone Controller")
        #Starts and creates the window

        while running:
                screen.fill((255,255,255))
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                running = False
                                pygame.quit()
                                sys.exit()
                        #Closes the window

                pygame.draw.circle(screen, (0,0,0), (x/2, y/2), 15)
                screen.blit(textSurface, (0,0))


                pygame.display.flip()
                clock.tick(100)
                #Updates the window
                


UI()


socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
#Creates the socket
print("socketmake")
Host = "0.0.0.0"
Port = 55555
num = 0

socket.bind((Host, Port))
#Attaches a socket to a location
print("socket bind")
socket.listen(5)
print("waiting")
conn, adress = socket.accept()
#Connects to the conncetion

print("connected by: " + adress[0])

while True:
        give = "amongus"+ str(num)
        final = give.encode()
        conn.send(final)

        respond = conn.recv(1024)
        print(respond)
        num +=1
        time.sleep(0.1)
        
        


