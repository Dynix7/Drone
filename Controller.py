import socket as Socket
import time
import sys
import pygame
import threading
import numpy

#Communication variables 
respond = "Data stuff"

#Pygame Variables
running = True


#movement thingys
fwd = False
right = False
left = False
down = False
lower = False
up = False


def UI():
        pygame.init()
        #Variables and Stuff
        clock = pygame.time.Clock()
        x,y = (500,500)

        #Setup Window/screen 
        screen = pygame.display.set_mode((x,y))
        pygame.display.set_caption("Drone Controller")

        #Load Background
        Grid = pygame.image.load("Grid.png").convert()
        GridRect = Grid.get_rect(center = (x/2, y/2))

        #Load Text
        Font = pygame.font.Font("Font.ttf", 23)
        textSurface = Font.render(str(respond), True, "White")

        global running, fwd, right, left, down, lower, up
        #set variables global so u can change

        while running:

                #Moves the background by doing opposite of movement key
                if fwd == True:
                        GridRect.centery += 3.7
                if down == True:
                        GridRect.centery -= 3.7
                if right == True:
                        GridRect.centerx -= 3.7
                if left == True:
                        GridRect.centerx += 3.7

                
                #Infinitely repeats grid by teleporting it back to where it came from
                #Teleport up(fwd)
                if GridRect.top > 0:
                        GridRect.centery -=y

                #Teleport Down(down)
                if GridRect.bottom < 513:
                        GridRect.centery +=y

                #Teleport Right(Right)
                if GridRect.right < 500:
                        GridRect.centerx +=x
                #Teleport Left(left)
                if GridRect.left > 0:
                        GridRect.centerx -=x



                screen.blit(Grid, GridRect)

                for event in pygame.event.get():
                        #Closes the window
                        if event.type == pygame.QUIT:
                                running = False
                                pygame.quit()
                                sys.exit()
                        
                        #Movement
                        if event.type == pygame.KEYDOWN:
                                
                                #Fwd movement
                                if event.key == pygame.K_w:
                                        fwd = True

                                #Down movement        
                                if event.key == pygame.K_s:
                                        down = True

                                #Right movement
                                if event.key == pygame.K_d:
                                        right = True

                                #Left movement
                                if event.key == pygame.K_a:
                                        left = True


                        elif event.type == pygame.KEYUP:
                                #Detects fwd release
                                if event.key == pygame.K_w:
                                        fwd = False

                                #Detects down button release thingy idk 
                                if event.key == pygame.K_s:
                                        down = False

                                if event.key == pygame.K_d:
                                        right = False

                                if event.key == pygame.K_a:
                                        left = False   

                #Draws Circle and text
                pygame.draw.circle(screen, (255,255,255), (x/2, y/2), 15)
                screen.blit(textSurface, (0,0))

                #Updates the window
                pygame.display.flip()
                clock.tick(100)
                   

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
        
        


