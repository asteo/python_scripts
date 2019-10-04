import threading
import time
import serial
import binascii
import argparse
import signal
import os
import sys
from sys import platform
import subprocess 

t1_regexp_list = ['als_value','Set day mode']
t1_regexp_line = 'BRD'

t2_regexp_list = ["ALS","| mode |"]
t2_regexp_line = 'isp_vs_metrics'

t1_serial_interface = '/dev/ttyUSB0'
t1_full_logs_path   = 'logger_data/t1_log.txt'
t1_regexp_logs_path =  'logger_data/t1_regexp_log.txt'
# if os.uname()[4] == 'armv5tel':

t2_serial_interface = '/dev/ttyUSB1'
t2_full_logs_path   = '/home/asteo/Documents/logger_data/logs/t2_log.txt'
t2_regexp_logs_path =  '/home/asteo/Documents/logger_data/logs/t2_regexp_log.txt'
#----------------------------------------------------------------------

#----------------------------------------------------------------------
#=============================================
#
#=============================================
def print_time(threadName):
    print ("%s: %s " % (threadName, time.ctime(time.time())))
#=============================================
#
#=============================================
def initSerial(port, speed):
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = speed
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    ser.timeout = 2              #timeout block read
    ser.xonxoff = False     #disable software flow control
    ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 2     #timeout for write
    return ser
#=============================================
# Thread responsible for whole device logs 
# also saves ISP metrics to separate file  
#=============================================
class myLoggerThread (threading.Thread):
    #---------------------------
    def __init__(self, threadID, name, logs_path, metrics_path, regexp_list :list, regexp_line :str, port='/dev/ttyUSB0',rate=115200,exclude_regexp_list=False):
        threading.Thread.__init__(self)
        self.threadID      = threadID
        self.name          = name
        self.port          = initSerial(port, rate)
        self.log_path      = logs_path
        self.metrics_path  = metrics_path
        self.isRunning     = True
        self.regexp_list   = regexp_list
        self.regexp_line   = regexp_line
        self.exclude_regexp_list   = exclude_regexp_list
    #---------------------------
    def run(self):
        print ("Starting " + self.name)
        # Get lock to synchronize threads
        try: 
            self.port.open()
        except Exception as e:
            print("error open serial port: " + str(e))
            exit()
        try: 
            with open(self.log_path, 'a') as log:  # Use file to refer to the file object
                log.write("\n ------ started at: " + time.ctime(time.time()) + " --\n" )
        except Exception as e:
            print("error open full log: " + str(e))
            exit()
        try: 
            threadLock.acquire()
            with open(self.metrics_path, 'a') as metrics:  # Use file to refer to the file object
                metrics.write("\n ------ started at: " + time.ctime(time.time()) + " --\n" )
            threadLock.release()
        except Exception as e:
            print("error open metrics log in logger thread: " + str(e))
            exit()
            
        try:
            self.port.flushInput() #flush input buffer, discarding all its contents
            self.port.flushOutput()#flush output buffer, aborting current output and discard all that is in buffer
            while self.port.isOpen() and self.isRunning :
                response_bin = self.port.readline()
                try:
                    response = response_bin.decode('ascii')
                    with open(self.log_path, 'a') as log:
                        log.write(response)
                    print(response + '')
                    
                    if self.regexp_line in response:
                        if self.exclude_regexp_list:
                            if not any(regexp in response for regexp in self.regexp_list):
                                threadLock.acquire()
                                with open(self.metrics_path, 'a') as metrics:
                                    metrics.write(response)
                                threadLock.release()
                        else:
                            if any(regexp in response for regexp in self.regexp_list):
                                threadLock.acquire()
                                with open(self.metrics_path, 'a') as metrics:
                                    metrics.write(response)
                                threadLock.release()
                except Exception as e2:
                    print("error decoding...: " + str(e2))
                    print(str(binascii.b2a_base64(response_bin)))

        except Exception as e1:
            print("error communicating...: " + str(e1))
            self.port.close()
    #---------------------------
    def stop(self):
        self.port.reset_input_buffer()
        self.isRunning = False
        print("Closing " + self.name + " ...")
        with open(self.metrics_path, 'a') as metrics: 
            metrics.write("\n ------ log thread closed at: " + time.ctime(time.time()) + " --\n" )
        with open(self.log_path, 'a') as log: 
            log.write("\n ------ log thread closed at: " + time.ctime(time.time()) + " --\n" )
    #---------------------------
    def __del__(self):
        print("Delete " + self.name + " ...")


threadLock = threading.Lock()

t1_logger = myLoggerThread(1, "T1-Logger", t1_full_logs_path, t1_regexp_logs_path, t1_regexp_list, t1_regexp_line,t1_serial_interface, 9600)
# t2_logger = myLoggerThread(2, "T2-Logger", t2_full_logs_path, t2_regexp_logs_path, t2_regexp_list, t2_regexp_line,t2_serial_interface, 115200, True)

# Start new Threads
t1_logger.start()
# t2_logger.start()

def receiveSignal(signum, stack):
    print ('Received: {} {}'.format(signum, stack))
    if signum == signal.SIGINT:
        if t1_logger != None:
            t1_logger.stop()
        # if t2_logger != None:
        #     t2_logger.stop()
        exit(0)

signal.signal(signal.SIGUSR1, receiveSignal)
signal.signal(signal.SIGINT, receiveSignal)

if t1_logger != None:
    t1_logger.join()
# if t2_logger != None:
#     t2_logger.join()
print ("Exiting Main Thread")