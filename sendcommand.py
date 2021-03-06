#!/usr/bin/env python
 
import socket   #for sockets
import sys  #for exit
import argparse # parser
from array import array
#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print "Failed to create socket"
    sys.exit()
     
print "Socket Created"
 
host = "192.168.X.X" #Set ip for coffe brewer
port = 2081
buffer = 20

parser = argparse.ArgumentParser(description='Socket client for Smarter Coffe machine')
parser.add_argument("-f", help="Which function to call, 1 = startbrew whit options -c -g -m -s, 2 = startbrew whit settings already on brewer, 3 = start hotplate whit option -m, 4 = set cups whit option -c, 5 = set strength whit option -2, 6 = defin grinder or filter whit option -g", type=int)
parser.add_argument("-c", help="Define how many cups that will be brewed choose between 1 - 12", type=int)
parser.add_argument("-g", help="Define is grinder or filter should be used. 1 for grinder, 0 for filter", type=int)
parser.add_argument("-m", help="Define how many minutes hotplateshould be on. define in minutes minimum 5", type=int)
parser.add_argument("-s", help="Define whick strenght it should be. choose between 1 - 3 ", type=int)
args = parser.parse_args()

returnMessageType = {
	'0x0' : "Ok",
	'0x1' : "Error: Brewing",
	'0x2' : "Error: No carafe",
	'0x3' : "Error: Not enough water",
	'0x4' : "Error: You sent wrong value",
}

#Connect to remote server
s.connect((host , port))


def coffeeSetCupsFunc(number): #cups value can be between 1 - 12. Syntax for cups is 36xx7e where 36 is value for "set cups" xx is how many and 7e is packet terminator
	cupsHex = ""
	if number <= 12 and number >= 1:
		cupsHex = "%0.2X" % number # convert to hex
	else:
		print "Error: coffe cups must be a value between 1 - 12 autosetting 1 cup"
		cupsHex = "01"
	coffeeSetCups = "36" + cupsHex + "7e"
	return coffeeSetCups
	
def coffeeSetStrengthFunc(numberStrength): # strength value can be between 1 - 3 when send to machine the value vill be converterd to 0 - 2
	numberStrength = numberStrength - 1
	strenghtHex = ""
	if numberStrength >= 0 and numberStrength <= 2:
		strengthHex = "%0.2X" % numberStrength # convert to hex
	else:
		print "Error: coffe strength must be a value between 1 - 3 autosetting 1"
		strengthHex = "00"
	coffeeSetStrength = "35" + strengthHex + "7e"
	return coffeeSetStrength
	
def coffeeStartFunc(cupsStart, strenghtStart, grindStart, hotPlateTime): #cupsStart = how many cups will be made max 12 min 1, 01 - 09 10 = 0a 11 = 0b 12 = 0c. strenghtStart = how strong the coffe will be 1 - 3. grindStart = 01 = on 00 = off (grinder, filter). hotPlateTime = how long the hotplate will stay on after finished brewing minimum 5min 
	cupsHex = ""
	strenghtHex = ""
	grindHex = ""
	hotPlateHex = ""
	if cupsStart <= 12 and cupsStart >= 1:
		cupsHex = "%0.2X" % cupsStart # convert to hex
	else:
		print "Error: coffe cups must be a value between 1 - 12 autosetting 1 cup"
		cupsHex = "01"
	strenghtStart = strenghtStart -1	
	if strenghtStart >= 0 and strenghtStart <= 2:
		strengthHex = "%0.2X" % strenghtStart # convert to hex
	else:
		print "Error: coffe strength must be a value between 1 - 3 autosetting 1"
		strengthHex = "00"	
		
	if grindStart == 1:
		grindHex = "01"
	else:
		grindHex = "00"
		
	if hotPlateTime < 5:
		print "Error: Time must be minimum 5. Autosetting 5min"
		hotPlateHex = "05"
	else:
		hotPlateHex = "%0.2X" % hotPlateTime # convert to hex
		
	finalHex = "33" + cupsHex + strengthHex + hotPlateHex + grindHex + "7e"
	print finalHex
	return finalHex
	
def coffeeHotPlate(timeValue): #Timevalue is for how long the hot plate will be on before auto turning off. Lowest value is 5 min. Max value is ?
	hotPlateHex = ""
	if timeValue < 5:
		print "Error: Time must be minimum 5. Autosetting 5min"
		hotPlateHex = "3e057e"
	else:
		timeValue = "%0.2X" % timeValue # convert to hex
		hotPlateHex = "3e" + timeValue + "7e"
	return hotPlateHex

def coffeeStartWithCurrentSettings():
	return "37"

def coffeeSetGrinder(valueGrinder): 
    if valueGrinder == 1:
        return "3c007e"
    else:
        return "3c017e"
	
def sendCommand(valueSend):
	s.send(valueSend.decode('hex')) # Send hex encode message to brewer
	returnMessage(s.recv(buffer)) # display return message
	s.close # close socket
	
def returnMessage(incomingData):
	a = array("B", incomingData)		
	b = map(hex, a)
	#print b
	returnMessage = b[1]
	print "Return: " + returnMessageType[returnMessage]
	
		
if args.f:
	if args.f <= 6 and args.f >= 1:
		if args.f == 1:
			if args.c and args.m and args.s:
				sendCommand(coffeeStartFunc(args.c, args.s, args.g, args.m)) # Send command startbrewing whit specified settings
			else:
				print "Error: specify args to function" #TODO Better text
		elif args.f == 2:
			sendCommand(coffeeStartWithCurrentSettings()) #Send command startbrewing whit avaliable settings
		elif args.f == 3:
			if args.m:
				sendCommand(coffeeHotPlate(args.m)) #Send command start hotplate
			else:
				print "Error: specify args to function" #TODO Better text
		elif args.f == 4:
			if args.c:
				sendCommand(coffeeSetCupsFunc(args.c)) #Send command set cups
			else:
				print "Error: specify args to function" #TODO Better text
		elif args.f == 5:
			if args.s:
				sendCommand(coffeeSetStrengthFunc(args.s)) #Send command set strength
			else:
				print "Error: specify args to function" #TODO Better text
		elif args.f == 6:
			if args.g:
				sendCommand(coffeeSetGrinder(args.g)) #Send command set grinder or filter
			else:
				print "Error: specify args to function" #TODO Better text
	else:
		print "Function must be between 1 -6"
else:
	print "You must specify an function! -f 1 = startbrew whit options -c -g -m -s, 2 = startbrew whit settings already on brewer, 3 = start hotplate whit option -m, 4 = set cups whit option -c, 5 = set strength whit option -s, 6 = defin grinder or filter whit option -g"
	exit()
#

