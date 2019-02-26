#Import Libraries we will be using
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os
import sqlite3 as mydb

#Assign GPIO pins
redPin = 27
tempPin = 17
buttonPin = 26

#Temp and Humidity Sensor
tempSensor = Adafruit_DHT.DHT11

#LED Variables--------------------------------------------------------
#Duration of each Blink
blinkDur = .1
#Number of times to Blink the LED
blinkTime = 7
#---------------------------------------------------------------------

#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

con = sqlite3.connect('/home/bryan/tempData.db')

def oneBlink(pin):
    GPIO.output(pin,True)
    time.sleep(blinkDur)
    GPIO.output(pin,False)
    time.sleep(blinkDur)

def readF(tempPin):
    humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
    temperature = temperature * 9/5.0 +32
    if humidity is not None and temperature is not None:
        tempFahr = '{0:0.1f}*F'.format(temperature)
    else:
        print('Error Reading Sensor')
    return tempFahr

def writeF(temp):
    with con:
        try:
            print "Temperature: %s temp" %(temp)
            cur = con.cursor()
            cur.execute(temp)
            print "Data sent"
        except:
            print "Error"

n = 60

try:
    while n > 0:
        n = n-1
        if n == 0:
            data = readF(tempPin)
            writeF(data)
            n = 60

except KeyboardInterrupt:
    os.system('clear')
    print('Thanks for Blinking and Thinking!')
    GPIO.cleanup()
