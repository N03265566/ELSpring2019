#!/usr/bin/python

#Import Libraries we will be using
import Adafruit_DHT
import RPi.GPIO as GPIO
import os
import time
import sqlite3 as mydb
import sys
from flask import Flask, render_template, jsonify, Response
import json
import threading
import smtplib

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

def flask_thread():
	conn = sqlite.connect('../../log/temperature.db', check_same_thread=False)
	curr = conn.cursor()
	app = Flask(__name__)

	@app.route("/")
	def index():
		return render_template('index2.html')

	@app,route('/sqlData')
	def chartData():
		conn.row_factory = sqlite.Row
		curr.execute("SELECT * FROM TempData")
		dataset = curr.fetchall()
		charData = []
		for row in dataset:
			charData.append({"Date": row[0], "Celsius": row[1], "Fahrenheit": row[2]})
		return Response(json.dumps(chartData), mimetype='application/json')

		if __name__ == "__main__":
			app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

def oneBlink(pin):
    	GPIO.output(pin,True)
    	time.sleep(blinkDur)
    	GPIO.output(pin,False)
    	time.sleep(blinkDur)

def readTemp():
	tempfile=open("/sys/bus/w1/devices/28-000006961c7b/w1_slave")
	tempfile_text=tempfile.read()
	currentTime=time.strftime("%x %X %Z")
	tempfile.close()
	tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
	tempF=tempC* 9.0/5.0 +32.0
    	return [currentTime, tempC, tempF]

def logTemp():
	con = mydb.connect('/home/bryan/EL/ELSpring2019/code/Auto_Sensor/temperature.db')
	with con:
		try:
			[t,C,F]=readTemp()
			print "Current temperature is: %s F" %F
			cur = con.cursor()
			#sql = "insert into TempData values(?,?,?)"
			cur.execute('insert into TempData values(?,?,?)',(t,C,F))
			print "Temperature logged"
		except mydb.Error, e:
			print "Error %s:" %e.args[0]
			sys.exit(1)

def tableData():
	cur.execute("Select * FROM TempData")
	print(cur.fetchall())


try:
	with open("../../log/templog.csv", "a") as log:
		con = mydb.connect('/home/bryan/EL/ELSpring2019/code/Auto_Sensor/temperature.db')
		while True:
			for i in range(blinkTime):
				oneBlink(redPin)
			t,C,F = readTemp()
			cur = con.cursor()
			readTemp()
			logTemp()
			log.write("{0},{1},{2}\n".format(time.strftime("%Y,%m,%d %H:%M:%S"),C,F))
			os.fsync(log)
			tableData()
			time.sleep(60)
			os.system('clear')

except KeyboardInterrupt:
    	os.system('clear')
    	print('Thanks for Blinking and Thinking!')
    	GPIO.cleanup()
