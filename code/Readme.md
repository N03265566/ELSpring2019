This is where I put my programs and code

### Assignment 3

The pins for the GPIO are first assigned and given variables and are assigned by what they are on the bread board

The oneBlink method is for the LED on the breadboard that makes it blink for the blinkDur which is set to .1
using the time.sleep

The readTemp looks at the i2c device with open("/sys/bus/w1/devices/28-000006961c7b/w1_slave")
It reads the data from the i2c into text with a time stamp
It then closes the file then converts the value for Celcius then for Fahrenheit and returns the time, Celcius, and Fahrenheit

The logTemp connects to the database called temperature.db
It takes the input from read temp and stores it into variables while outputting the current temperature
It takes the values then stores them into the database into a table called TempData

The tableData takes all of the data in the data table and prints it on the console

After all those defined the program opens the templog.csv for the log data
It reads the data from the temperature.db
It blinks the LED then takes in the values for the time and temperatures and logs it using readTemp() and logTemp()
It writes the temperature recorded to the log using log.write("{0},{1},{2}\n".format(time.strftime("%Y,%m,%d %H:%M:%S"),C,F))
Then the data from the table is printed and waits 60 seconds and clears the console and repeats this process
