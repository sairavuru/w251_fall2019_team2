# @Author: sai.ravuru
# @Date:   2019-12-08T23:00:30-08:00
# @Last modified by:   sai.ravuru
# @Last modified time: 2019-12-10T15:20:09-08:00



## Captures face photo when eyes are closed and publishes it to the MQTT broker
## Press 'esc' to exit
## use 'docker cp photo_capture:/photos/sleepy_driver.png  .' to copy photo capture to local host
## mqtt service sends the photo to topic/dream_catcher running on 'iot-broker' container.

import numpy as np
import pandas as pd
import cv2
import base64
import paho.mqtt.client as mqtt
from datetime import datetime
import gps_simulator

## use external camera
cap = cv2.VideoCapture(1)

# cascade classifier:
eye_cascade_path = "/usr/share/opencv/haarcascades/haarcascade_eye_tree_eyeglasses.xml"
face_cascade_path = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"

face_cascade = cv2.CascadeClassifier(face_cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

driver_sleeping = False

#Read in simulated GPS logs
gps_df = pd.read_csv('gps_logs.csv')
gps_df.loc[:, 'Datetime'] = gps_df['Datetime'].apply(pd.to_datetime)
pic_count = 0

# Speed
#import random
#speed = random.randint(0,200)
speed = int(gps_df.loc[pic_count, 'mph'])



while(True):
	ret, frame = cap.read();
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray_face = gray
	# Detect Faces

	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
	cv2.imshow('Driver Camera',gray)

	for (x,y,h,w) in faces:
		gray_face = gray[y:y+h,x:x+w]

	# if a face is detected, search for eyes:
	if len(faces)>0:
		eyes = eye_cascade.detectMultiScale(gray_face, scaleFactor = 1.05, minNeighbors = 10)

#		Not in use, used to test cascade parameters
#		for (x,y,h,w) in eyes:
#			xc = x + w/2
#			yc = y + h/2
#			radius = min(h,w)/2
#			cv2.circle(gray_face, (int(xc), int(yc)), int(radius), (255,0,0), 1)

		# Are the eyes closed, len(eyes) == 0 if eyes could not be detected on the face
		if len(eyes) == 0:
			# Warning message
			cv2.putText(gray_face, "DRIVER SLEEPING!", (int(0.05*gray_face.shape[1]),int(0.1*gray_face.shape[0])), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0), 1, cv2.LINE_AA)
			# Time Stamp
			#time_stamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
			time_stamp = gps_df.loc[pic_count, 'Datetime'].strftime("%m/%d/%Y, %H:%M:%S")
			cv2.putText(gray_face, "UTC Time: " + str(time_stamp), (int(0.05*gray_face.shape[1]),int(0.15*gray_face.shape[0])), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255,0,0), 1, cv2.LINE_AA)

			# Speed and Location
			cv2.putText(gray_face, "Speed " + str(speed) + " mph", (int(0.05*gray_face.shape[1]),int(0.85*gray_face.shape[0])), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 1, cv2.LINE_AA)


			driver_sleeping = True
			pic_filename = 'sleepy_driver_{}.png'.format(pic_count)
			gps_df.loc[pic_count, 'Image'] = pic_filename
			cv2.imwrite(pic_filename,gray_face)
			pic_count += 1

			# Send to IoT Broker
			msg = cv2.imencode('.jpg',gray_face)[1]
			msg_out = base64.b64encode(msg)
			client = mqtt.Client()
			client.connect("iot-broker",1883,60)
			client.publish("topic/dream_catcher", msg_out)
			client.disconnect()



	k = cv2.waitKey(1)
	if k==27:
		break

gps_simulator() #Run GPS simulation
cv2.destroyAllWindows()
