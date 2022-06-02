#call this file's main fuction to run IMU gamemode
#accepts roll number as input agrument for main()

from cmath import rect
import numpy as np
import csv
import sys
import time
import math
import datetime
import os
import paho.mqtt.client as mqtt
import time,logging
import pygame


#print statements are still in this code

ans_str = ''      #empty string for returned answers
xang=[0] * 100   #sets array to 100 zeroes (this is due to not wanting to trigger break statement when there are only three elements in array)

arrow = pygame.image.load("Archive/white-arrow.png")
up = pygame.transform.scale(arrow, (100, 200))
down = pygame.transform.flip(up, False, True)
images = {'^': up, 'v': down}

def on_connect(client, userdata, flags, rc):
  print('connected')
  client.subscribe("ece180d/IMU", qos=1)



def on_message(client, userdata, message):
	global xang
	message_string = str(message.payload.decode("utf-8"))  #changes input from bytes to string and cleans up for reading into array
	disallowed_characters = "'"
	for character in disallowed_characters:
		message_string = message_string.replace(character, "") #removes characters from the payload before converting to array
	disallowed_characters = '"'
	for character in disallowed_characters:
		message_string = message_string.replace(character, "")
	disallowed_characters = '['
	for character in disallowed_characters:
		message_string = message_string.replace(character, "")
	disallowed_characters = ']'
	for character in disallowed_characters:
		message_string = message_string.replace(character, "")
	disallowed_characters = '('
	for character in disallowed_characters:
		message_string = message_string.replace(character, "")
	disallowed_characters = ')'
	for character in disallowed_characters:
		message_string = message_string.replace(character, "")
	disallowed_characters = ' '
	for character in disallowed_characters:
		message_string = message_string.replace(character, "")

	message_int = float(message_string)   #makes payload into float

	xang.append(message_int)   #adds most recent IMU reading to array
	#print(message_int)

pygame.font.init()
font = pygame.font.SysFont('comicsansms', 48)

def main(WIN, roll_num):   #accepts roll number as arguement

	client = mqtt.Client('hopefullythisisauniqueclientname12345678901234567890123')  #client name is irrelevant
	client.on_connect = on_connect
	client.on_message = on_message

	#print('running')


	global xang
	global ans_str
	count = 1
	ans = ''

	while count <= roll_num:
		WIN.fill((0,0,0))
		msg = "Reset hand to neutral position."
		text = font.render(msg, False, (255,255,255))
		rect = text.get_rect(center = (1400/2, 800/2))
		WIN.blit(text, rect)
		pygame.display.update()
		print('reset hand to neutral position')

		time.sleep(3)				#wait three seconds at start and before going again (can be changed as needed)
		WIN.fill((0,0,0))
		msg = "Start moving hand."
		text = font.render(msg, False, (255,255,255))
		rect = text.get_rect(center = (1400/2, 800/2))
		WIN.blit(text, rect)
		pygame.display.update()
		print('start moving hand')

		#timeout = 100         							 #only needed if using runtime errors
		#timeout_start = time.time()


		client.connect_async('test.mosquitto.org')    #start recording IMU data 
		client.loop_start()


		while True:  #will run until motion is detected (or timeout error if enabled)
			mean = np.nanmean(xang[-100:])
			print(mean)												#this print statement slows down the code to the point that these threshold values are accurate. if you remove it you will need to chnage the values as well
			if mean<-3:  #averages last 100 elements of array
				ans = '^'
				break
			if mean>3:  #averages last 100 elements of array
				ans = 'v'
				break
			#if time.time() > timeout+timeout_start							#only needed if using runtime errors		
				#ans = '>'
				#break


		client.loop_stop()			#stop recording IMU data
		client.disconnect()


		ans_str += ans

		im = images[ans]
		WIN.fill((0,0,0))
		WIN.blit(im, im.get_rect(center = (700, 400)))
		pygame.display.update()
		pygame.time.delay(1000)
		print('answer was ' + ans)

		xang.clear()       #clear the queue of past data
		xang = [0] * 100   #resets array to 100 zeroes

		count=count+1   #increment count for next motion


	print('all answers are ' + ans_str)
	return ans_str    #returns string of answers in form of (vv^v^^)
	

#main(6)   #for testing purposes






