import os
import sys
import time
import winsound
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
    config_filename = "step0_default_PRBSmode.txt"                         # load I2C default value
    COM_Port = "COM5"                                             # need to change according com port

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
            print("Step6 read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr6[i]), hex(Reg_Val6[i]), hex(read_data6[i])))
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
    with open("step9_MSBeye.txt", 'r') as infile:                  # read configuration file
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


    for i in range(3):                                      # if read back data matched with write in data, speaker will make a sound three times
        winsound.Beep(freqency, duration)
        time.sleep(0.01)

    print("Ok!")
#-----------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()
