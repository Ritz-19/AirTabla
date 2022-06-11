#Virtual Tabla
'''This project use Open CV to create a virtual Tabla set (Tabla + Base Drum). It uses color detection in a region of interest
and plays the corresponding Tabla bol (Sound that Tabla Makes). The tablas are shown in the video output and hitting them
with a red object would make you able to virtually play it.'''

# Importing the necessary libraries
import numpy as np
import time
import cv2
from pygame import mixer

# This function plays the corresponding Tabla bol if a red color object is detected in the region
def play_bol(detected,sound): 

	# Checks if the detected red color is greater that a preset value
	play = (detected) > tabla_thickness[0]*tabla_thickness[1]*0.8  

	# If it is detected play the corresponding Tabla bol
	if play and sound==1:   								   
		tabla_2.play()
		time.sleep(0.1)
	elif play and sound==2:
		tabla_1.play()
		time.sleep(0.1)


# This function is used to check if red color is present in the small region
def detect_in_region(frame,sound):
    	
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Converting to HSV
	mask = cv2.inRange(hsv, redLower, redUpper)  # Creating mask
	detected = np.sum(mask)						 # Calculating the number of red pixels
	
	# Call the function to play the Tabla bol
	play_bol(detected,sound)

	return mask

# A flag variable to choose whether to show the region that is being detected
verbose = False

# Importing Tabla bols
mixer.init()
tabla_1 = mixer.Sound('./sounds/Tabla_Sounds/Na.wav')
tabla_2 = mixer.Sound('./sounds/Drum_Sounds/Ghe.wav')

# Set HSV (Hue, Saturation. Brightness) range for detecting red color 
redLower = (161,155,84)
redUpper = (179,255,255)

# Obtain input from the webcam 
camera = cv2.VideoCapture(0)
ret,frame = camera.read()
H,W = frame.shape[:2]

kernel = np.ones((7,7),np.uint8)

# Read the image of the two Tablas
tabla1 = cv2.resize(cv2.imread('./images/Tabla1.png'),(200,200),interpolation=cv2.INTER_CUBIC)
tabla2 = cv2.resize(cv2.imread('./images/Tabla2.png'),(200,200),interpolation=cv2.INTER_CUBIC)


# Set the region area for detecting red color 
tabla1_center = [np.shape(frame)[1]*2//8,np.shape(frame)[0]*6//8]
tabla2_center = [np.shape(frame)[1]*6//8,np.shape(frame)[0]*6//8]

tabla_thickness = [200,200]
tabla1_top = [tabla1_center[0]-tabla_thickness[0]//2,tabla1_center[1]-tabla_thickness[1]//2]
tabla1_btm = [tabla1_center[0]+tabla_thickness[0]//2,tabla1_center[1]+tabla_thickness[1]//2]

tabla2_thickness = [200,200]
tabla2_top = [tabla2_center[0]-tabla2_thickness[0]//2,tabla2_center[1]-tabla2_thickness[1]//2]
tabla2_btm = [tabla2_center[0]+tabla2_thickness[0]//2,tabla2_center[1]+tabla2_thickness[1]//2]

time.sleep(1)

while True:
	
	# Select the current frame
	ret, frame = camera.read()
	frame = cv2.flip(frame,1)

	if not(ret):
	    break
    
	# Select region corresponding to Tabla 2
	tabla2_region = np.copy(frame[tabla2_top[1]:tabla2_btm[1],tabla2_top[0]:tabla2_btm[0]])
	mask = detect_in_region(tabla2_region,1)

	# Select region corresponding to Tabla 1
	tabla1_region = np.copy(frame[tabla1_top[1]:tabla1_btm[1],tabla1_top[0]:tabla1_btm[0]])
	mask = detect_in_region(tabla1_region,2)

	# Output project title
	cv2.putText(frame,'SM2702 Project 2 - Tabla',(10,30),2,1,(20,20,20),2)
    
	# If flag is selected, display the region under detection
	if verbose:
		frame[tabla2_top[1]:tabla2_btm[1],tabla2_top[0]:tabla2_btm[0]] = cv2.bitwise_and(frame[tabla2_top[1]:tabla2_btm[1],tabla2_top[0]:tabla2_btm[0]],frame[tabla2_top[1]:tabla2_btm[1],tabla2_top[0]:tabla2_btm[0]], mask=mask[tabla2_top[1]:tabla2_btm[1],tabla2_top[0]:tabla2_btm[0]])
		frame[tabla1_top[1]:tabla1_btm[1],tabla1_top[0]:tabla1_btm[0]] = cv2.bitwise_and(frame[tabla1_top[1]:tabla1_btm[1],tabla1_top[0]:tabla1_btm[0]],frame[tabla1_top[1]:tabla1_btm[1],tabla1_top[0]:tabla1_btm[0]],mask=mask[tabla1_top[1]:tabla1_btm[1],tabla1_top[0]:tabla1_btm[0]])
    
	# If flag is not selected, display the Tablas
	else:
		frame[tabla2_top[1]:tabla2_btm[1],tabla2_top[0]:tabla2_btm[0]] = cv2.addWeighted(tabla2, 1, frame[tabla2_top[1]:tabla2_btm[1],tabla2_top[0]:tabla2_btm[0]], 1, 0)
		frame[tabla1_top[1]:tabla1_btm[1],tabla1_top[0]:tabla1_btm[0]] = cv2.addWeighted(tabla1, 1, frame[tabla1_top[1]:tabla1_btm[1],tabla1_top[0]:tabla1_btm[0]], 1, 0)
    
    
	cv2.imshow('Output',frame)
	key = cv2.waitKey(1) & 0xFF
	
	# 'Q' to exit
	if key == ord("q"):
		break
 
# Clean up the open windows
camera.release()
cv2.destroyAllWindows()