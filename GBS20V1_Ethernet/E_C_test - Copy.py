
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
## DDR3 write data to external device
# @param[in] wr_wrap: wrap address
# @param[in] wr_begin_addr: write data begin address
# @param[in] post_trigger_addr: post trigger address
def write_data_into_ddr3(wr_wrap, wr_begin_addr, post_trigger_addr):
    # writing begin address and wrap_around
    val = (wr_wrap << 28) + wr_begin_addr
    cmd_interpret.write_config_reg(8, 0xffff & val)
    cmd_interpret.write_config_reg(9, 0xffff & (val >> 16))
    # post trigger address
    cmd_interpret.write_config_reg(10, 0xffff & post_trigger_addr)
    cmd_interpret.write_config_reg(11, 0xffff & (post_trigger_addr >> 16))
#--------------------------------------------------------------------------#
## DDR3 read data from fifo to ethernet
# @param[in] rd_stop_addr: read data start address
def read_data_from_ddr3(rd_stop_addr):
    cmd_interpret.write_config_reg(12, 0xffff & rd_stop_addr)
    cmd_interpret.write_config_reg(13, 0xffff & (rd_stop_addr >> 16))
    cmd_interpret.write_pulse_reg(0x0020)           # reading start
#--------------------------------------------------------------------------#
## test ddr3
# @param[in] data_num: set fetch data number
def test_ddr3(data_num):
    cmd_interpret.write_config_reg(0, 0x0000)       # written disable
    cmd_interpret.write_pulse_reg(0x0040)           # reset ddr3 logic, data fifo, and fifo32to256 
    time.sleep(0.1)
    print("sent pulse!")

    write_data_into_ddr3(1, 0x0000000, 0x0700000)   # set write begin address and post trigger address and wrap around
    cmd_interpret.write_pulse_reg(0x0008)           # writing start
    time.sleep(0.1)
    cmd_interpret.write_config_reg(0, 0x0001)       # written enable fifo32to256

    time.sleep(0.5)
    cmd_interpret.write_pulse_reg(0x0010)           # writing stop                           

    time.sleep(3)                                   # delay 2s to receive data
    cmd_interpret.write_config_reg(0, 0x0000)       # fifo32to256 write disablee
    time.sleep(1)
    read_data_from_ddr3(0x0700000)                  # set read begin address

    data_out = []
    for i in range(data_num):                       # reading start
        data_out += cmd_interpret.read_data_fifo(50000)           
    return data_out
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
## Enable FPGA Descrambler
def Enable_FPGA_Descramblber(val):
    if val==1:
        print("Enable FPGA Descrambler")
    else:
        print("Disable FPGA Descrambler")
    cmd_interpret.write_config_reg(14, 0x0001 & val)       # write enable
#--------------------------------------------------------------------------#
## main functionl
def main():
    # slave_addr = 0x4E                                               # I2C slave address
    # # print(test_ddr3(1))
    # print(iic_read(2,slave_addr,1,0))
    # iic_read_val = []
    # for i in range(1000):                                   # Read back from I2C register
    #     iic_read_val += [iic_read(0, slave_addr, 1, i)]
    # print("I2C read back data:")
    # print(iic_read_val)
    ping('192.168.2.3', verbose=True)
    # print(test_ddr3(1))
    # print(read_data_from_ddr3(10000000000000000000))
    # cmd_interpret.write_config_reg(0,0) #(addr,data)
    print(cmd_interpret.read_config_reg(0))
    for i in range(7):
        print('reg = ' , i , hex(cmd_interpret.read_status_reg(i)))
    print(cmd_interpret.read_status_reg(0))
    # print(read_data_from_ddr3(0x1000000000)) 
    # print(cmd_interpret.read_data_fifo(100)) 




## if statement
if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#initial socket
	s.connect((hostname, port))								#connect socket
	cmd_interpret = command_interpret(s)					#Class instance
	main()													#execute main function
	s.close()												#close socket