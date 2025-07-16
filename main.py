import network
import socket
from machine import Pin
import time
import sys
import _thread
import ujson

wifiName = ""
wifiPassword = ""
# wait chat literally bot behavivor i need to actually download them
led = Pin("LED", Pin.OUT)
Movement = {}

Host = ""
#Enter the laptop IP
Port = 55555



def connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print(wlan.scan())
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        time.sleep(1)
        led.toggle()
        #Loop while trying to connect
    print("connected to the minecraft server")
    print(wlan.ifconfig())
    # https://docs.micropython.org/en/latest/library/network.WLAN.html
    
connect(wifiName, wifiPassword)

try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket make")
    #Creates the socket
except Exception as e:
    print("ur cooked lil bro no socket", e)
    sys.exit()

time.sleep(5)

try:
    socket.connect((Host, Port))
    print("connected to socket")
    #Attempting to connect
except Exception as e:
    print("no connected :(", e)
    #If theres an error


while True:
   
    try:
        recieve = socket.recv(1024)
        if recieve:
            
            recieve = recieve.decode()
            Movement = ujson.loads(recieve)
            
            print(Movement)
            
            led.toggle()
            
            respond = "fr"
            final = respond.encode()
            socket.send(final)
            
            time.sleep(0.1)
            
        else:
            print("nothing back, conn closed")
            break
            
    except Exception as e:
        print(e)
        break
            
    
   
