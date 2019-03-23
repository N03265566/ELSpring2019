#Import Libraries we will be using
import RPi.GPIO as GPIO
import os
import time
import sqlite3 as mydb
import sys

#Assign GPIO pins
camPin1 = 13
camPin2 = 26

#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(camPin1, GPIO.IN)
GPIO.setup(camPin2, GPIO.IN)

def logTime(order):
    con = mydb.connect('/home/bryan/EL/ELSpring2019/log/motions.db')
    with con:
		try:
                        if(order==1):
                            T=time.strftime("%Y-%m-%d %H:%M:%S")
                            cur = con.cursor()
                            cur.execute('insert into motionData values(?)',(T))
                            print "Entry logged"
                        if(order==2):
                            T=time.strftime("%Y-%m-%d %H:%M:%S")
                            cur = con.cursor()
                            cur.execute('insert into motionData values(?)',(T))
                            print "Exit logged"
                        else:
                            break;
		except mydb.Error, e:
			print "Error %s:" %e.args[0]
			sys.exit(1)

def trig1(pin1,pin2,count):
    i = GPIO.input(pin1)
    j = GPIO.input(pin2)
    if(i==1):
        if(j==1):
            logTime(1)
            count++
    if(j==1):
        if(i==1):
            logTime(2)
            count--

def bothTriggers(pin2, wait=5):
    timestamp = False
    timeCheck = time.time()
	while not GPIO.input(pin2):
		if time.time() - timeCheck > wait:
            break
        continue
    if time.time() - timeCheck <= wait:
        timeStamp = time.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(4)
        continue

def tableData():
	cur.execute("Select * FROM motionData")
	print(cur.fetchall())


time.sleep(10)

try:
	with open("../../log/templog.csv", "a") as log:
		con = mydb.connect('/home/bryan/EL/ELSpring2019/log/motions.db')
		while True:
                        cur = con.cursor()
                        timeStamp = False
                        if GPIO.input(camPin1):
                            timeStamp = bothTriggers(roomPin)
                            if timeStamp:
                                count++;
                        if GPIO.input(camPin2):
                            timeStamp = bothTriggers(hallPin)
                            if timeStamp:
                                count--;
			time.sleep(5)
			os.system('clear')

except mydb.Error, e:
	print "Error %s:" %e.args[0]
	sys.exit(1)

except KeyboardInterrupt:
        GPIO.cleanup()
        con.close()
        print('Exited Cleanly')

