#!/usr/bin/python3

import threading, time, serial, subprocess, os

stopFlag = False #Flag to determine when to end program

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
ser.flushInput()
#ser.open()


#def serialWrite():
#  global stopFlag
#  while True:
#    dataToSend = raw_input("Command>>> ") 
#    if dataToSend == "":
#      continue
    #ser.write(str.encode(prepared + "\n"))
	#ser.close() 
#    ser.write(dataToSend + "\n")
#    if dataToSend == "exit":
#      stopFlag = True
#      print "Exiting serialWrite"
#      return
comp_list = ["Hello Pi, this is the arduino uno\r\n", "b'Hello Pi, this is the arduino uno\r\n'", "b'Flash complete\r\n'"]

def serialRead():
	while True:
		if (ser.in_waiting > 0):
			inputValue = ser.readline() 
			print(inputValue)
			if True:
				try:
					n = input("Set Arduino flash times: ")
					no = str.encode(n)
					ser.write(no)
				except:
					print("Input error, please input a number")
					ser.write(str.encode('0'))
	#while stopFlag==False:
	#	dataToRead = ser.readline()
	#	dataToRead = dataToRead.decode()
		
    #speed = "Speed: 250"
    #direction = "C"
	#	if dataToRead != "":
	#		print("\n"+dataToRead)
    #print "Command>>> "
    #if dataToRead[:6] == "Speed: "
    #    speed = dataToRead[6:]
    #    print "Changed the speed to: " + speed
    #if dataToRead == "1\n":
    #    print "Command received, change direction/button press"
    #    direction = "CC"
    #if dataToRead == "0\n":
    #    print "Command received, change direction/button press"
    #    direction = "C"
    #if dataToRead == "MOTOR ON\n":
	#print "Command received, turn motor on"
	#subprocess.call(["sudo", "python", "piComMotorScript.py", speed, direction])
    #if dataToRead == "MOTOR OFF\n":
	#print "Command receieved, turn motor off"
	#subprocess.call(["sudo", "python", "Motor_Stop.py"])
	#	ser.flush()	
    #speed = ""
    #direction = ""
	#print("Exiting serialRead")

try:
	print("Type 'exit' to close program")
#  writeLoop = threading.Thread(target=serialWrite) #create a separate thread for writing to serial port
	readLoop = threading.Thread(target=serialRead) #create a separate thread for reading from serial port
#  writeLoop.start()
	readLoop.start()
#  writeLoop.join() #wait for this thread to finish
	readLoop.join() #wait for this thread to finish
	print("Exiting main thread")
	ser.close()
    
except KeyboardInterrupt:
	ser.close()
