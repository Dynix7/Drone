import network
import socket
from machine import Pin
import time
import sys
import _thread
import ujson
from rp2 import PIO, StateMachine, asm_pio
wifiName = ""
wifiPassword = ""
# wait chat literally bot behavivor i need to actually download them
led = Pin("LED", Pin.OUT)
Movement = {}

Host = ""
#Enter the local laptop IP
Port = 55555

#Prevents threads from like writing over eachother
lock = _thread.allocate_lock()

#Starting at top right and going counterclockwise
# 0 - 2047


m1Pin = 16 #Clockwise
m2Pin = 17 #Counter Clockwise
m3Pin = 18 #CW
m4Pin = 19 #CCW


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
    


try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket make")
    #Creates the socket
except Exception as e:
    print("ur cooked lil bro no socket", e)
    sys.exit()

time.sleep(3)

try:
    socket.connect((Host, Port))
    print("connected to socket")
    #Attempting to connect
except Exception as e:
    print("no connected :(", e)
    #If theres an error

connect(wifiName, wifiPassword)






#DISCLAIMER
#DISCLAIMER
#DISCLAIMER
#NGL I HAVE NO CLUE HOW THE DSHOT COMMUNICATION PROTOCOL WORKS so im just using this and I hope it works 
#I would just use a module but uhh idk cant find

DSHOT_SPEED = 150  # kbps

@asm_pio(
    sideset_init=PIO.OUT_LOW,
    out_shiftdir=PIO.SHIFT_LEFT,  # MSB first
    autopull=True,
    pull_thresh=16,
)
def dshot():
    # Send each bit (MSB first)
    # For DSHOT: 0 = short high, long low; 1 = long high, short low
    # 1: high 2/3 of bit time, 0: high 1/3 of bit time
    set(x, 15)                 # 16 bits
    label("bitloop")
    out(y, 1)                  # Pull next bit to y
    mov(pins, y)   [2]         # Set pin (high/low) for high time (2 cycles)
    nop()         [1]          # Stay high for 1 more cycle
    set(pins, 0)  [2]          # Set pin low for low time (2 cycles)
    jmp(x_dec, "bitloop")      # Next bit

# Helper to create DSHOT packet
def create_packet(throttle, telemetry=0):
    packet = (throttle << 1) | (telemetry & 0x1)
    csum = 0
    csum_data = packet
    for _ in range(3):  # Only XOR 3 nibbles (12 bits)
        csum ^= csum_data & 0xF
        csum_data >>= 4
    csum &= 0xF
    return (packet << 4) | csum

def send_dshot_to_escs(throttles, pins=None, dshot_speed=150):
    if pins is None:
        pins = [16, 17, 18, 19]
    packets = [create_packet(t) for t in throttles]
    freq = dshot_speed * 1000 * 3  # 3 cycles per bit

    sms = []
    for i, pin_num in enumerate(pins):
        sm = StateMachine(i, dshot, freq=freq, sideset_base=Pin(pin_num))
        sm.active(1)
        sms.append(sm)
    for sm, packet in zip(sms, packets):
        sm.put(packet)
# Example usage with custom pins:
# send_dshot_to_escs([1000, 1000, 1000, 1000], pins=[2, 3, 4, 5])
#Send every 10-20ms



def coms():
    global Movement
    while True:
       
        try:
            recieve = socket.recv(1024)
            if recieve:
                
                lock.acquire()
                
                recieve = recieve.decode()
                Movement = ujson.loads(recieve)
                
                print(Movement)
                
                led.toggle()
                respond = "fr"
                final = respond.encode()
                socket.send(final)
                
                lock.release()
                
                time.sleep(0.1)
                
            else:
                print("nothing back, conn closed")
                break
                
        except Exception as e:
            print(e)
            break

#ALSO IS REALIZED THAT THERE IS NO ROLL CONTROL SO UHHH lol
def motorControl():
    
    m1T = 0 #CW top right
    m2T = 0 #CCW top left
    m3T = 0 #CW bottom left
    m4T = 0 #CCW bottom right
    
    
    
    m1TSave = 0
    m2TSave = 0
    m3TSave = 0
    m4TSave = 0
    #Just adding a wait for communication purposes
    time.sleep(5)
    
    while True:
        
        lock.acquire()
        
        if Movement["running"] == True:
            if m1T == 0:
                m1T = m2T = m3T = m4T = 100
                
            if Movement["up"] == True:
                m1T+=40
                m2T+=40
                m3T+=40
                m4T+=40
                
            if Movement["lower"] == True:
                m1T-=40
                m2T-=40
                m3T-=40
                m4T-=40
        
            if Movement["fwd"] == True:
                #95% of the original speed for the front motors
                m1T = 0.95 * m1TSave
                m2T = 0.95 * m2TSave
                m3T = 1.05 * m3TSave
                m4T = 1.05 * m4TSave
                
            if Movement["down"] == True:
                m1T = 1.05 * m1TSave
                m2T = 1.05 * m2TSave
                m3T = 0.95 * m3TSave
                m4T = 0.95 * m4TSave
            
            #Needs to rotate clockwise so increase CCW motors 2 and 4 since torque is opposite of rotation direction
            if Movement["right"] == True:
                m1T = 0.95 * m1TSave
                m2T = 1.05 * m2TSave
                m3T = 0.95 * m3TSave
                m4T = 1.05 * m4TSave
            
            #Needs to rotate counterclockwise so increase CW motors 1 and 3
            if Movement["left"] == True:
                m1T = 1.05 * m1TSave
                m2T = 0.95 * m2TSave
                m3T = 1.05 * m3TSave
                m4T = 0.95 * m4TSave
          
        
            #Safety Checks so it doesn't go too high or between 1 to 47
            if m1T > 1969 or m2T > 1969:
                m1T = m2T = m3T = m4T = 1969
                
            if m1T < 50 or m2T < 50:
                m1T = m2T = m3T = m4T = 50
            
            #Makes whole number so like it doesn't explode
            m1T = round(m1T)
            m2T = round(m2T)
            m3T = round(m3T)
            m4T = round(m4T)
            

                
            #Saves the current motor value so it can go back to them once movement stops
            #Turns out this is harder than I thought
            if m1T == m2T == m3T == m4T:
                m1TSave = m1T
                m2TSave = m2T
                m3TSave = m3T
                m4TSave = m4T
            
            #Ensures that when no movement all the motors are the same speed
            elif Movement["motion"] == False:
                m1T = m1TSave
                m2T = m2TSave
                m3T = m3TSave
                m4T = m4TSave
            
            lock.release()
            
            send_dshot_to_escs([m1T, m2T, m3T, m4T], pins=[m1Pin, m2Pin, m3Pin, m4Pin], dshot_speed = 150)
                               
                          
            time.sleep(.012)
        
        else:
            send_dshot_to_escs([0, 0, 0, 0], pins=[m1Pin, m2Pin, m3Pin, m4Pin], dshot_speed = 150)
            break

_thread.start_new_thread(coms, ())
#_threada.start_new_thread(motorControl, ())