# @Author: sai.ravuru
# @Date:   2019-12-10T15:23:26-08:00
# @Last modified by:   sai.ravuru
# @Last modified time: 2019-12-10T15:48:12-08:00



import paho.mqtt.client as mqtt
from ibm_botocore.client import Config
import ibm_boto3
import cv2

# This is the Subscriber
#hostname
broker="172.17.0.1"

#port
port=1883

#time to live
timelive=60

credentials = {
    'IBM_API_KEY_ID': '9OvePRwCnNV1g7RvK69WRXXwv43zViGgSk-_JiIZejnF',
    'IAM_SERVICE_ID': 'w251-sr',
    'ENDPOINT': 's3.us.cloud-object-storage.appdomain.cloud',
    'IBM_AUTH_ENDPOINT': '',
    'BUCKET': 'w251-sr'
}

try:
	cos = ibm_boto3.client(service_name='s3', \
	    ibm_api_key_id=credentials['IBM_API_KEY_ID'], \
	    ibm_service_instance_id=credentials['IAM_SERVICE_ID'], \
	    ibm_auth_endpoint=credentials['IBM_AUTH_ENDPOINT'], \
	    config=Config(signature_version='oauth'), \
	    endpoint_url=credentials['ENDPOINT'])
except:
	print('Cannot connect to IBM COS!')


def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("topic/dream_catcher")

def on_message(client, userdata, msg):
	try:
		print("message received!")
		nparr = np.fromstring(msg.payload.decode(), np.uint8)
		img_np = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)

		#cos.upload_fileobj(img_np,  credentials['BUCKET'], 'face-' + str(i) + '.jpg')
		#cos.upload_fileobj(<html file>,  credentials['BUCKET'], 'face-' + str(i) + '.jpg')
		#URL: https://s3.us.cloud-object-storage.appdomain.cloud/w251-sr

		# if we wanted to re-publish this message, something like this should work
		#msg = msg.payload
		#remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0, retain=False)
	except:
		print("Unexpected error:", sys.exc_info()[0])



client = mqtt.Client()
client.connect(broker,port,timelive)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
