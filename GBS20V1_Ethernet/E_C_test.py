
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import copy
import time
import visa
import struct
import socket
import datetime
import winsound
import heartrate
import numpy as np
from command_interpret import *
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from pythonping import ping

'''
@author: Wei Zhang, Elijah Cruda
@date: 2021-08-04
This script is used for testing GBS20V1 Ethernet. The mianly function of this script is I2C write and read, Ethernet communication, instrument control and so on.
'''
hostname = '192.168.2.3'					#FPGA IP address
port = 1024									#port number

#--------------------------------------------------------------------------#
## IIC write slave device
# @param mode[1:0] : '0'is 1 bytes read or wirte, '1' is 2 bytes read or write, '2' is 3 bytes read or write
# @param slave[7:0] : slave device address
# @param wr: 1-bit '0' is write, '1' is read
# @param reg_addr[7:0] : register address
# @param data[7:0] : 8-bit write data
def iic_write(mode, slave_addr, wr, reg_addr, data):
    print(type(mode))
    print(type(slave_addr))
    print(type(wr))
    print(type(reg_addr))
    print(type(data))
    val = mode << 24 | slave_addr << 17 | wr << 16 | reg_addr << 8 | data
    print(val)
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.01)
    cmd_interpret.write_pulse_reg(0x0001)           # reset ddr3 data fifo
    time.sleep(0.01)
    
    # print(hex(val))
#--------------------------------------------------------------------------#
## IIC read slave device
# @param mode[1:0] : '0'is 1 bytes read or wirte, '1' is 2 bytes read or write, '2' is 3 bytes read or write
# @param slave[7:0]: slave device address
# @param wr: 1-bit '0' is write, '1' is read
# @param reg_addr[7:0] : register address
def iic_read(mode, slave_addr, wr, reg_addr):
    val = mode << 24 | slave_addr << 17 |  0 << 16 | reg_addr << 8 | 0x00	  # write device addr and reg addr
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.01)
    cmd_interpret.write_pulse_reg(0x0001)				                      # Sent a pulse to IIC module

    val = mode << 24 | slave_addr << 17 | wr << 16 | reg_addr << 8 | 0x00	  # write device addr and read one byte
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.01)
    cmd_interpret.write_pulse_reg(0x0001)				                      # Sent a pulse to IIC module
    time.sleep(0.01)									                      # delay 10ns then to read data
    return cmd_interpret.read_status_reg(0) & 0xff
#--------------------------------------------------------------------------#

def resetFPGA():
        print("start reset")
        cmd_interpret.write_config_reg(10,1)
        print("reg10 value = " + hex(cmd_interpret.read_config_reg(10)))
        time.sleep(0.05)
        print("resetting error counters")
        cmd_interpret.write_config_reg(10,0) 
        print("reset done!")   

## main functionl
def main():

    ping('192.168.2.3', verbose=True)
    print(cmd_interpret.read_config_reg(0))
    for i in range(13):
        print('status reg = ' , i , hex(cmd_interpret.read_status_reg(i)))


    for i in range(12):
        print('config reg = ' , i , hex(cmd_interpret.read_config_reg(i)))
        
    resetFPGA()

    
    start_time = time.time()
    interval = 1
    lasttime = datetime.datetime.now()  
    with open("log1.txt","w") as infile:
        while True:
            
            if(datetime.datetime.now() - lasttime > datetime.timedelta(seconds=10)):
                lasttime = datetime.datetime.now()
                # file.write(print(cmd_interpret.read_status_reg(2) +  cmd_interpret.read_status_reg(1))) 
                #infile.write("%s align is %s total error status is %s\n"%(lasttime, hex(cmd_interpret.read_status_reg(6)), hex(cmd_interpret.read_status_reg(2) +  cmd_interpret.read_status_reg(1))  ))
                #infile.write("%s align is %s total error status is %s\n"%(lasttime, hex(cmd_interpret.read_status_reg(6)), hex((cmd_interpret.read_status_reg(2) << 16) +  cmd_interpret.read_status_reg(1))  ))
                infile.write("%s errorflag is %s alinger is %s total error status is %s\n"%(lasttime, hex(cmd_interpret.read_status_reg(8)), hex(cmd_interpret.read_status_reg(6)), hex((cmd_interpret.read_status_reg(4) << 48) + (cmd_interpret.read_status_reg(2) << 32) + (cmd_interpret.read_status_reg(2) << 16) +  cmd_interpret.read_status_reg(1))  ))
                # print(type(cmd_interpret.read_status_reg(2)))
                # infile.write(time + cmd_interpret.read_status_reg(2) +  cmd_interpret.read_status_reg(1)) 
                infile.flush()
            



## if statement
if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#initial socket
	s.connect((hostname, port))								#connect socket
	cmd_interpret = command_interpret(s)					#Class instance
	main()													#execute main function
	s.close()												#close socket