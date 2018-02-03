# ECE5725 Embedded Operating System Final Project
# Final Project: Use_Multiple_Moving_Mouse_version6.py
# December 7, 2017
# Authors: Vishisht M. Tiwari and Kyu Sub Shin
# NetIDs: vmt28 and ks763
# Description: This program runs on the pi. It connects using bluetooth to
#               a computer. It also tracks the movement of the hand and fingers
#               of the hand and then sends the corresponding signals to the
#               computer.

###################################################################
# importing libraries
###################################################################
from pygame.locals import *
from mpu6050 import mpu6050
from bluetooth import *
import smbus
import time
import sys
import math
import numpy as np
import subprocess
import pygame
import os
import RPi.GPIO as GPIO
import pygame

###################################################################
# set the environments for piTFT
###################################################################
os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') #
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

###################################################################
# initialize pygame
###################################################################
pygame.init()
pygame.mouse.set_visible(False)

###################################################################
# Set variables
###################################################################
speed = 3
addr = None
timeTrack = 0
averaging = 10
click_averaging = 10
count_avg = 0
count_click = 0
x_rotation_gyro = 0
y_rotation_gyro = 0
z_rotation_gyro = 0
I2C_address = 0x71
I2C_bus_number = 1
I2C_ch_0 = 0b00000001
I2C_ch_1 = 0b00000010
I2C_ch_2 = 0b00000100
I2C_ch_3 = 0b00001000
I2C_ch_4 = 0b00010000
I2C_ch_5 = 0b00100000
I2C_ch_6 = 0b01000000
I2C_ch_7 = 0b10000000
x_rotation_gyro_center = 0
y_rotation_gyro_center = 0
z_rotation_gyro_center = 0
x_rotation_gyro_index = 0
y_rotation_gyro_index = 0
z_rotation_gyro_index = 0
x_rotation_gyro_middle = 0
y_rotation_gyro_middle = 0
z_rotation_gyro_middle = 0
x_rotation_gyro_ring = 0
y_rotation_gyro_ring = 0
z_rotation_gyro_ring = 0
x_rotation_gyro_pinki = 0
y_rotation_gyro_pinki = 0
z_rotation_gyro_pinki = 0
x_rotation_gyro_thumb = 0
y_rotation_gyro_thumb = 0
z_rotation_gyro_thumb = 0
mux_channel = [I2C_ch_0, I2C_ch_1, I2C_ch_2, I2C_ch_3, I2C_ch_4, I2C_ch_5, I2C_ch_6, I2C_ch_7]
mouseSelected = True
fpsSelected = False
puzzleSelected = False
threedSelected = False
customSelected = False
paused = False
size = width,height = 320,240
white = 255,255,255
red = 255,0,0
green = 0,255,0
black = 0,0,0
brown = 244,164,96
left = 82
right = 238
top = 58
bottom = 138
position = 0
axis = 0
numberOfFingers = 1
leftFingerName = []
leftFingerNumber = [1]
rightFingerName = []
rightFingerNumber = [3]

###################################################################
# initialze the screen, colors and clock
###################################################################
screen = pygame.display.set_mode(size)
screen.fill(green)
Clock = pygame.time.Clock()

pygame.draw.rect(screen, black, (10,10,300,220))
pygame.draw.rect(screen, brown, (left - 35,top - 35,70,70))

###################################################################
# initialze the icons in GUI
###################################################################
mouse = pygame.image.load("mouse.png")
mouserect = mouse.get_rect()
mouserect.center = (left,top)

puzzle = pygame.image.load("puzzle.jpg")
puzzlerect = puzzle.get_rect()
puzzlerect.center = (right,top)

custom = pygame.image.load("custom.png")
customrect = custom.get_rect()
customrect.center = ((left+right)/2,(top+bottom)/2)

threed = pygame.image.load("3d.jpg")
threedrect = threed.get_rect()
threedrect.center = (left,bottom)

fps = pygame.image.load("fps.png")
fpsrect = fps.get_rect()
fpsrect.center = (right,bottom)

my_font = pygame.font.Font(None,38)
my_buttons = {'QUIT':((left+right)/2,200)}
for my_text, text_pos in my_buttons.items():
        text_surface = my_font.render(my_text, True, white)
        text_rect = text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, text_rect)

screen.blit(mouse, mouserect)
screen.blit(fps, fpsrect)
screen.blit(puzzle, puzzlerect)
screen.blit(threed, threedrect)
screen.blit(custom, customrect)
pygame.display.update()

###################################################################
# setup I2C connections with sensors
###################################################################
def I2C_setup(i2c_channel_setup):
        global I2C_bus_number
        bus = smbus.SMBus(I2C_bus_number)
        bus.write_byte(I2C_address,i2c_channel_setup)

###################################################################
# Set the bluetooth config for python 2
###################################################################
if sys.version < '3':
        input = raw_input

###################################################################
# Get values from the sensor in the middle of the hand
###################################################################
while True:
	try:
		# Set address of sensors
		I2C_setup(mux_channel[4])
		sensor = mpu6050(0x68)
		break
	except(IOError):
		pass

###################################################################
# create arrays for averaging
###################################################################
x_gyro_avg_center = np.zeros(averaging)
y_gyro_avg_center = np.zeros(averaging)
z_gyro_avg_center = np.zeros(averaging)
x_rot_gyro_avg_center = np.zeros(averaging)
y_rot_gyro_avg_center = np.zeros(averaging)
z_rot_gyro_avg_center = np.zeros(averaging)

x_gyro_avg_index = np.zeros(averaging)
y_gyro_avg_index = np.zeros(averaging)
z_gyro_avg_index = np.zeros(averaging)
x_rot_gyro_avg_index = np.zeros(averaging)
y_rot_gyro_avg_index = np.zeros(averaging)
z_rot_gyro_avg_index = np.zeros(averaging)

x_gyro_avg_middle = np.zeros(averaging)
y_gyro_avg_middle = np.zeros(averaging)
z_gyro_avg_middle = np.zeros(averaging)
x_rot_gyro_avg_middle = np.zeros(averaging)
y_rot_gyro_avg_middle = np.zeros(averaging)
z_rot_gyro_avg_middle = np.zeros(averaging)

x_gyro_avg_ring = np.zeros(averaging)
y_gyro_avg_ring = np.zeros(averaging)
z_gyro_avg_ring = np.zeros(averaging)
x_rot_gyro_avg_ring = np.zeros(averaging)
y_rot_gyro_avg_ring = np.zeros(averaging)
z_rot_gyro_avg_ring = np.zeros(averaging)

x_gyro_avg_pinki = np.zeros(averaging)
y_gyro_avg_pinki = np.zeros(averaging)
z_gyro_avg_pinki = np.zeros(averaging)
x_rot_gyro_avg_pinki = np.zeros(averaging)
y_rot_gyro_avg_pinki = np.zeros(averaging)
z_rot_gyro_avg_pinki = np.zeros(averaging)

x_gyro_avg_thumb = np.zeros(averaging)
y_gyro_avg_thumb = np.zeros(averaging)
z_gyro_avg_thumb = np.zeros(averaging)
x_rot_gyro_avg_thumb = np.zeros(averaging)
y_rot_gyro_avg_thumb = np.zeros(averaging)
z_rot_gyro_avg_thumb = np.zeros(averaging)

centerClick = np.zeros(click_averaging)
indexClick = np.zeros(click_averaging)
middleClick = np.zeros(click_averaging)
ringClick = np.zeros(click_averaging)
pinkiClick = np.zeros(click_averaging)
thumbClick = np.zeros(click_averaging)

###################################################################
# See if the user has specified the address for bluetooth connection
###################################################################
if len(sys.argv) < 2:
        print("no device specified. Searching all nearby bluetooth devices for")
        print("the RatGlove service")
else:
        addr = sys.argv[1]
        if (addr == "Mac"):
                addr = "F4:0F:24:2A:0D:D7"
        print("Searching for RatGlove on %s" % addr)

###################################################################
# search for the SampleServer service
###################################################################
uuid = "12345678-1234-1234-1234-123456789012"
service_matches = find_service( uuid = uuid, address = addr )

if len(service_matches) == 0:
        print("couldn't find the RatGlove service =(")
        sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to \"%s\" on %s" % (name, host))

###################################################################
# Create the client socket
###################################################################
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))

###################################################################
# GPIO input connection for closing the glove
###################################################################
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
previous_Toggle = GPIO.input(6)

###################################################################
# Functions to calculate rotation and distance
###################################################################
def dist(a,b):
        return math.sqrt((a*a)+(b*b))

def get_x_rotation(x,y,z):
        radians = math.atan2(x,dist(y,z))
        return math.degrees(radians)

def get_y_rotation(x,y,z):
        radians = math.atan2(y, dist(x,z))
        return -math.degrees(radians)

def get_z_rotation(x,y,z):
        radians = math.atan2(z, dist(x,y))
        return math.degrees(radians)

###################################################################
# Get sensors values from a sensor specified by the channel number
###################################################################
def get_gyro_accel_values(count_avg, channel, x_rotation_gyro, y_rotation_gyro, z_rotation_gyro, x_gyro_avg, y_gyro_avg, z_gyro_avg, x_rot_gyro_avg, y_rot_gyro_avg, z_rot_gyro_avg):
	try:
		# Set address of sensors
		I2C_setup(mux_channel[channel])
		sensor = mpu6050(0x68)

        	gyrometer = sensor.get_gyro_data()
		x_gyro = gyrometer['x'] + 6.1
        	y_gyro = gyrometer['y'] - 1
        	z_gyro = gyrometer['z'] + 1
        	x_gyro_avg[count_avg] = x_gyro
        	y_gyro_avg[count_avg] = y_gyro
        	z_gyro_avg[count_avg] = z_gyro

        	x_rotation_gyro += x_gyro
        	y_rotation_gyro += y_gyro
        	z_rotation_gyro += z_gyro
        	x_rot_gyro_avg[count_avg] = x_rotation_gyro
        	y_rot_gyro_avg[count_avg] = y_rotation_gyro
        	z_rot_gyro_avg[count_avg] = z_rotation_gyro
	except(IOError):
		pass
        
	return x_rotation_gyro, y_rotation_gyro, z_rotation_gyro, x_rot_gyro_avg, y_rot_gyro_avg, z_rot_gyro_avg

###################################################################
# Function for normal mouse mode
###################################################################
def mouse_function(centerClickEvent, indexClickEvent, middleClickEvent, ringClickEvent, pinkiClickEvent, thumbClickEvent, y_send, x_send):
	speed = 3

	# Find which finger was moved
	if (indexClickEvent > 300):
                sock.send(str(5000) + "," + str(5000) + ",")
        elif (middleClickEvent > 300):
                sock.send(str(10000) + "," + str(10000) + ",")
        elif (ringClickEvent > 300):
                sock.send(str(15000) + "," + str(15000) + ",")
        elif (pinkiClickEvent > 300):
                sock.send(str(20000) + "," + str(20000) + ",")
        elif (thumbClickEvent > 300):
                sock.send(str(25000) + "," + str(25000) + ",")
        else:
                sock.send(str(y_send) + "," + str(x_send) + ",")

###################################################################
# Function for fps mode
###################################################################
def fps_function(centerClickEvent, indexClickEvent, middleClickEvent, ringClickEvent, pinkiClickEvent, thumbClickEvent, y_send, x_send):	
	speed = 2

        # Find if index finger was moved or not for shooting
	if (indexClickEvent > 300):
                sock.send(str(5000) + "," + str(5000) + ",")
        else:
                sock.send(str(y_send) + "," + str(x_send) + ",")

###################################################################
# Function for puzzle mode
###################################################################
def puzzle_function(centerClickEvent, indexClickEvent, middleClickEvent, ringClickEvent, pinkiClickEvent, thumbClickEvent, y_send, x_send):	
	speed = 2

        # Find which fingers are moved
	if (indexClickEvent > 300):
                sock.send(str(5000) + "," + str(5000) + ",")
        elif (middleClickEvent > 150 and ringClickEvent > 150 and pinkiClickEvent > 150 and thumbClickEvent > 150):
                sock.send(str(20000) + "," + str(20000) + ",")
        else:
                sock.send(str(y_send) + "," + str(x_send) + ",")
                
###################################################################
# Function for threed mode
###################################################################
def threed_function(centerClickEvent, indexClickEvent, middleClickEvent, ringClickEvent, pinkiClickEvent, thumbClickEvent, y_send, x_send):	
	speed = 3

        # Find which fingers are moved
	if (indexClickEvent > 300):
                sock.send(str(5000) + "," + str(5000) + ",")
        elif (middleClickEvent > 150 and ringClickEvent > 150 and pinkiClickEvent > 150 and thumbClickEvent > 150):
                sock.send(str(20000) + "," + str(20000) + ",")
        else:
                sock.send(str(y_send) + "," + str(x_send) + ",")

###################################################################
# Function for custom mode
###################################################################
def custom_function(centerClickEvent, indexClickEvent, middleClickEvent, ringClickEvent, pinkiClickEvent, thumbClickEvent, y_send, x_send):
	speed = 3
	leftThreshold = 300
	rightThreshold = 300
	global leftFingerName
        global leftFingerNumber
        global rightFingerName
        global rightFingerNumber

        # Set the threshold value for different finger movements
	if len(leftFingerNumber) == 1:
		leftThreshold = 300
	elif ((len(leftFingerNumber) == 2) or (len(leftFingerNumber) == 3)):
		leftThreshold = 200
	elif ((len(leftFingerNumber) == 4) or (len(leftFingerNumber) == 5)):
		leftThreshold = 150
	if len(rightFingerNumber) == 1:
		rightThreshold = 300
	elif ((len(rightFingerNumber) == 2) or (len(rightFingerNumber) == 3)):
		rightThreshold = 200
	elif ((len(rightFingerNumber) == 4) or (len(rightFingerNumber) == 5)):
		rightThreshold = 150

        # See what fingers are moved for left-click gesture
	leftCurrentArray = []	
	if (indexClickEvent > leftThreshold):
		leftCurrentArray.append(1)
	if (middleClickEvent > leftThreshold):
                leftCurrentArray.append(2)
	if (ringClickEvent > leftThreshold):
                leftCurrentArray.append(3)
	if (pinkiClickEvent > leftThreshold):
                leftCurrentArray.append(4)
	if (thumbClickEvent > leftThreshold):
                leftCurrentArray.append(5)

         # See what fingers are moved for right-click gesture
	rightCurrentArray = []	
	if (indexClickEvent > rightThreshold):
		rightCurrentArray.append(1)
	if (middleClickEvent > rightThreshold):
                rightCurrentArray.append(2)
	if (ringClickEvent > rightThreshold):
                rightCurrentArray.append(3)
	if (pinkiClickEvent > rightThreshold):
                rightCurrentArray.append(4)
	if (thumbClickEvent > rightThreshold):
                rightCurrentArray.append(5)

        # See if the gestures that were moved for left and right
        # were the ones that were set
	if (set(leftFingerNumber) == set(leftCurrentArray)):
                sock.send(str(5000) + "," + str(5000) + ",")
        elif (set(rightFingerNumber) == set(rightCurrentArray)):
                sock.send(str(15000) + "," + str(15000) + ",")
        else:
                sock.send(str(y_send) + "," + str(x_send) + ",")

###################################################################
# Find which finger was used for gestures
###################################################################
def find_Which_Fingers(numberOfFingers):
        # Set all the variables
	averaging = 10
	click_averaging = 10
	count_avg = 0
	count_click = 0
	threshold = 300

	if numberOfFingers == 1:
		threshold = 300
	elif ((numberOfFingers == 2) or (numberOfFingers == 3)):
		threshold = 200
	elif ((numberOfFingers == 4) or (numberOfFingers == 5)):
		threshold = 150

	indexOcc = False
	middleOcc = False
	ringOcc = False
	pinkiOcc = False
	thumbOcc = False

	FingerName = []
        FingerNumber = []
	x_rotation_gyro_center = 0
	y_rotation_gyro_center = 0
	z_rotation_gyro_center = 0
	x_rotation_gyro_index = 0
	y_rotation_gyro_index = 0
	z_rotation_gyro_index = 0
	x_rotation_gyro_middle = 0
	y_rotation_gyro_middle = 0
	z_rotation_gyro_middle = 0
	x_rotation_gyro_ring = 0
	y_rotation_gyro_ring = 0
	z_rotation_gyro_ring = 0
	x_rotation_gyro_pinki = 0
	y_rotation_gyro_pinki = 0
	z_rotation_gyro_pinki = 0
	x_rotation_gyro_thumb = 0
	y_rotation_gyro_thumb = 0
	z_rotation_gyro_thumb = 0

	# create an array for averaging
	x_gyro_avg_center = np.zeros(averaging)
	y_gyro_avg_center = np.zeros(averaging)
	z_gyro_avg_center = np.zeros(averaging)
	x_rot_gyro_avg_center = np.zeros(averaging)
	y_rot_gyro_avg_center = np.zeros(averaging)
	z_rot_gyro_avg_center = np.zeros(averaging)

	x_gyro_avg_index = np.zeros(averaging)
	y_gyro_avg_index = np.zeros(averaging)
	z_gyro_avg_index = np.zeros(averaging)
	x_rot_gyro_avg_index = np.zeros(averaging)
	y_rot_gyro_avg_index = np.zeros(averaging)
	z_rot_gyro_avg_index = np.zeros(averaging)

	x_gyro_avg_middle = np.zeros(averaging)
	y_gyro_avg_middle = np.zeros(averaging)
	z_gyro_avg_middle = np.zeros(averaging)
	x_rot_gyro_avg_middle = np.zeros(averaging)
	y_rot_gyro_avg_middle = np.zeros(averaging)
	z_rot_gyro_avg_middle = np.zeros(averaging)

	x_gyro_avg_ring = np.zeros(averaging)
	y_gyro_avg_ring = np.zeros(averaging)
	z_gyro_avg_ring = np.zeros(averaging)
	x_rot_gyro_avg_ring = np.zeros(averaging)
	y_rot_gyro_avg_ring = np.zeros(averaging)
	z_rot_gyro_avg_ring = np.zeros(averaging)

	x_gyro_avg_pinki = np.zeros(averaging)
	y_gyro_avg_pinki = np.zeros(averaging)
	z_gyro_avg_pinki = np.zeros(averaging)
	x_rot_gyro_avg_pinki = np.zeros(averaging)
	y_rot_gyro_avg_pinki = np.zeros(averaging)
	z_rot_gyro_avg_pinki = np.zeros(averaging)

	x_gyro_avg_thumb = np.zeros(averaging)
	y_gyro_avg_thumb = np.zeros(averaging)
	z_gyro_avg_thumb = np.zeros(averaging)
	x_rot_gyro_avg_thumb = np.zeros(averaging)
	y_rot_gyro_avg_thumb = np.zeros(averaging)
	z_rot_gyro_avg_thumb = np.zeros(averaging)

	centerClick = np.zeros(click_averaging)
	indexClick = np.zeros(click_averaging)
	middleClick = np.zeros(click_averaging)
	ringClick = np.zeros(click_averaging)
	pinkiClick = np.zeros(click_averaging)
	thumbClick = np.zeros(click_averaging)

        # Call the get_gyro_accel_values function for updating the array that contains
        # the movements of specific fingers
	while(numberOfFingers > 0):
		x_rotation_gyro_center, y_rotation_gyro_center, z_rotation_gyro_center,\
	 	x_rot_gyro_avg_center, y_rot_gyro_avg_center, z_rot_gyro_avg_center\
	 	= get_gyro_accel_values(count_avg, 4,\
	 	x_rotation_gyro_center, y_rotation_gyro_center, z_rotation_gyro_center,\
	 	x_gyro_avg_center, y_gyro_avg_center, z_gyro_avg_center,\
	 	x_rot_gyro_avg_center, y_rot_gyro_avg_center, z_rot_gyro_avg_center)
        
		x_rotation_gyro_index, y_rotation_gyro_index, z_rotation_gyro_index,\
	 	x_rot_gyro_avg_index, y_rot_gyro_avg_index, z_rot_gyro_avg_index\
	 	= get_gyro_accel_values(count_avg, 7,\
	 	x_rotation_gyro_index, y_rotation_gyro_index, z_rotation_gyro_index,\
	 	x_gyro_avg_index, y_gyro_avg_index, z_gyro_avg_index,\
	 	x_rot_gyro_avg_index, y_rot_gyro_avg_index, z_rot_gyro_avg_index)
        
		x_rotation_gyro_middle, y_rotation_gyro_middle, z_rotation_gyro_middle,\
	 	x_rot_gyro_avg_middle, y_rot_gyro_avg_middle, z_rot_gyro_avg_middle\
	 	= get_gyro_accel_values(count_avg, 6,\
	 	x_rotation_gyro_middle, y_rotation_gyro_middle, z_rotation_gyro_middle,\
	 	x_gyro_avg_middle, y_gyro_avg_middle, z_gyro_avg_middle,\
	 	x_rot_gyro_avg_middle, y_rot_gyro_avg_middle, z_rot_gyro_avg_middle)

		x_rotation_gyro_ring, y_rotation_gyro_ring, z_rotation_gyro_ring,\
	 	x_rot_gyro_avg_ring, y_rot_gyro_avg_ring, z_rot_gyro_avg_ring\
	 	= get_gyro_accel_values(count_avg, 2,\
	 	x_rotation_gyro_ring, y_rotation_gyro_ring, z_rotation_gyro_ring,\
	 	x_gyro_avg_ring, y_gyro_avg_ring, z_gyro_avg_ring,\
	 	x_rot_gyro_avg_ring, y_rot_gyro_avg_ring, z_rot_gyro_avg_ring)
	
		x_rotation_gyro_pinki, y_rotation_gyro_pinki, z_rotation_gyro_pinki,\
	 	x_rot_gyro_avg_pinki, y_rot_gyro_avg_pinki, z_rot_gyro_avg_pinki\
	 	= get_gyro_accel_values(count_avg, 3,\
	 	x_rotation_gyro_pinki, y_rotation_gyro_pinki, z_rotation_gyro_pinki,\
	 	x_gyro_avg_pinki, y_gyro_avg_pinki, z_gyro_avg_pinki,\
	 	x_rot_gyro_avg_pinki, y_rot_gyro_avg_pinki, z_rot_gyro_avg_pinki)
        
		x_rotation_gyro_thumb, y_rotation_gyro_thumb, z_rotation_gyro_thumb,\
	 	x_rot_gyro_avg_thumb, y_rot_gyro_avg_thumb, z_rot_gyro_avg_thumb\
	 	= get_gyro_accel_values(count_avg, 5,\
	 	x_rotation_gyro_thumb, y_rotation_gyro_thumb, z_rotation_gyro_thumb,\
	 	x_gyro_avg_thumb, y_gyro_avg_thumb, z_gyro_avg_thumb,\
	 	x_rot_gyro_avg_thumb, y_rot_gyro_avg_thumb, z_rot_gyro_avg_thumb)

		centerClick[count_click] = y_rotation_gyro_center - np.average(y_rot_gyro_avg_center)
		indexClick[count_click] = y_rotation_gyro_index - np.average(y_rot_gyro_avg_index)
		middleClick[count_click] = y_rotation_gyro_middle - np.average(y_rot_gyro_avg_middle)
		ringClick[count_click] = y_rotation_gyro_ring - np.average(y_rot_gyro_avg_ring)
		pinkiClick[count_click] = y_rotation_gyro_pinki - np.average(y_rot_gyro_avg_pinki)
		thumbClick[count_click] = y_rotation_gyro_thumb - np.average(y_rot_gyro_avg_thumb)
       
		centerClickEvent = y_rotation_gyro_center - np.average(y_rot_gyro_avg_center) - np.average(centerClick)
		indexClickEvent = y_rotation_gyro_index - np.average(y_rot_gyro_avg_index) - np.average(indexClick)
		middleClickEvent = y_rotation_gyro_middle - np.average(y_rot_gyro_avg_middle) - np.average(middleClick)
		ringClickEvent = y_rotation_gyro_ring - np.average(y_rot_gyro_avg_ring) - np.average(ringClick)
		pinkiClickEvent = y_rotation_gyro_pinki - np.average(y_rot_gyro_avg_pinki) - np.average(pinkiClick)
		thumbClickEvent = y_rotation_gyro_thumb - np.average(y_rot_gyro_avg_thumb) - np.average(thumbClick)
	
		indexClickEvent -= centerClickEvent
		middleClickEvent -= centerClickEvent
		ringClickEvent -= centerClickEvent
		pinkiClickEvent -= centerClickEvent
		thumbClickEvent -= centerClickEvent

                # If the specific finger was moved then save the finger number and name to an array
		if (indexClickEvent > threshold and indexOcc == False):
			FingerName.append("Index")
			FingerNumber.append(1)
			numberOfFingers -= 1
			indexOcc = True

		if (middleClickEvent > threshold and middleOcc == False):
			FingerName.append("Middle")
			FingerNumber.append(2)
			numberOfFingers -= 1
			middleOcc = True

		if (ringClickEvent > threshold and ringOcc == False):
			FingerName.append("Ring")
			FingerNumber.append(3)
			numberOfFingers -= 1
			ringOcc = True

		if (pinkiClickEvent > threshold and pinkiOcc == False):
			FingerName.append("Pinki")
			FingerNumber.append(4)
			numberOfFingers -= 1
			pinkiOcc = True

		if (thumbClickEvent > threshold and thumbOcc == False):
			FingerName.append("Thumb")
			FingerNumber.append(5)
			numberOfFingers -= 1
			thumbOcc = True

		count_avg += 1
	        count_click += 1
        	previous_Toggle = toggle_Position
        	if (count_avg > averaging-1):
                	count_avg = 0
        	if (count_click > click_averaging-1):
                	count_click = 0

	return FingerName, FingerNumber

###################################################################
# Function used for changing gestures using customizations
###################################################################
def change_Gestures():
	global leftFingerName
	global leftFingerNumber
	global rightFingerName
	global rightFingerNumber
	global axis

	leftFingerName = []
        leftFingerNumber = []
        rightFingerName = []
        rightFingerNumber = []

        # Setting the axis for operation of glove
	fail = False
	screen.fill(black)
	text1 = pygame.font.Font(None,18)
	text1_surface = text1.render('Please keep the glove in the normal position of gesture.', True, white)
	text2 = pygame.font.Font(None,18)
        text2_surface = text1.render('This will decide the axis in which your glove will operate.', True, white)
	text3 = pygame.font.Font(None,18)
        text3_surface = text1.render('After keeping the glove in desired position, press Next.', True, white)

	my_font = pygame.font.Font(None,38)
	my_buttons = {'Next':((left+right)/2,200)}
	for my_text, text_pos in my_buttons.items():
        	text_surface = my_font.render(my_text, True, white)
        	text_rect = text_surface.get_rect(center=text_pos)
        	screen.blit(text_surface, text_rect)

	screen.blit(text1_surface, (0, 50))
	screen.blit(text2_surface, (0, 70))
	screen.blit(text3_surface, (0, 90))
	pygame.display.update()

	while True:
		try:	
			# Set address of sensors
			I2C_setup(mux_channel[4])
        		sensor = mpu6050(0x68)
			break
		except(IOError):
			pass

	# Setting the left-click
	while (fail == False):
		try:
			accelerometer = sensor.get_accel_data()
		except(IOError):
			pass
		# check if any button has been pressed
	        for event in pygame.event.get():
        	        if (event.type is MOUSEBUTTONDOWN):
                	        pos = pygame.mouse.get_pos()
                	elif (event.type is MOUSEBUTTONUP):
                        	pos = pygame.mouse.get_pos()
                        	x,y = pos
				if (y > 190 and y < 210):
                                	if (x > (left+right)/2 - 32 and x < (left+right)/2 + 32):
						try:
							accelerometer = sensor.get_accel_data()
							x_accel_custom = accelerometer['x']
        						y_accel_custom = accelerometer['y']
        						z_accel_custom = accelerometer['z']
							if (abs(z_accel_custom)> abs(x_accel_custom) and abs(z_accel_custom) > abs(y_accel_custom)):
								axis = 0
								fail = True
							elif (abs(y_accel_custom) > abs(x_accel_custom) and abs(y_accel_custom) > abs(z_accel_custom)):
								axis = 1
								fail = True
						except(IOError):
							pass

	fail = False
	screen.fill(black)
	text1 = pygame.font.Font(None,18)
        text1_surface = text1.render('Select the gesture for Left-Click', True, white)
        text2 = pygame.font.Font(None,18)
        text2_surface = text1.render('How many fingers do you want to use for this gesture', True, white)
        my_font = pygame.font.Font(None,38)
        my_buttons = {'1':(50,200),'2':(100,200),'3':(150,200),'4':(200,200),'5':(250,200)}
        for my_text, text_pos in my_buttons.items():
                text_surface = my_font.render(my_text, True, white)
                text_rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, text_rect)
        screen.blit(text1_surface, (0, 50))
        screen.blit(text2_surface, (0, 70))
        pygame.display.update()

        # Setting the right-click
	while (fail == False):
		# check if any button has been pressed
	        for event in pygame.event.get():
        	        if (event.type is MOUSEBUTTONDOWN):
                	        pos = pygame.mouse.get_pos()
                	elif (event.type is MOUSEBUTTONUP):
                        	pos = pygame.mouse.get_pos()
                        	x,y = pos
				if (y > 180 and y < 220):
                                	if (x > 35  and x < 65):
						numberOfFingers = 1
						fail = True
					elif (x > 85  and x < 115):
						numberOfFingers = 2
						fail = True
					elif (x > 135  and x < 165):
						numberOfFingers = 3
						fail = True
					elif (x > 185  and x < 215):
						numberOfFingers = 4
						fail = True
					elif (x > 195  and x < 265):
						numberOfFingers = 5
						fail = True
	
	screen.fill(black)
        text1 = pygame.font.Font(None,18)
        text1_surface = text1.render('Do the gesture with ' + str(numberOfFingers) + ' fingers', True, white)
        text2 = pygame.font.Font(None,18)
        text2_surface = text1.render('These gestures will be used for left-click', True, white)
	text3 = pygame.font.Font(None,18)
        text3_surface = text1.render('Please keep the rest of your hand very still', True, white)
        screen.blit(text1_surface, (0, 50))
        screen.blit(text2_surface, (0, 70))
        pygame.display.update()

	leftFingerName, leftFingerNumber = find_Which_Fingers(numberOfFingers)
	position = 50
	screen.fill(black)
        text1 = pygame.font.Font(None,18)
        text1_surface = text1.render('The fingers selected for left-click gesture are:', True, white)
	screen.blit(text1_surface, (0, 10))
	for i,n in enumerate(leftFingerName):
		text_surface = my_font.render(n, True, white)
                screen.blit(text_surface, (0,position))
		position += 30
	pygame.display.update()
	time.sleep(5)

	fail = False
	screen.fill(black)
	text1 = pygame.font.Font(None,18)
        text1_surface = text1.render('Select the gesture for Right-Click', True, white)
        text2 = pygame.font.Font(None,18)
        text2_surface = text1.render('How many fingers do you want to use for this gesture', True, white)
        my_font = pygame.font.Font(None,38)
        my_buttons = {'1':(50,200),'2':(100,200),'3':(150,200),'4':(200,200),'5':(250,200)}
        for my_text, text_pos in my_buttons.items():
                text_surface = my_font.render(my_text, True, white)
                text_rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, text_rect)
        screen.blit(text1_surface, (0, 50))
        screen.blit(text2_surface, (0, 70))
        pygame.display.update()

	while (fail == False):
		# check if any button has been pressed
	        for event in pygame.event.get():
        	        if (event.type is MOUSEBUTTONDOWN):
                	        pos = pygame.mouse.get_pos()
                	elif (event.type is MOUSEBUTTONUP):
                        	pos = pygame.mouse.get_pos()
                        	x,y = pos
				if (y > 180 and y < 220):
                                	if (x > 35  and x < 65):
						numberOfFingers = 1
						fail = True
					elif (x > 85  and x < 115):
						numberOfFingers = 2
						fail = True
					elif (x > 135  and x < 165):
						numberOfFingers = 3
						fail = True
					elif (x > 185  and x < 215):
						numberOfFingers = 4
						fail = True
					elif (x > 195  and x < 265):
						numberOfFingers = 5
						fail = True

	fail = False
	screen.fill(black)
        text1 = pygame.font.Font(None,18)
        text1_surface = text1.render('Do the gesture with ' + str(numberOfFingers) + ' fingers', True, white)
        text2 = pygame.font.Font(None,18)
        text2_surface = text1.render('These gestures will be used for right-click', True, white)
	text3 = pygame.font.Font(None,18)
        text3_surface = text1.render('Please keep the rest of your hand very still', True, white)
        screen.blit(text1_surface, (0, 50))
        screen.blit(text2_surface, (0, 70))
        pygame.display.update()

	rightFingerName, rightFingerNumber = find_Which_Fingers(numberOfFingers)
	position = 50
	screen.fill(black)
        text1 = pygame.font.Font(None,18)
        text1_surface = text1.render('The fingers selected for right-click gesture are:', True, white)
	screen.blit(text1_surface, (0, 10))
	for i,n in enumerate(rightFingerName):
		text_surface = my_font.render(n, True, white)
                screen.blit(text_surface, (0,position))
		position += 30
	pygame.display.update()
	time.sleep(5)

	screen.fill(black)
        text1 = pygame.font.Font(None,30)
        text1_surface = text1.render('Congratulations...:D', True, white)
	text2 = pygame.font.Font(None,18)
        text2_surface = text1.render('Your Gestures are set', True, white)

	screen.blit(text1_surface, (0, 50))
        screen.blit(text2_surface, (0, 100))
        pygame.display.update()
	time.sleep(5)

	screen.fill(green)
	my_buttons = {'QUIT':((left+right)/2,200)}
	for my_text, text_pos in my_buttons.items():
        	text_surface = my_font.render(my_text, True, white)
        	text_rect = text_surface.get_rect(center=text_pos)
        	screen.blit(text_surface, text_rect)
	pygame.draw.rect(screen, black, (10,10,300,220))
	pygame.draw.rect(screen, brown, ((left+right)/2 - 35,(top+bottom)/2 - 35,70,70))
	screen.blit(mouse, mouserect)
	screen.blit(fps, fpsrect)
	screen.blit(puzzle, puzzlerect)
	screen.blit(threed, threedrect)
	screen.blit(custom, customrect)
	pygame.display.update()

###################################################################
# Always run until quit
###################################################################
while (True):
        # See if button for halting bluetooth is pressed
	toggle_Position = GPIO.input(6)
        if ( not GPIO.input(17)):
                print("Closing the Connection")
                break
	if (toggle_Position != previous_Toggle):
		if ( not toggle_Position):
                	paused = True
			screen.fill(red)
			pygame.draw.rect(screen, black, (10,10,300,220))
			if (position == 0):
				pygame.draw.rect(screen, brown, (left - 35,top - 35,70,70))
			elif (position == 1):
				pygame.draw.rect(screen, brown, (right - 35,top - 35,70,70))
			elif (position == 2):
				pygame.draw.rect(screen, brown, (right - 35,top - 35,70,70))
			elif (position == 3):
				pygame.draw.rect(screen, brown, (right - 35,bottom - 35,70,70))
			elif (position == 4):
				pygame.draw.rect(screen, brown, ((left+right)/2 - 35,(top+bottom)/2 - 35,70,70))
			screen.blit(mouse, mouserect)
			screen.blit(fps, fpsrect)
			screen.blit(puzzle, puzzlerect)
			screen.blit(threed, threedrect)
			screen.blit(custom, customrect)
			screen.blit(text_surface, text_rect)
			pygame.display.update()

		elif (toggle_Position):
                	paused = False
                	screen.fill(green)
			pygame.draw.rect(screen, black, (10,10,300,220))
			if (position == 0):
				pygame.draw.rect(screen, brown, (left - 35,top - 35,70,70))
			elif (position == 1):
				pygame.draw.rect(screen, brown, (right - 35,top - 35,70,70))
			elif (position == 2):
				pygame.draw.rect(screen, brown, (right - 35,top - 35,70,70))
			elif (position == 3):
				pygame.draw.rect(screen, brown, (right - 35,bottom - 35,70,70))
			elif (position == 4):
				pygame.draw.rect(screen, brown, ((left+right)/2 - 35,(top+bottom)/2 - 35,70,70))
			screen.blit(mouse, mouserect)
			screen.blit(fps, fpsrect)
			screen.blit(puzzle, puzzlerect)
			screen.blit(threed, threedrect)
			screen.blit(custom, customrect)
			screen.blit(text_surface, text_rect)
			pygame.display.update()

	
	# check if any button has been pressed on the GUI
        for event in pygame.event.get():
                if (event.type is MOUSEBUTTONDOWN):
                        pos = pygame.mouse.get_pos()
                elif (event.type is MOUSEBUTTONUP):
                        pos = pygame.mouse.get_pos()
                        x,y = pos
                        if (y > top - 32 and y < top + 32):
                                if (x > left - 32 and x < left + 32):
					mouseSelected = True
					fpsSelected = False
					puzzleSelected = False
					threedSelected = False
					customSelected = False
				
					pygame.draw.rect(screen, black, (10,10,300,220))
					pygame.draw.rect(screen, brown, (left - 35,top - 35,70,70))
					position = 0
				elif (x > right - 32 and x < right + 32):
					mouseSelected = False
					fpsSelected = False
					puzzleSelected = True
					threedSelected = False
					customSelected = False
		
					pygame.draw.rect(screen, black, (10,10,300,220))
					pygame.draw.rect(screen, brown, (right - 35,top - 35,70,70))
					position = 1
                        if (y > bottom - 32 and y < bottom + 32):
                                if (x > left - 32 and x < left + 32):
                                        mouseSelected = False
					fpsSelected = False
					puzzleSelected = False
					threedSelected = True
					customSelected = False
		
					pygame.draw.rect(screen, black, (10,10,300,220))
					pygame.draw.rect(screen, brown, (left - 35,bottom - 35,70,70))
					position = 2
				elif (x > right - 32 and x < right + 32):
					mouseSelected = False
					fpsSelected = True
					puzzleSelected = False
					threedSelected = False
					customSelected = False
		
					pygame.draw.rect(screen, black, (10,10,300,220))
					pygame.draw.rect(screen, brown, (right - 35,bottom - 35,70,70))
					position = 3
			if (y > 66 and y < 130):
                                if (x > 128 and x < 192 and customSelected == False):
                                        mouseSelected = False 
                                        fpsSelected = False
                                        puzzleSelect = False
                                        threedSelected = False
                                        customSelected = True
					
					pygame.draw.rect(screen, black, (10,10,300,220))
					pygame.draw.rect(screen, brown, ((left+right)/2 - 35,(top+bottom)/2 - 35,70,70))
					position = 4
				elif (x > 128 and x < 192 and customSelected == True):
					change_Gestures()
					
                        # If quit is pressed then exit
			if (y > 190 and y < 210):
				if (x > (left+right)/2 - 32 and x < (left+right)/2 + 32):
					print("Closing the Connection")
					sock.close()
					GPIO.cleanup()
					exit()
			screen.blit(mouse, mouserect)
        		screen.blit(fps, fpsrect)
        		screen.blit(puzzle, puzzlerect)
        		screen.blit(threed, threedrect)
        		screen.blit(custom, customrect)
        		screen.blit(text_surface, text_rect)
        		pygame.display.update()

        # Call the get_gyro_accel_values for updating the array with values of the sensors
	x_rotation_gyro_center, y_rotation_gyro_center, z_rotation_gyro_center,\
	 x_rot_gyro_avg_center, y_rot_gyro_avg_center, z_rot_gyro_avg_center\
	 = get_gyro_accel_values(count_avg, 4,\
	 x_rotation_gyro_center, y_rotation_gyro_center, z_rotation_gyro_center,\
	 x_gyro_avg_center, y_gyro_avg_center, z_gyro_avg_center,\
	 x_rot_gyro_avg_center, y_rot_gyro_avg_center, z_rot_gyro_avg_center)
        
	x_rotation_gyro_index, y_rotation_gyro_index, z_rotation_gyro_index,\
	 x_rot_gyro_avg_index, y_rot_gyro_avg_index, z_rot_gyro_avg_index\
	 = get_gyro_accel_values(count_avg, 7,\
	 x_rotation_gyro_index, y_rotation_gyro_index, z_rotation_gyro_index,\
	 x_gyro_avg_index, y_gyro_avg_index, z_gyro_avg_index,\
	 x_rot_gyro_avg_index, y_rot_gyro_avg_index, z_rot_gyro_avg_index)
        
	x_rotation_gyro_middle, y_rotation_gyro_middle, z_rotation_gyro_middle,\
	 x_rot_gyro_avg_middle, y_rot_gyro_avg_middle, z_rot_gyro_avg_middle\
	 = get_gyro_accel_values(count_avg, 6,\
	 x_rotation_gyro_middle, y_rotation_gyro_middle, z_rotation_gyro_middle,\
	 x_gyro_avg_middle, y_gyro_avg_middle, z_gyro_avg_middle,\
	 x_rot_gyro_avg_middle, y_rot_gyro_avg_middle, z_rot_gyro_avg_middle)

	x_rotation_gyro_ring, y_rotation_gyro_ring, z_rotation_gyro_ring,\
	 x_rot_gyro_avg_ring, y_rot_gyro_avg_ring, z_rot_gyro_avg_ring\
	 = get_gyro_accel_values(count_avg, 2,\
	 x_rotation_gyro_ring, y_rotation_gyro_ring, z_rotation_gyro_ring,\
	 x_gyro_avg_ring, y_gyro_avg_ring, z_gyro_avg_ring,\
	 x_rot_gyro_avg_ring, y_rot_gyro_avg_ring, z_rot_gyro_avg_ring)
	
	x_rotation_gyro_pinki, y_rotation_gyro_pinki, z_rotation_gyro_pinki,\
	 x_rot_gyro_avg_pinki, y_rot_gyro_avg_pinki, z_rot_gyro_avg_pinki\
	 = get_gyro_accel_values(count_avg, 3,\
	 x_rotation_gyro_pinki, y_rotation_gyro_pinki, z_rotation_gyro_pinki,\
	 x_gyro_avg_pinki, y_gyro_avg_pinki, z_gyro_avg_pinki,\
	 x_rot_gyro_avg_pinki, y_rot_gyro_avg_pinki, z_rot_gyro_avg_pinki)
        
	x_rotation_gyro_thumb, y_rotation_gyro_thumb, z_rotation_gyro_thumb,\
	 x_rot_gyro_avg_thumb, y_rot_gyro_avg_thumb, z_rot_gyro_avg_thumb\
	 = get_gyro_accel_values(count_avg, 5,\
	 x_rotation_gyro_thumb, y_rotation_gyro_thumb, z_rotation_gyro_thumb,\
	 x_gyro_avg_thumb, y_gyro_avg_thumb, z_gyro_avg_thumb,\
	 x_rot_gyro_avg_thumb, y_rot_gyro_avg_thumb, z_rot_gyro_avg_thumb)

        # Find if any finger was moved
	centerClick[count_click] = y_rotation_gyro_center - np.average(y_rot_gyro_avg_center)
	indexClick[count_click] = y_rotation_gyro_index - np.average(y_rot_gyro_avg_index)
	middleClick[count_click] = y_rotation_gyro_middle - np.average(y_rot_gyro_avg_middle)
	ringClick[count_click] = y_rotation_gyro_ring - np.average(y_rot_gyro_avg_ring)
	pinkiClick[count_click] = y_rotation_gyro_pinki - np.average(y_rot_gyro_avg_pinki)
	thumbClick[count_click] = y_rotation_gyro_thumb - np.average(y_rot_gyro_avg_thumb)
       
	centerClickEvent = y_rotation_gyro_center - np.average(y_rot_gyro_avg_center) - np.average(centerClick)
	indexClickEvent = y_rotation_gyro_index - np.average(y_rot_gyro_avg_index) - np.average(indexClick)
	middleClickEvent = y_rotation_gyro_middle - np.average(y_rot_gyro_avg_middle) - np.average(middleClick)
	ringClickEvent = y_rotation_gyro_ring - np.average(y_rot_gyro_avg_ring) - np.average(ringClick)
	pinkiClickEvent = y_rotation_gyro_pinki - np.average(y_rot_gyro_avg_pinki) - np.average(pinkiClick)
	thumbClickEvent = y_rotation_gyro_thumb - np.average(y_rot_gyro_avg_thumb) - np.average(thumbClick)
	
	indexClickEvent -= centerClickEvent
	middleClickEvent -= centerClickEvent
	ringClickEvent -= centerClickEvent
	pinkiClickEvent -= centerClickEvent
	thumbClickEvent -= centerClickEvent

        # Depending on the mode selected , call different functions for sending bluetooth information
	if(mouseSelected and paused == False):
		x_send = -round(((z_rotation_gyro_center-np.average(z_rot_gyro_avg_center))/speed),2)
        	y_send = -round(((y_rotation_gyro_center-np.average(y_rot_gyro_avg_center))/speed),2)

		mouse_function(centerClickEvent, indexClickEvent, middleClickEvent,\
		 ringClickEvent, pinkiClickEvent, thumbClickEvent, y_send, x_send)	
	
	elif(fpsSelected and paused == False):
		x_send = round(((y_rotation_gyro_center-np.average(y_rot_gyro_avg_center))/speed),2)
	        y_send = -round(((z_rotation_gyro_center-np.average(z_rot_gyro_avg_center))/speed),2)
	
		fps_function(centerClickEvent, indexClickEvent, middleClickEvent,\
		 ringClickEvent, pinkiClickEvent, thumbClickEvent, y_send, x_send)	
	
	elif(puzzleSelected and paused == False):
		x_send = -round(((z_rotation_gyro_center-np.average(z_rot_gyro_avg_center))/speed),2)
        	y_send = -round(((y_rotation_gyro_center-np.average(y_rot_gyro_avg_center))/speed),2)
		
		puzzle_function(centerClickEvent, indexClickEvent, middleClickEvent,\
		 ringClickEvent, pinkiClickEvent, thumbClickEvent, y_send, x_send)	
	
	elif(threedSelected and paused == False):
		x_send = -round(((z_rotation_gyro_center-np.average(z_rot_gyro_avg_center))/speed),2)
        	y_send = -round(((y_rotation_gyro_center-np.average(y_rot_gyro_avg_center))/speed),2)
		
		threed_function(centerClickEvent, indexClickEvent, middleClickEvent,\
		 ringClickEvent, pinkiClickEvent, thumbClickEvent, y_send, x_send)	

	elif(customSelected and paused == False):
		if (axis == 0):
			x_send = -round(((z_rotation_gyro_center-np.average(z_rot_gyro_avg_center))/speed),2)
        		y_send = -round(((y_rotation_gyro_center-np.average(y_rot_gyro_avg_center))/speed),2)
		elif (axis == 1):
			x_send = round(((y_rotation_gyro_center-np.average(y_rot_gyro_avg_center))/speed),2)
	                y_send = -round(((z_rotation_gyro_center-np.average(z_rot_gyro_avg_center))/speed),2)
		
		custom_function(centerClickEvent, indexClickEvent, middleClickEvent,\
                 ringClickEvent, pinkiClickEvent, thumbClickEvent, y_send, x_send)

	# Upadate the counter for arrays
        count_avg += 1
	count_click += 1
	previous_Toggle = toggle_Position
        if (count_avg > averaging-1):
                count_avg = 0
	if (count_click > click_averaging-1):
                count_click = 0

# End the program, close bluetooth connection and close teh GPIO connections	
sock.close()
GPIO.cleanup()
exit()

