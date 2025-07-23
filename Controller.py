import socket as Socket
import time
import sys
import pygame
import threading
import json

#Communication variables 
respond = "Data stuff"

#Pygame Variables
running = True


#movement thingys
#A is the acceleraion thingy
fwd = False
fwdA= 0

right = False
rightA = 0

left = False
leftA = 0

down = False
downA = 0

lower = False
up = False

Movement = {"fwd": fwd, "fwdA": fwdA, "right": right, "rightA": rightA, "left": left, "leftA": leftA, "down": down, "downA": downA, "lower": lower, "up": up}



def Accel(Check, accelVar):
        if Check == True and accelVar < 1:

                accelVar += 0.05
        elif Check == False and accelVar > 0:

                accelVar -=0.05
        accelVar = round(accelVar, 4)
        return accelVar





def UI():
        global running, fwd, right, left, down, lower, up, fwdA, rightA, leftA, downA, Movement
        #set variables global so u can change


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


        #Load Font
        Font = pygame.font.Font("Font.ttf", 23)
        



        while running:
                
                Movement = {"fwd": fwd, "fwdA": fwdA, "right": right, "rightA": rightA, "left": left, "leftA": leftA, "down": down, "downA": downA, "lower": lower, "up": up, "running": running}



                textSurface = Font.render("fwd: " +str(fwdA) + " right: " + str(rightA) + " down: " + str(downA) + " left: " + str(leftA), True, "White")
                #Adjusts the acceleration

                fwdA = Accel(fwd, fwdA)
                downA = Accel(down, downA)
                rightA = Accel(right, rightA)
                leftA = Accel(left, leftA)

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
                if GridRect.bottom < 505:
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

                                if event.key == pygame.K_SPACE:
                                        up = True
                                
                                if event.key == pygame.K_LCTRL:
                                        lower = True

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

                                if event.key == pygame.K_SPACE:
                                        up = False  

                                if event.key == pygame.K_LCTRL:
                                        lower = False

                #Draws Circle and text
                pygame.draw.circle(screen, (255,255,255), (x/2, y/2), 15)
                screen.blit(textSurface, (0,0))

                #Updates the window
                pygame.display.flip()
                clock.tick(100)

                   



def Communication():
        socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
        #Creates the socket
        print("socketmake")
        Host = "0.0.0.0"
        Port = 55555


        socket.bind((Host, Port))
        #Attaches a socket to a location
        print("socket bind")
        socket.listen(5)
        print("waiting")
        conn, adress = socket.accept()
        #Connects to the conncetion

        print("connected by: " + adress[0])

        while running:
                #Data to be sent
                give = json.dumps(Movement)
                
                conn.send(give.encode())

                responce = conn.recv(1024)
                print(responce)

                time.sleep(0.1)
        sys.exit()
        
UIthread = threading.Thread(target=UI)
communicationThread = threading.Thread(target=Communication)

UIthread.start()
communicationThread.start()
