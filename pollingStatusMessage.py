#!/usr/bin/env python
 
import socket   #for sockets
import sys  #for exit
from array import array
incommingCommandSecond = ""
incommingCommandFirst = ""
#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
     
#print 'Socket Created'
 
host = '192.168.86.194';
port = 2081;
statusMessageType = {
	'0x4' : "Filter, No carafe",
	'0x5' : "Filter, OK to start",
	'0x6' : "Grinder, No carafe",
	'0x7' : "Grinder, OK to start",
	'0x20' : "Filter, No carafe",
	'0x22' : "Grinder, No carafe",
	'0x45' : "Filter, Done",
	'0x47' : "Grinder, Done",
	'0x51' : "Brewing",
	'0x53' : "Boiling",
	'0x60' : "Filter, No carafe, Hotplate On",
	'0x61' : "Filter, Hotplate On",
	'0x62' : "Grinder, No carafe, Hotplate On",
	'0x63' : "Grinder, Hotplate On",
	
}
waterLevelMessageType = {
    '0x0' : "Very low",
    '0x1': "Low",
	'0x2' : "Not enough water",
	'0x11' : "Half",
	'0x12' : "Half",
	'0x13' : "Full",		
}
strengthMessageType = {
	'0x0' : "1",
	'0x1' : "2",
	'0x2' : "3",		
} 
cupsMessageType = {
	'0x11' : "1",
	'0x12' : "2",
	'0x13' : "3",
	'0x14' : "4",
	'0x15' : "5",
	'0x16' : "6",
	'0x17' : "7",
	'0x18' : "8",
	'0x19' : "9",
	'0x1a' : "10",
	'0x1b' : "11",
	'0x1c' : "12",
	'0x21' : "1",
	'0x22' : "2",
	'0x23' : "3",
	'0x24' : "4",
	'0x25' : "5",
	'0x26' : "6",
	'0x27' : "7",
	'0x28' : "8",
	'0x29' : "9",
	'0x2a' : "10",
	'0x2b' : "11",
	'0x2c' : "12",
	'0x51' : "1",
	'0x52' : "2",
	'0x53' : "3",
	'0x54' : "4",
	'0x55' : "5",
	'0x56' : "6",
	'0x57' : "7",
	'0x58' : "8",
	'0x59' : "9",
	'0x5a' : "10",
	'0x5b' : "11",
	'0x5c' : "12",
	'0x61' : "1",
	'0x62' : "2",
	'0x63' : "3",
	'0x64' : "4",
	'0x65' : "5",
	'0x66' : "6",
	'0x67' : "7",
	'0x68' : "8",
	'0x69' : "9",
	'0x6a' : "10",
	'0x6b' : "11",
	'0x6c' : "12",
	'0x1' : "1",
	'0x2' : "2",
	'0x3' : "3",
	'0x4' : "4",
	'0x5' : "5",
	'0x6' : "6",
	'0x7' : "7",
	'0x8' : "8",
	'0x9' : "9",
	'0xa' : "10",
	'0xb' : "11",
	'0xc' : "12",
} 

#Connect to remote server
s.connect((host , port))
 
#print 'Socket Connected to ' + host + ' on ip ' + host
#while 1:
reply = s.recv(4096)
incommingCommandFirst = reply
if incommingCommandFirst == incommingCommandSecond: # only display message if something is changed
	pass
else:
	incommingCommandSecond = reply
	a = array("B", reply)
	b = map(hex, a)
	#print b
	deviceMessage = b[0]
	statusMessage = b[1]
	waterLevelMessage = b[2]
	wifiStrengthMessage = b[3]
	strengthMessage = b[4]
	cupsMessage = b[5]
	#print "Status: " + statusMessageType[statusMessage] + " (" + statusMessage + ")"
	#print "WaterLevel: " + waterLevelMessageType[waterLevelMessage]
	#print "Strength: " + strengthMessageType[strengthMessage]
	print "{\"cups\": " + cupsMessageType[cupsMessage] + ", \"status\": \"" + statusMessageType[statusMessage] + "\", \"water\" : \"" + waterLevelMessageType[waterLevelMessage] + "\", \"strength\" : " + strengthMessageType[strengthMessage] + "}"
	#print "-----------------"

	#print "Status: " + statusMessageType[statusMessage] + " ,WaterLevel: " + waterLevelMessageType[waterLevelMessage] + " ,Strength: " + strengthMessageType[strengthMessage] + " ,Cups: " + cupsMessageType[cupsMessage]
		
