import network
import socket
from machine import Pin
import time
import sys
import _thread
import ujson
import rp2
wifiName = ""
wifiPassword = ""
# wait chat literally bot behavivor i need to actually download them
led = Pin("LED", Pin.OUT)
Movement = {}

Host = ""
#Enter the local laptop IP
Port = 55555

lock = _thread.allocate_lock()

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
#NGL I HAVE NO CLUE HOW THE DSHOT COMMUNICATION PROTOCOL WORKS I JUST STOLE THIS
#I would just use a libary but uhh idk cant find

def send_dshot_to_escs(throttles, pins=None, dshot_speed=150):
    """
    Send DSHOT signals to 4 ESCs.

    Parameters:
        throttles: list of 4 throttle values (0-2047)
        pins: list of 4 GPIO pin numbers, default is [16, 17, 18, 19]
        dshot_speed: DSHOT speed in kbps, default 150
    """
    if pins is None:
        pins = [16, 17, 18, 19]  # default GPIO pins

    # Function to create a simple 16-bit DSHOT packet with checksum
    def create_packet(throttle, telemetry=0):
        packet = (throttle << 1) | (telemetry & 0x1)
        # Simple checksum: XOR of 4 4-bit nibbles
        csum = 0
        csum_data = packet
        for _ in range(4):
            csum ^= (csum_data & 0xF)
            csum_data >>= 4
        csum &= 0xF
        return (packet << 4) | csum  # 16-bit packet
    
    # Generate packets for each throttle
    packets = [create_packet(t) for t in throttles]
    
    # Calculate frequency based on DSHOT speed (approximate)
    freq = dshot_speed * 1000 * 16  # cycles per second

    # Define the PIO program to send 16 bits
    @rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.SHIFT_RIGHT, autopull=True, pull_thresh=16)
    def dshot():
        label("start")
        mov(x, osr)             # load 16 bits into x
        label("bit_loop")
        pull()                  # get next bit
        jmp(x_not_zero, "send_one")
        # Send 0: low for 1 cycle
        set(pins, 0) [1]
        jmp("done")
        label("send_one")
        # Send 1: high for 2 cycles
        set(pins, 1) [1]
        set(pins, 1) [1]
        label("done")
        in_(x, 1)
        jmp(x, "bit_loop")

    # Initialize and activate a state machine for each pin
    sm_list = []
    for pin_num in pins:
        sm = rp2.StateMachine(
            0, dshot, freq=freq, sideset_pin=Pin(pin_num)
        )
        sm.active(1)
        sm_list.append(sm)

    # Send packets to each ESC
    for sm, packet in zip(sm_list, packets):
        sm.put(packet)

# Example usage with custom pins:
# send_dshot_to_escs([1000, 1000, 1000, 1000], pins=[2, 3, 4, 5])
#Send every 10-20ms



def coms()
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
            
coms()
   
