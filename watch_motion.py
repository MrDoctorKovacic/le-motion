import RPi.GPIO as GPIO
import time
import os
import imp
fade = imp.load_source('fade', '/home/pi/le/lighting/fade.py')
from datetime import datetime

lights_set = 0
GPIO.setmode(GPIO.BCM)
PIR_PIN = 27
GPIO.setup(PIR_PIN, GPIO.IN)

def fadeLightsIn(brightness = 150):
        fade.main(['room_light1', 50])

def fadeLightsOut():
        fade.main(['default'])

def MOTION(PIR_PIN):
        global lights_set
        lights_on_time = 18
        lights_off_time = 9
        
	print "Motion Detected!"
        
	current_hour = datetime.now().hour

	if(current_hour > lights_on_time or current_hour < lights_off_time):
                if not lights_set:
                        try:
                                if current_hour < lights_off_time-4 or lights_on_time+4 > current_hour:
                                        lights_fade_brightness = 30
                                else:
                                        lights_fade_brightness = 150
                                fadeLightsIn(lights_fade_brightness)
                        except:
                                print("Error fading lights in")
                if lights_set <= 20:
                        lights_set += 3
	#start_time = time.time()
        #elapsed_time = time.time() - start_time

def watchMotion():
        global lights_set

        fadeLightsOut()
        
	try:
		GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=MOTION)
        	while 1:
                        print("Light timer is {}".format(lights_set))
                        if lights_set > 1:
                                lights_set -= 1
                        elif lights_set == 1:
                                fadeLightsOut()
                                lights_set = 0
			time.sleep(2)
        except KeyboardInterrupt:
                print "Quit"
                GPIO.cleanup()
	#except:
	#	print "Error getting pin data"
	#	GPIO.cleanup()
		
if __name__ == "__main__":
	watchMotion()
	start_time = time.time()

