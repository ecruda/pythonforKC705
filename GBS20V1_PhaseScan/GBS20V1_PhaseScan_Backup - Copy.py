import os
import sys
import time
import winsound
import numpy as np
from usb_iss import UsbIss, defs
'''
@author: Lily Zhang
@date: March 28, 2021
This script as a generic I2C cofniguration software to configure I2C slave. The I2C reg configuration data is read into a xxx.dat file.
The UsbIss as I2C master deivce is used to write and read I2C slave register.
'''
#-----------------------------------------------------------------------------------#
freqency = 1000
duration = 200
#-----------------------------------------------------------------------------------#


def main():

#-----------------------------------------------------------------------------------#
# Step0,load step0_default_PRBSmode.txt value, check I2C wirte and read
#-----------------------------------------------------------------------------------#
    config_filename = "step0_default.txt"                         # load I2C default value
    COM_Port = "COM4"                                             # need to change according com port

    I2C_Addr = 0x20                                               # Please check in test plan or user manual
    Reg_Addr0 = [] 
    Reg_Val0 = []
    with open(config_filename, 'r') as infile:                    # read configuration file
        for line in infile.readlines():
            Reg_Addr0 += [int(line.split()[0], 16)]
            Reg_Val0 += [int(line.split()[1], 16)]

    print (Reg_Addr0)
    #print (Reg_Val0)

    # set usb-iss iic master device
    iss = UsbIss()
    iss.open(COM_Port)
    iss.setup_i2c(clock_khz=100)

    regWritelen = 32
    #print(regWritelen)
    for i in range(regWritelen):                                  # write data into i2c slave
        #print (I2C_Addr, hex(Reg_Addr0[i]), hex(Reg_Val0[i]))
        iss.i2c.write(I2C_Addr, Reg_Addr0[i], [Reg_Val0[i]])
        time.sleep(0.02)

    regReadlen = 39                                               
    read_data0 = []
    for i in range(regReadlen):                                   # read data from i2c slave
        read_data0 += iss.i2c.read(I2C_Addr, Reg_Addr0[i], 1)
        time.sleep(0.02)

    print(Reg_Val0)
    print(read_data0)

    # compare write in data with read back data
    print('Check write-in registers:')
    for i in range(regWritelen):
        if Reg_Val0[i] != read_data0[i]:
            print("Step0 read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr0[i]), hex(Reg_Val0[i]), hex(read_data0[i])) )
    print('Step0 pass!')

#-----------------------------------------------------------------------------------#
## Step1,load step1_AFC_S1.txt, check I2C wirte and read. This step sets the PLL work in Ovrride mode, Pll loop is turned off.
#-----------------------------------------------------------------------------------#
    Reg_Addr1 = [] 
    Reg_Val1 = []
    with open("step1_AFC_S1.txt", 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            Reg_Addr1 += [int(line.split()[0], 16)]
            Reg_Val1 += [int(line.split()[1], 16)]
  
    for i in range(regWritelen):                                   # write data into i2c slave
        # print (I2C_Addr, hex(Reg_Addr1[i]), hex(Reg_Val1[i]))
        iss.i2c.write(I2C_Addr, Reg_Addr1[i], [Reg_Val1[i]])
        time.sleep(0.02)

    read_data1 = []
    for i in range(regReadlen):                                    # read data from i2c slave
        read_data1 += iss.i2c.read(I2C_Addr, Reg_Addr1[i], 1)
        time.sleep(0.02)

    print(Reg_Val1)
    print(read_data1)

    print('Check write-in registers:')
    for i in range(regWritelen):
        if Reg_Val1[i] != read_data1[i]:
            print("Step1 read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr1[i]), hex(Reg_Val1[i]), hex(read_data1[i])) )
    print('Step1 pass!')

#-----------------------------------------------------------------------------------#
## Step2, load step2_AFC_SR2.1.txt.This step begins to reset AFC,check I2C wirte and read.
#-----------------------------------------------------------------------------------#
    Reg_Addr2 = [] 
    Reg_Val2 = []
    with open("step2_AFC_SR2.1.txt", 'r') as infile:               # read configuration file
        for line in infile.readlines():
            Reg_Addr2 += [int(line.split()[0], 16)]
            Reg_Val2 += [int(line.split()[1], 16)]

    for i in range(regWritelen):                                   # write data into i2c slave
        # print (I2C_Addr, hex(Reg_Addr2[i]), hex(Reg_Val2[i]))
        iss.i2c.write(I2C_Addr, Reg_Addr2[i], [Reg_Val2[i]])
        time.sleep(0.02)

    read_data2 = []
    for i in range(regReadlen):                                    # read data from i2c slave
        read_data2 += iss.i2c.read(I2C_Addr, Reg_Addr2[i], 1)
        time.sleep(0.02)

    print(Reg_Val2)
    print(read_data2)

    print('Check write-in registers:')
    for i in range(regWritelen):
        if Reg_Val2[i] != read_data2[i]:
            print("Step2 read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr2[i]), hex(Reg_Val2[i]), hex(read_data2[i])))
    print('Step2 pass!')

#-----------------------------------------------------------------------------------#
## Step3, load step3_AFC_SR2.2.txt,.This step finish reset AFC, check I2C wirte and read
#-----------------------------------------------------------------------------------#
    Reg_Addr3 = [] 
    Reg_Val3 = []
    with open("step3_AFC_SR2.2.txt", 'r') as infile:               # read configuration file
        for line in infile.readlines():
            Reg_Addr3 += [int(line.split()[0], 16)]
            Reg_Val3 += [int(line.split()[1], 16)]

    for i in range(regWritelen):                                    # write data into i2c slave
        # print (I2C_Addr, hex(Reg_Addr3[i]), hex(Reg_Val3[i]))
        iss.i2c.write(I2C_Addr, Reg_Addr3[i], [Reg_Val3[i]])
        time.sleep(0.02)

    read_data3 = []
    for i in range(regReadlen):                              # read data from i2c slave
        read_data3 += iss.i2c.read(I2C_Addr, Reg_Addr3[i], 1)
        time.sleep(0.02)

    print(Reg_Val3)
    print(read_data3)

    print('Check write-in registers:')
    for i in range(regWritelen):
        if Reg_Val3[i] != read_data3[i]:
            print("Step3 read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr3[i]), hex(Reg_Val3[i]), hex(read_data3[i])))
    print('Step3 pass!')

#-----------------------------------------------------------------------------------#
## Step4, load step4_AFC_S2.1.txt.This step begins to launch AFC, check I2C wirte and read
#-----------------------------------------------------------------------------------#
    Reg_Addr4 = [] 
    Reg_Val4 = []
    with open("step4_AFC_S2.1.txt", 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            Reg_Addr4 += [int(line.split()[0], 16)]
            Reg_Val4 += [int(line.split()[1], 16)]

    for i in range(regWritelen):                              # write data into i2c slave
        # print (I2C_Addr, hex(Reg_Addr4[i]), hex(Reg_Val4[i]))
        iss.i2c.write(I2C_Addr, Reg_Addr4[i], [Reg_Val4[i]])
        time.sleep(0.02)

    read_data4 = []
    for i in range(regReadlen):                              # read data from i2c slave
        read_data4 += iss.i2c.read(I2C_Addr, Reg_Addr4[i], 1)
        time.sleep(0.02)

    print(Reg_Val4)
    print(read_data4)

    print('Check write-in registers:')
    for i in range(regWritelen):
        if Reg_Val4[i] != read_data4[i]:
            print("Step4 read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr4[i]), hex(Reg_Val4[i]), hex(read_data4[i])))
    print('Step4 pass!')

#-----------------------------------------------------------------------------------#
## Step5,load step5_AFC_S2.2.txt. This step finish AFC calibration, check I2C wirte and read. 
# And get the AFCcalCap in reg20.
#-----------------------------------------------------------------------------------#
    Reg_Addr5 = [] 
    Reg_Val5 = []
    with open("step5_AFC_S2.2.txt", 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            Reg_Addr5 += [int(line.split()[0], 16)]
            Reg_Val5 += [int(line.split()[1], 16)]

    for i in range(regWritelen):                              # write data into i2c slave
        # print (I2C_Addr, hex(Reg_Addr5[i]), hex(Reg_Val5[i]))
        iss.i2c.write(I2C_Addr, Reg_Addr5[i], [Reg_Val5[i]])
        time.sleep(0.02)

    read_data5 = []
    for i in range(regReadlen):                              # read data from i2c slave
        read_data5 += iss.i2c.read(I2C_Addr, Reg_Addr5[i], 1)
        time.sleep(0.02)

    print(Reg_Val5)
    print(read_data5)

    AFCCalCap = (read_data5[-7])
    print ("%s,%s"%('AFCCalCap',AFCCalCap))

    AFCbusy = (read_data5[-6])
    print ("%s,%s"%('AFCbusy',AFCbusy))

    print('Check write-in registers:')
    for i in range(regWritelen):
        if Reg_Val5[i] != read_data5[i]:
            print("Step5 read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr5[i]), hex(Reg_Val5[i]), hex(read_data5[i])))
    print('Step5 pass!')
      
    #AFCcalCap = (read_data5[-2]&0x7e)>>1
    #print ("%s,%s"%('AFCvalue',AFCcalCap))


#-----------------------------------------------------------------------------------#
# ##Step6,load step6_AFC_S4.txt. This step,AFC work in override mode,and AFCcalCap will wirte in AFC.
#-----------------------------------------------------------------------------------#
    Reg_Addr6 = [] 
    Reg_Val6 = []
    with open("step6_AFC_S4.txt", 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            Reg_Addr6 += [int(line.split()[0], 16)]
            Reg_Val6 += [int(line.split()[1], 16)]

    Reg_Val6[7] = AFCCalCap 

    #print (Reg_Val6)
    for i in range(regWritelen):                              # write data into i2c slave
        # print (I2C_Addr, hex(Reg_Addr6[i]), hex(Reg_Val6[i]))
        iss.i2c.write(I2C_Addr, Reg_Addr6[i], [Reg_Val6[i]])
        time.sleep(0.02)

    read_data6 = []
    for i in range(regReadlen):                              # read data from i2c slave
        read_data6 += iss.i2c.read(I2C_Addr, Reg_Addr6[i], 1)
        time.sleep(0.02)

    print(Reg_Val6)
    print(read_data6)

    INSTLOCK_PLL = (read_data6[-5])
    print ("%s,%s"%('INSTLOCK_PLL',INSTLOCK_PLL))

    print('Check write-in registers:')
    for i in range(regWritelen):
        if Reg_Val6[i] != read_data6[i]:
            print("Step4 read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr6[i]), hex(Reg_Val6[i]), hex(read_data6[i])))
    print('Step6 pass!')

#-----------------------------------------------------------------------------------#
## Step7, load step7_AFC_S5.txt. This step is for locking PLL,check I2C wirte and read.
#-----------------------------------------------------------------------------------#
    Reg_Addr7 = [] 
    Reg_Val7 = []
    with open("step7_AFC_S5.txt", 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            Reg_Addr7 += [int(line.split()[0], 16)]
            Reg_Val7 += [int(line.split()[1], 16)]
    Reg_Val7[7] = AFCCalCap

    for i in range(regWritelen):                              # write data into i2c slave
        # print (I2C_Addr, hex(Reg_Addr2_1[i]), hex(Reg_Val2_1[i]))
        iss.i2c.write(I2C_Addr, Reg_Addr7[i], [Reg_Val7[i]])
        time.sleep(0.02)

    read_data7 = []
    for i in range(regReadlen):                              # read data from i2c slave
        read_data7 += iss.i2c.read(I2C_Addr, Reg_Addr7[i], 1)
        time.sleep(0.02)

    print(Reg_Val7)
    print(read_data7)

    INSTLOCK_PLL = (read_data7[-5])
    print ("%s,%s"%('INSTLOCK_PLL',INSTLOCK_PLL))

    print('Check write-in registers:')
    for i in range(regWritelen):
        if Reg_Val7[i] != read_data7[i]:
            print("Step7 read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr7[i]), hex(Reg_Val7[i]), hex(read_data7[i])))
    print('Step7 pass!')


#-----------------------------------------------------------------------------------#
## Step8, load step8_RstPrbs.txt, This step reset prbs,check I2C wirte and read
#-----------------------------------------------------------------------------------#
    Reg_Addr8 = [] 
    Reg_Val8 = []
    with open("step8_RstPrbs.txt", 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            Reg_Addr8 += [int(line.split()[0], 16)]
            Reg_Val8 += [int(line.split()[1], 16)]
    Reg_Val8[7] = AFCCalCap

    for i in range(regWritelen):                              # write data into i2c slave
        # print (I2C_Addr, hex(Reg_Addr2_1[i]), hex(Reg_Val2_1[i]))
        iss.i2c.write(I2C_Addr, Reg_Addr8[i], [Reg_Val8[i]])
        time.sleep(0.02)

    read_data8 = []
    for i in range(regReadlen):                              # read data from i2c slave
        read_data8 += iss.i2c.read(I2C_Addr, Reg_Addr8[i], 1)
        time.sleep(0.02)

    print(Reg_Val8)
    print(read_data8)

    print('Check write-in registers:')
    for i in range(regWritelen):
        if Reg_Val8[i] != read_data8[i]:
            print("Step8 read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr8[i]), hex(Reg_Val8[i]), hex(read_data8[i])))
    print('Step8 pass!')
#-----------------------------------------------------------------------------------#
## Step9, load step9_LSBeye.txt, This step is for measuring the max value of BIAS,and observe the LSB current.
# check I2C wirte and read
#-----------------------------------------------------------------------------------#
    Reg_Addr9 = [] 
    Reg_Val9 = []
    with open("step9_LSBeye.txt", 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            Reg_Addr9 += [int(line.split()[0], 16)]
            Reg_Val9 += [int(line.split()[1], 16)]
    Reg_Val9[7] = AFCCalCap

    for i in range(regWritelen):                              # write data into i2c slave
        # print (I2C_Addr, hex(Reg_Addr2_1[i]), hex(Reg_Val2_1[i]))
        iss.i2c.write(I2C_Addr, Reg_Addr9[i], [Reg_Val9[i]])
        time.sleep(0.02)

    read_data9 = []
    for i in range(regReadlen):                              # read data from i2c slave
        read_data9 += iss.i2c.read(I2C_Addr, Reg_Addr9[i], 1)
        time.sleep(0.02)

    print(Reg_Val9)
    print(read_data9)
    
    print('Check write-in registers:')
    for i in range(regWritelen):
        if Reg_Val9[i] != read_data9[i]:
            print("Step9 read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr9[i]), hex(Reg_Val9[i]), hex(read_data9[i])))
    print('Step9 pass!')

#-----------------------------------------------------------------------------------#
## Step10 load step10_on_userdata.txt, This step trun on the user data chain, and Begain to reset the DLL of Phaseshift and Read The edge value in phase0.
# check I2C wirte and read
#-----------------------------------------------------------------------------------#
    Reg_Addr10 = [] 
    Reg_Val10 = []
    with open("step10_on_userdata.txt", 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            Reg_Addr10 += [int(line.split()[0], 16)]
            Reg_Val10 += [int(line.split()[1], 16)]
    Reg_Val10[7] = AFCCalCap

    for i in range(regWritelen):                              # write data into i2c slave
        # print (I2C_Addr, hex(Reg_Addr2_1[i]), hex(Reg_Val2_1[i]))
        iss.i2c.write(I2C_Addr, Reg_Addr10[i], [Reg_Val10[i]])
        time.sleep(0.02)
    print(type([Reg_Val10[i]]))
    read_data10 = []
    for i in range(regReadlen):                              # read data from i2c slave
        read_data10 += iss.i2c.read(I2C_Addr, Reg_Addr10[i], 1)
        time.sleep(0.02)

    print(Reg_Val10)
    print(read_data10)

    print('Check write-in registers:')
    for i in range(regWritelen):
        if Reg_Val10[i] != read_data10[i]:
            print("Step10 read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr10[i]), hex(Reg_Val10[i]), hex(read_data10[i])))
    print('Step10 check finihsed!')

#-----------------------------------------------------------------------------------#
## Step11 Reset the edgeDetect and scan phase0.
# check I2C wirte and read
#-----------------------------------------------------------------------------------#
    for i in range(regWritelen):                              # write data into i2c slave
        iss.i2c.write(I2C_Addr, Reg_Addr10[i], [Reg_Val10[i]])
        time.sleep(0.02)
    Reg_Addr11 = [] 
    Reg_Val11 = []
    read_data11 = []
    with open("step11_Reset_Edge.txt", 'r') as infile:                  # read configuration file
       for line in infile.readlines():
         Reg_Addr11 += [int(line.split()[0], 16)]
         Reg_Val11 += [int(line.split()[1], 16)]
    Reg_Val11[7] = AFCCalCap

    print("AFCCalCap: %d"%AFCCalCap)
    iss.i2c.write_ad1(I2C_Addr, 0x07, [int(AFCCalCap)])

    list0 = []
    list1 = []  
    sum_list0 = []
    Repeat = 300
    Phase_value = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    # Phase_value = [0, 17, 34, 51, 68, 85, 102,  119, 136, 153, 170, 187, 204, 221, 238, 255]
    for l in range(Repeat):
        for j in range(len(Phase_value)):                                
            # iss.i2c.write_ad1(I2C_Addr, 0x1a, [0x29])        # set PA0_edgeResetN = 0
            # iss.i2c.write_ad1(I2C_Addr, 0x1b, [0x09])        # set PA1_edgeResetN = 0
            # time.sleep(0.02)
            # iss.i2c.write_ad1(I2C_Addr, 0x1a, [0x39])        # set PA0_edgeResetN = 1
            # iss.i2c.write_ad1(I2C_Addr, 0x1b, [0x19])        # set PA1_edgeResetN = 1
            
            # print("Write Phase value: %d"%Phase_value[j])
            iss.i2c.write_ad1(I2C_Addr, 0x11, [Phase_value[j]])               # write Phase value to LSB channel
            # iss.i2c.write_ad1(I2C_Addr, 0x12, [Phase_value[j]])
            # iss.i2c.write_ad1(I2C_Addr, 0x13, [Phase_value[j]])
            # iss.i2c.write_ad1(I2C_Addr, 0x14, [Phase_value[j]])

            iss.i2c.write_ad1(I2C_Addr, 0x15, [Phase_value[j]])               # write Phase value to MSB channel
            # iss.i2c.write_ad1(I2C_Addr, 0x16, [Phase_value[j]])
            # iss.i2c.write_ad1(I2C_Addr, 0x17, [Phase_value[j]])
            # iss.i2c.write_ad1(I2C_Addr, 0x18, [Phase_value[j]])
         
            iss.i2c.write_ad1(I2C_Addr, 0x0d, [0x2c])                             #LSB seed 0
            #iss.i2c.write_ad1(I2C_Addr, 0x0e, [0x01])                            #MSB seed 0                                      #prbs restet
            # print("Read Phase value: ", iss.i2c.read_ad1(I2C_Addr, 0x11, 1))  # write one Phase value
            iss.i2c.write_ad1(I2C_Addr, 0x1a, [0x29])        # set PA0_edgeResetN = 0
            iss.i2c.write_ad1(I2C_Addr, 0x1b, [0x09])        # set PA1_edgeResetN = 0
            iss.i2c.write_ad1(I2C_Addr, 0x1a, [0x39])        # set PA0_edgeResetN = 1
            iss.i2c.write_ad1(I2C_Addr, 0x1b, [0x19])        # set PA1_edgeResetN = 1
            iss.i2c.write_ad1(I2C_Addr, 0x0d, [0x2d])                 # prbs on
            time.sleep(0.02)

            read_data11 = []
            for i in range(regReadlen):                              # read data from i2c slave
                read_data11 += iss.i2c.read(I2C_Addr, Reg_Addr11[i], 1)
                # time.sleep(0.01)
            print(read_data11)

            PA0_edge = read_data11[-2]
            PA1_edge = read_data11[-1]
            list0 += [PA0_edge]
            list1 += [PA1_edge] 

    
        # print ("%s,%s"%('LSB_testedge',list0))
    
    # print (list0)
    # print (list1)
    Array_list0 = np.array(list0).reshape(Repeat,16)
    Array_list1 = np.array(list1).reshape(Repeat,16)
    print (Array_list0)
    print (Array_list1)
    sum_list0 = sum(Array_list0)
    sum_list1 = sum(Array_list1)
    print (sum_list0)
    print (sum_list1)

    print ("%s,%s"%('PA0_testedge',sum_list0))           
    np.savetxt("PA0_testedge.txt", Array_list0, fmt = '%d', delimiter=",")
    
    print ("%s,%s"%('PA1_testedge',sum_list1))           
    np.savetxt("PA1_testedge.txt", Array_list1, fmt = '%d', delimiter=",")


    for i in range(3):                                      # if read back data matched with write in data, speaker will make a sound three times
        winsound.Beep(freqency, duration)
        time.sleep(0.01)

    print("Ok!")
#-----------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()
