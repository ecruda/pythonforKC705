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
## Step10 load step10_on_userdata.txt, This step trun on the user data chain, and Begain to reset the DLL of Phaseshift and Read The edge value in phase0.
# check I2C wirte and read
#-----------------------------------------------------------------------------------#
    COM_Port = "COM5"                                             # need to change according com port
    I2C_Addr = 0x20                                               # Please check in test plan or user manual
    
    iss = UsbIss()
    iss.open(COM_Port)
    iss.setup_i2c(clock_khz=100)

    regWritelen = 32
    regReadlen = 39
    Reg_Addr10 = [] 
    Reg_Val10 = []
    with open("step10_on_userdata.txt", 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            Reg_Addr10 += [int(line.split()[0], 16)]
            Reg_Val10 += [int(line.split()[1], 16)]

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
## Step11 Reset the edgeDetect and scan phase.
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

    list0 = []
    list1 = []  
    LSB_list0 = []
    LSB_list1 = []
    LSB_list2 = []
    LSB_list3 = []
    LSB_list4 = []
    LSB_list5 = []
    LSB_list6 = []
    LSB_list7 = []
    MSB_list0 = []
    MSB_list1 = []
    MSB_list2 = []
    MSB_list3 = []
    MSB_list4 = []
    MSB_list5 = []
    MSB_list6 = []
    MSB_list7 = []
    Repeat = 300
    # Phase_value = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    Phase_value = [0, 17, 34, 51, 68, 85, 102,  119, 136, 153, 170, 187, 204, 221, 238, 255]
    for l in range(Repeat):
        for j in range(len(Phase_value)):                                            
            # print("Write Phase value: %d"%Phase_value[j])
            iss.i2c.write_ad1(I2C_Addr, 0x11, [Phase_value[j]])               # write Phase value to LSB channel
            iss.i2c.write_ad1(I2C_Addr, 0x12, [Phase_value[j]])
            iss.i2c.write_ad1(I2C_Addr, 0x13, [Phase_value[j]])
            iss.i2c.write_ad1(I2C_Addr, 0x14, [Phase_value[j]])

            iss.i2c.write_ad1(I2C_Addr, 0x15, [Phase_value[j]])               # write Phase value to MSB channel
            iss.i2c.write_ad1(I2C_Addr, 0x16, [Phase_value[j]])
            iss.i2c.write_ad1(I2C_Addr, 0x17, [Phase_value[j]])
            iss.i2c.write_ad1(I2C_Addr, 0x18, [Phase_value[j]])
         
            # iss.i2c.write_ad1(I2C_Addr, 0x0d, [0x01])                            #LSB seed 0
            # iss.i2c.write_ad1(I2C_Addr, 0x0e, [0x01])                            #MSB seed 0  
            iss.i2c.write_ad1(I2C_Addr, 0x0e, [0x0])                               #trun off prbs clock                                    #prbs restet
            # print("Read Phase value: ", iss.i2c.read_ad1(I2C_Addr, 0x11, 1))     # write one Phase value
            # iss.i2c.write_ad1(I2C_Addr, 0x02, [0xff])                            #trun on equailizer1  LSB
            # iss.i2c.write_ad1(I2C_Addr, 0x03, [0xff])                            #trun on equailizer1  MSB
            # iss.i2c.write_ad1(I2C_Addr, 0x04, [0xff])                            #trun on equailizer0  LSB
            # iss.i2c.write_ad1(I2C_Addr, 0x05, [0xff])                            #trun on equailizer0  MSB
            # iss.i2c.write_ad1(I2C_Addr, 0x0, [0x0])                              # Turn off LSB eRx
            # iss.i2c.write_ad1(I2C_Addr, 0x1, [0x0])                              # Turn off MSB eRx.
            # os.system("pause")
  
            iss.i2c.write_ad1(I2C_Addr, 0x1a, [0x29])                              # set PA0_edgeResetN = 0
            iss.i2c.write_ad1(I2C_Addr, 0x1b, [0x09])                              # set PA1_edgeResetN = 0
            # iss.i2c.write_ad1(I2C_Addr, 0x0, [0xff])                              # Turn on LSB eRx
            # iss.i2c.write_ad1(I2C_Addr, 0x1, [0xff])                              # Turn on MSB eRx

            iss.i2c.write_ad1(I2C_Addr, 0x1a, [0x39])                              # set PA0_edgeResetN = 1
            iss.i2c.write_ad1(I2C_Addr, 0x1b, [0x19])                              # set PA1_edgeResetN = 1
            # iss.i2c.write_ad1(I2C_Addr, 0x1a, [0x21])                              # set PA0_enableDetect = 0
            # iss.i2c.write_ad1(I2C_Addr, 0x1b, [0x01])                              # set PA1_enableDetect = 0  


            #iss.i2c.write_ad1(I2C_Addr, 0x0d, [0x2d])                 # prbs on
            time.sleep(0.02)

            read_data11 = []
            for i in range(regReadlen):                              # read data from i2c slave
                read_data11 += iss.i2c.read(I2C_Addr, Reg_Addr11[i], 1)
                # time.sleep(0.01)
            print(read_data11)

            PA0_edge = read_data11[-2]                          # save LSB and MSB prbs data edge into list 
            PA1_edge = read_data11[-1]
            list0 += [PA0_edge]
            list1 += [PA1_edge] 
      
            LSB_edge_D0 = (read_data11[-4]&0x1)
            LSB_list0 += [LSB_edge_D0]
            LSB_edge_D1 = (read_data11[-4]&0x2)>>1 
            LSB_list1 += [LSB_edge_D1]
            LSB_edge_D2 = (read_data11[-4]&0x4)>>2 
            LSB_list2 += [LSB_edge_D2]
            LSB_edge_D3 = (read_data11[-4]&0x8)>>3 
            LSB_list3 += [LSB_edge_D3]
            LSB_edge_D4 = (read_data11[-4]&0x10)>>4
            LSB_list4 += [LSB_edge_D4]
            LSB_edge_D5 = (read_data11[-4]&0x20)>>5 
            LSB_list5 += [LSB_edge_D5]
            LSB_edge_D6 = (read_data11[-4]&0x40)>>6
            LSB_list6 += [LSB_edge_D6]
            LSB_edge_D7 = (read_data11[-4]&0x80)>>7 
            LSB_list7 += [LSB_edge_D7]

            MSB_edge_D0 = (read_data11[-3]&0x1)
            MSB_list0 += [MSB_edge_D0]
            MSB_edge_D1 = (read_data11[-3]&0x2)>>1 
            MSB_list1 += [MSB_edge_D1]
            MSB_edge_D2 = (read_data11[-3]&0x4)>>2 
            MSB_list2 += [MSB_edge_D2]
            MSB_edge_D3 = (read_data11[-3]&0x8)>>3 
            MSB_list3 += [MSB_edge_D3]
            MSB_edge_D4 = (read_data11[-3]&0x10)>>4
            MSB_list4 += [MSB_edge_D4]
            MSB_edge_D5 = (read_data11[-3]&0x20)>>5 
            MSB_list5 += [MSB_edge_D5]
            MSB_edge_D6 = (read_data11[-3]&0x40)>>6
            MSB_list6 += [MSB_edge_D6]
            MSB_edge_D7 = (read_data11[-3]&0x80)>>7 
            MSB_list7 += [MSB_edge_D7]


    Array_list0 = np.array(list0).reshape(Repeat,16)
    Array_list1 = np.array(list1).reshape(Repeat,16)

    Array_LSB_list0 = np.array(LSB_list0).reshape(Repeat,16)
    Array_LSB_list1 = np.array(LSB_list1).reshape(Repeat,16)
    Array_LSB_list2 = np.array(LSB_list2).reshape(Repeat,16)
    Array_LSB_list3 = np.array(LSB_list3).reshape(Repeat,16)
    Array_LSB_list4 = np.array(LSB_list4).reshape(Repeat,16)
    Array_LSB_list5 = np.array(LSB_list5).reshape(Repeat,16)
    Array_LSB_list6 = np.array(LSB_list6).reshape(Repeat,16)
    Array_LSB_list7 = np.array(LSB_list7).reshape(Repeat,16)

    Array_MSB_list0 = np.array(MSB_list0).reshape(Repeat,16)
    Array_MSB_list1 = np.array(MSB_list1).reshape(Repeat,16)
    Array_MSB_list2 = np.array(MSB_list2).reshape(Repeat,16)
    Array_MSB_list3 = np.array(MSB_list3).reshape(Repeat,16)
    Array_MSB_list4 = np.array(MSB_list4).reshape(Repeat,16)
    Array_MSB_list5 = np.array(MSB_list5).reshape(Repeat,16)
    Array_MSB_list6 = np.array(MSB_list6).reshape(Repeat,16)
    Array_MSB_list7 = np.array(MSB_list7).reshape(Repeat,16)



    # print (Array_list0)
    # print (Array_list1)
    print (Array_LSB_list0)
    print (Array_LSB_list1)
    print (Array_LSB_list2)
    print (Array_LSB_list3)
    print (Array_LSB_list4)
    print (Array_LSB_list5)
    print (Array_LSB_list6)
    print (Array_LSB_list7)

    print (Array_MSB_list0)
    print (Array_MSB_list1)
    print (Array_MSB_list2)
    print (Array_MSB_list3)
    print (Array_MSB_list4)
    print (Array_MSB_list5)
    print (Array_MSB_list6)
    print (Array_MSB_list7)

    sum_list0 = sum(Array_list0)
    sum_list1 = sum(Array_list1)
        
    sum_LSB_list0 = sum(Array_LSB_list0)
    sum_LSB_list1 = sum(Array_LSB_list1)
    sum_LSB_list2 = sum(Array_LSB_list2)
    sum_LSB_list3 = sum(Array_LSB_list3)
    sum_LSB_list4 = sum(Array_LSB_list4)
    sum_LSB_list5 = sum(Array_LSB_list5)
    sum_LSB_list6 = sum(Array_LSB_list6)
    sum_LSB_list7 = sum(Array_LSB_list7) 
    sum_MSB_list0 = sum(Array_MSB_list0)
    sum_MSB_list1 = sum(Array_MSB_list1)
    sum_MSB_list2 = sum(Array_MSB_list2)
    sum_MSB_list3 = sum(Array_MSB_list3)
    sum_MSB_list4 = sum(Array_MSB_list4)
    sum_MSB_list5 = sum(Array_MSB_list5)
    sum_MSB_list6 = sum(Array_MSB_list6)
    sum_MSB_list7 = sum(Array_MSB_list7) 

    # print (sum_list0)
    # print (sum_list1)

    print ("%s,%s"%('PA0_testedge',sum_list0))                                     # Save PRBS test data edge orginal data and summary data
    np.savetxt("PA0_testedge.txt", Array_list0, fmt = '%d', delimiter=",")
    np.savetxt("PA0_testedge_sum.txt", sum_list0, fmt = '%d', delimiter=",")
    print ("%s,%s"%('PA1_testedge',sum_list1))           
    np.savetxt("PA1_testedge.txt", Array_list1, fmt = '%d', delimiter=",")
    np.savetxt("PA1_testedge_sum.txt", sum_list1, fmt = '%d', delimiter=",")

    print ("%s,%s"%('LSB_edge_D0',sum_LSB_list0))           
    np.savetxt("LSB_edge_D0.txt", Array_LSB_list0, fmt = '%d', delimiter=",")        # Save LSB user channel edge orginal data and summary data
    np.savetxt("LSB_edge_DO_sum.txt", sum_LSB_list0, fmt = '%d', delimiter=",")

    print ("%s,%s"%('LSB_edge_D1',sum_LSB_list1))           
    np.savetxt("LSB_edge_D1.txt", Array_LSB_list1, fmt = '%d', delimiter=",")        
    np.savetxt("LSB_edge_D1_sum.txt", sum_LSB_list1, fmt = '%d', delimiter=",")

    print ("%s,%s"%('LSB_edge_D2',sum_LSB_list2))           
    np.savetxt("LSB_edge_D2.txt", Array_LSB_list2, fmt = '%d', delimiter=",")        
    np.savetxt("LSB_edge_D2_sum.txt", sum_LSB_list2, fmt = '%d', delimiter=",")

    print ("%s,%s"%('LSB_edge_D3',sum_LSB_list3))           
    np.savetxt("LSB_edge_D3.txt", Array_LSB_list3, fmt = '%d', delimiter=",")        
    np.savetxt("LSB_edge_D3_sum.txt", sum_LSB_list3, fmt = '%d', delimiter=",")

    print ("%s,%s"%('LSB_edge_D4',sum_LSB_list4))           
    np.savetxt("LSB_edge_D4.txt", Array_LSB_list4, fmt = '%d', delimiter=",")        
    np.savetxt("LSB_edge_D4_sum.txt", sum_LSB_list4, fmt = '%d', delimiter=",")

    print ("%s,%s"%('LSB_edge_D5',sum_LSB_list5))           
    np.savetxt("LSB_edge_D5.txt", Array_LSB_list5, fmt = '%d', delimiter=",")        
    np.savetxt("LSB_edge_D5_sum.txt", sum_LSB_list5, fmt = '%d', delimiter=",")

    print ("%s,%s"%('LSB_edge_D6',sum_LSB_list6))           
    np.savetxt("LSB_edge_D6.txt", Array_LSB_list6, fmt = '%d', delimiter=",")        
    np.savetxt("LSB_edge_D6_sum.txt", sum_LSB_list6, fmt = '%d', delimiter=",")

    print ("%s,%s"%('LSB_edge_D7',sum_LSB_list7))           
    np.savetxt("LSB_edge_D7.txt", Array_LSB_list7, fmt = '%d', delimiter=",")        
    np.savetxt("LSB_edge_D7_sum.txt", sum_LSB_list7, fmt = '%d', delimiter=",")

    print ("%s,%s"%('MSB_edge_D0',sum_MSB_list0))           
    np.savetxt("MSB_edge_D0.txt", Array_MSB_list0, fmt = '%d', delimiter=",")        # Save MSB user channel edge orginal data and summary data
    np.savetxt("MSB_edge_DO_sum.txt", sum_MSB_list0, fmt = '%d', delimiter=",")

    print ("%s,%s"%('MSB_edge_D1',sum_MSB_list1))           
    np.savetxt("MSB_edge_D1.txt", Array_MSB_list1, fmt = '%d', delimiter=",")        
    np.savetxt("MSB_edge_D1_sum.txt", sum_MSB_list1, fmt = '%d', delimiter=",")

    print ("%s,%s"%('MSB_edge_D2',sum_MSB_list2))           
    np.savetxt("MSB_edge_D2.txt", Array_MSB_list2, fmt = '%d', delimiter=",")        
    np.savetxt("MSB_edge_D2_sum.txt", sum_MSB_list2, fmt = '%d', delimiter=",")

    print ("%s,%s"%('MSB_edge_D3',sum_MSB_list3))           
    np.savetxt("MSB_edge_D3.txt", Array_MSB_list3, fmt = '%d', delimiter=",")        
    np.savetxt("MSB_edge_D3_sum.txt", sum_MSB_list3, fmt = '%d', delimiter=",")

    print ("%s,%s"%('MSB_edge_D4',sum_MSB_list4))           
    np.savetxt("MSB_edge_D4.txt", Array_MSB_list4, fmt = '%d', delimiter=",")        
    np.savetxt("MSB_edge_D4_sum.txt", sum_MSB_list4, fmt = '%d', delimiter=",")

    print ("%s,%s"%('MSB_edge_D5',sum_MSB_list5))           
    np.savetxt("MSB_edge_D5.txt", Array_MSB_list5, fmt = '%d', delimiter=",")        
    np.savetxt("MSB_edge_D5_sum.txt", sum_MSB_list5, fmt = '%d', delimiter=",")

    print ("%s,%s"%('MSB_edge_D6',sum_MSB_list6))           
    np.savetxt("MSB_edge_D6.txt", Array_MSB_list6, fmt = '%d', delimiter=",")        
    np.savetxt("MSB_edge_D6_sum.txt", sum_MSB_list6, fmt = '%d', delimiter=",")
    
    print ("%s,%s"%('MSB_edge_D7',sum_MSB_list7))           
    np.savetxt("MSB_edge_D7.txt", Array_MSB_list7, fmt = '%d', delimiter=",")        
    np.savetxt("MSB_edge_D7_sum.txt", sum_MSB_list7, fmt = '%d', delimiter=",")



    for i in range(3):                                      # if read back data matched with write in data, speaker will make a sound three times
        winsound.Beep(freqency, duration)
        time.sleep(0.01)

    print("Ok!")
#-----------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()
