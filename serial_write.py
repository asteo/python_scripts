import serial
import time
ser = serial.Serial('/dev/ttyUSB0')  # open serial port
print(ser.name)         # check which port was really used
idx = 0
#---------------------------------------------------------------
while True:
    ser.write(str.encode('\r\n Send HP-->TOSHIBA {0}'.format(idx)))
    print(str.encode('\r\n Send HP-->TOSHIBA {0}'.format(idx)))
    idx=idx+1     # write a string
    time.sleep(2)
    if idx > 100:
        break