from firebase import firebase
import RPi.GPIO as GPIO 
import plivo

from time import sleep     # this lets us have a time delay (see line 15)  
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(25, GPIO.IN)    # set GPIO25 as input (button)  
GPIO.setup(24, GPIO.OUT)

#plivo setup

srcPhoneNo="<mobile number>"	#phone number associated with your account
dstPhoneNo="<mobile number>"			#phone number where you want to send sms
smsText= u"leds glow"		#message which you want to send

msgObj={ 'src': srcPhoneNo, 'dst': dstPhoneNo, 'text': smsText}

#get auth_id and auth_token from plivo console
auth_id="<id>"
#auth_id key which you will get on plivio app
auth_token="<token>"
#auth_token which you will get on plivio app
pSMS = plivo.RestAPI(auth_id, auth_token)

#firebase setup

firebaseURL='< your firebase link>'
fBase = firebase.FirebaseApplication(firebaseURL, None)

gasleakOn=False;


def gasLeakDetected():
	print(fBase.put('/data/user_1/',"gasleakage","1"))
	print(pSMS.send_message(msgObj))
	gasleakOn=True

def gasLeakBlured():
	if(fBase.get('/data/user_1/','gasleakage')=="1") :
		print(fBase.put('/data/user_1/',"gasleakage","0"))
		gasleakOn=False


try:  
    while True:              
        if GPIO.input(25):   
            print ("Port 25 is 1/HIGH/True - LED ON")  
            GPIO.output(24, 1)
            gasLeakDetected()
            #result=firebase.put('/data/','user_1',{'gasleakage':'1'})   
        else:  
            print ("Port 25 is 0/LOW/False - LED OFF")  
            GPIO.output(24, 0)         # set port/pin value to 0/LOW/False  
        sleep(0.1)         
  
finally:                    
    GPIO.cleanup()         
