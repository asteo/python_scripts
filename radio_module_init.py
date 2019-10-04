import serial
ser = serial.Serial('/dev/ttyUSB0')  # open serial port
print(ser.name)         # check which port was really used
#---------------------------------------------------------------
cmd ='AT'
print('Check that module is alive')
print(cmd)
ser.write(str.encode(cmd))     # write a string
s = ser.readline()
print(s)
print('---------------------------------------------------------------')
 
print('Check current module baudrate')
cmd ='AT+RB'
print(cmd)
ser.write(str.encode(cmd))     # write a string
s = ser.readline()
print(s)
print('---------------------------------------------------------------')
 
print('Check current module RF channel')
cmd ='AT+RC'
print(cmd)
ser.write(str.encode(cmd))     # write a string
s = ser.readline()
print(s)
print('---------------------------------------------------------------')
 
print('Check current module work mode')
cmd ='AT+RF'
print(cmd)
ser.write(str.encode(cmd))     # write a string
s = ser.readline()
print(s)
print('---------------------------------------------------------------')
 
print('Check current module POWER mode')
cmd ='AT+RP'
print(cmd)
ser.write(str.encode(cmd))     # write a string
s = ser.readline()
print(s)
print('---------------------------------------------------------------')
print('  ')
print('  ')
print('############### SET NEW VALUES ################################')
 
baudrate = 'AT+B115200'
mode     = 'AT+FU3'
channel  = 'AT+C025'
#---------------------------------------------------------------     # write a string
print(baudrate)
ser.write(str.encode(baudrate))     # write a string
s = ser.readline()
print(s)
 
print(mode)
ser.write(str.encode(mode))     # write a string
s = ser.readline()
print(s)
 
print(channel)
ser.write(str.encode(channel))     # write a string
s = ser.readline()
print(s)