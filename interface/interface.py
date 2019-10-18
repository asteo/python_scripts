# -*- coding: utf-8 -*-
"""
Created on Oct 17 

@author: arthur.pulatov
"""
import json
import re
import socket
import serial
from time import sleep
from struct import unpack
from datetime import datetime
# #######################################################################
# 
# #######################################################################
class IFACE(object):
    def __init__(self,*args):
        self.data = bytes(0)
        if args:
            configFileName = args[0]
            conf = json.loads(open(configFileName,'r').read())
            self.connectionType = conf['connectionType']
            if self.connectionType == 'serial':
                self.ser = serial.Serial()
                self.ser.baudrate = conf['baudrate']
                self.ser.port = conf['PORT']
                
            elif self.connectionType == 'socket':
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_address = conf['ADDRESS']
                self.port = conf['IP_PORT']
                self.buffer = conf['buffer']
                self.ip_type = conf['IP_TYPE']

            else:
                print('Unknown Connection type!')
# #######################################################################
    def _open(self):
        if self.connectionType == 'serial':
            self.ser.open()
        elif self.connectionType == 'socket':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM if self.ip_type == 'TCP' else socket.SOCK_DGRAM)#socket.SOCK_STREAM)
            self.connectStatus = self.sock.connect_ex((self.server_address,self.port))
        else:
            print('Open ERROR: ',self.connectionType)
# #######################################################################
    def _close(self):
        if self.connectionType == 'serial':
            self.ser.close()
        elif self.connectionType == 'socket':
            self.sock.close()
        else:
            print('Close ERROR: ',self.connectionType)
# #######################################################################
    def _read(self):
        if self.connectionType == 'serial':
            return self.ser.read(self.ser.inWaiting())
        elif self.connectionType == 'socket':
            return self.sock.recv(self.buffer)
        else:
            print('Read ERROR: ',self.connectionType)
# #######################################################################
    def _write(self,msg):
        if self.connectionType == 'serial':
            if self.ser.writable():
                self.ser.write(msg)
                # sleep(1)
            else:
                print('Connection Error')
        elif self.connectionType == 'socket':
            if self.connectStatus == 0:
                self.sock.send(msg)
                # sleep(1)
            else:
                print('Connection Error %s',self.connectStatus)
        else:
            print('Write ERROR: ',self.connectionType)


test_info ="\r\n Hello World \n"
configName = '/home/asteo/Documents/python/interface/config.json'
iface = IFACE(configName)
iface._open()
iface._write(str.encode(test_info))
sleep(1)
iface.data = iface._read()
print(iface.data)
iface._close()

