# ECE5725 Embedded Operating System Final Project
# Final Project: ratglove_receiver.py
# December 7, 2017
# Authors: Vishisht M. Tiwari and Kyu Sub Shin
# NetIDs: vmt28 and ks763
# Description: This program runs on the computer and is used for establishing.
#               bluetooth connection on the computer. It also received different
#               signals from the PI and preforms mouse actions
###################################################################
# importing libraries
###################################################################
from bluetooth import *
import pyautogui as mouse
import time

###################################################################
# Set variables
###################################################################
sleepTime = 0
startScrolling = False
startDragging = False

mouse.PAUSE = 0     # pyautogui function call
                    #will wait for 1 second if
                    #in case i want to control
                    #the mouse using my mouse

mouse.FAILSAFE = False  # pyautogui has a failsafe
                        #feature where i can crash
                        #this python program by taking
                        # my mouse to the top-left
                        # corner. I am disabling that

width,height = mouse.size()     # this returns the size of the screen

###################################################################
# Create the server socket
###################################################################
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "12345678-1234-1234-1234-123456789012"

advertise_service( server_sock, "RatGlove",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        numbers = data.split(",")
        
        # For left Click
        if (float(numbers[1]) ==  5000.0):
            startScrolling = False
            startDragging = False
            mouse.click()
            
        # For double Click
        elif (float(numbers[1]) ==  10000.0):
            mouse.doubleClick()

        # For right Click
        elif (float(numbers[1]) ==  15000.0):
            mouse.rightClick()

        # For switching on the dragging mode
        elif (float(numbers[1]) ==  20000.0):
            startDragging = True
            mouse.mouseDown(button = 'left')

        # For switching on the scrolling mode
        elif (float(numbers[1]) == 25000.0):
            startScrolling = True

         # Move the mouse pointer in normal and dragging mode
         # In scrolling mode nove the acroll up or down
        else:
            if (startScrolling):
                if (float(numbers[1]) > 20000):
                    mouse.scroll(float(numbers[1])-25000)
                else:
                    mouse.scroll(float(numbers[1]))
            else:
                mouse.moveRel(float(numbers[1]),float(numbers[0]),duration=0.05)
        if (startDragging):
            mouse.mouseDown(button = 'left')
        else:
            mouse.mouseUp(button = 'left')

except IOError:
    pass

print("disconnected")

###################################################################
# Disconnect Socket
###################################################################
client_sock.close()
server_sock.close()
print("all done")
