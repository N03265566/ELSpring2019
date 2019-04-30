#!/usr/bin/python

#Import Libraries we will be using
import RPi.GPIO as GPIO
import os
import time
import sqlite3 as mydb
import sys
from flask import Flask, render_template, jsonify, Response
import smtplib
import json
import threading

#Assign GPIO pins
camPin1 = 13
camPin2 = 26
#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(camPin1, GPIO.IN)
GPIO.setup(camPin2, GPIO.IN)

count = 0



def trig1(pin1,pin2):
	global order
	i = GPIO.input(pin1)
	j = GPIO.input(pin2)
	if(i==1):
		order = "Entry"
		time.sleep(2)
		trig2(camPin2,order)
	if(j==1):
		order = "Exit"
		time.sleep(2)
		trig2(camPin1,order)

def trig2(pin,order):
	global count
	k = GPIO.input(pin)
	if(k == 1):
		if(order == "Entry"):
			count += 1
		if(order == "Exit"):
			if(count!=0):
				count -= 1
		logTime(order)
		time.sleep(5)

def logTime(order):
	con = mydb.connect('../../log/motions.db')
	with con:
		try:
			global count
			T=time.strftime("%Y-%m-%d %H:%M:%S")
			E = order
			cur = con.cursor()
			cur.execute('insert into motionData values(?,?,?)',(T,E,count))
			print "Data logged"
			print E
			os.system('clear')
			cur.execute("Select * FROM motionData")
			print(cur.fetchall())

		except mydb.Error, e:
			print "Error %s:" %e.args[0]
			sys.exit(1)

def flask_thread():
	conn = mydb.connect('../../log/motions.db', check_same_thread=False)
	curr = conn.cursor()
	app = Flask(__name__)

	@app.route("/")
	def index():
		return render_template('index.html')

	@app.route('/sqlData')
	def chartData():
		conn.row_factory = mydb.Row
		curr.execute("SELECT * FROM motionData")
		dataset = curr.fetchall()
		chartData = []
		for row in dataset:
			chartData.append({"Time": row[0], "Direction": row[1], "Count": int(row[2])})
		return Response(json.dumps(chartData), mimetype='application/json')


	if __name__ == "__main__":
		app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

webApp_thread = threading.Thread(target = flask_thread)
webApp_thread.daemon = True
webApp_thread.start()

time.sleep(10)

try:
	con = mydb.connect('../../log/motions.db')
	while True:
		trig1(camPin1,camPin2)

except mydb.Error, e:
	print "Error %s:" %e.args[0]
	sys.exit(1)

except KeyboardInterrupt:
        GPIO.cleanup()
        con.close()
        print('Exited Cleanly')
