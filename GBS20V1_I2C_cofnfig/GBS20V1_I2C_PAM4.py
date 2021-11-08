import pandas as pd
import os
import sys
import time
import winsound
from usb_iss import UsbIss, defs

'''
@author: Peilong Wang
@date: Apr. 7, 2021
This script as a generic I2C cofniguration software to configure I2C slave. The I2C reg configuration data is read into a xxx.dat file.
The UsbIss as I2C master deivce is used to write and read I2C slave register.
'''


def df_form_reg(df):
    rN = []

    l1 = df['V2'][:6].astype('int32')
    # print (l1)
    rN.append(l1[0])
    rN.append(l1[1])
    rN.append(l1[2])
    rN.append(l1[3])
    rN.append(l1[4])
    rN.append(l1[5])

    l2 = df['V1'][:9].astype('int32')
    # print (l2)
    rN.append( l2[0] << 7 | l2[1] << 6 | l2[2] << 5 | l2[3] << 4 | l2[4] << 3 | l2[5] << 2 | l2[6] << 1 | l2[7] )
    rN.append(l2[8])
    
    l3 = df['V1'][9:18].astype('int32').tolist()
    # print (l3)
    rN.append( l3[0] << 7 | l3[1] << 6 | l3[2] << 2 | l3[3] << 1 | l3[4] )
    rN.append( l3[5] << 4 | l3[6] )
    rN.append( l3[7] << 4 | l3[8] )

    l4 = df['V1'][18:].astype('int32').tolist()
    # print (l4)
    rN.append( l4[0] )
    rN.append( l4[1] )
    rN.append( l4[2] << 1 | l4[3] )
    rN.append( l4[4] << 1 | l4[5] )

    l5 = df['V2'][6:].astype('int32').tolist()
    # print (l5)
    rN.append( l5[0] )
    rN.append( l5[1] )
    rN.append( l5[2] << 4 | l5[3] )
    rN.append( l5[4] << 4 | l5[5] )
    rN.append( l5[6] << 4 | l5[7] )
    rN.append( l5[8] << 4 | l5[9] )
    rN.append( l5[10] << 4 | l5[11] )
    rN.append( l5[12] << 4 | l5[13] )
    rN.append( l5[14] << 4 | l5[15] )
    rN.append( l5[16] << 4 | l5[17] )

    l6 = df['V3'][:17].astype('int32').tolist()
    # print (l6)
    rN.append( l6[0] << 4 | l6[1] << 2 | l6[2] << 1 | l6[3] )
    rN.append( l6[4] << 5 | l6[5] << 4 | l6[6] << 3 | l6[7] << 2 | l6[8] << 1 | l6[9] )
    rN.append( l6[10] << 6 | l6[11] << 5 | l6[12] << 4 | l6[13] << 3 | l6[14] << 2 | l6[15] << 1 | l6[16] )

    l7 = df['V3'][17:22].astype('int32').tolist()
    # print (l7)
    rN.append( l7[0] << 5 | l7[1] )
    rN.append( l7[2] )
    rN.append( l7[3] )
    rN.append( l7[4] )

    return rN
    

def read_and_write_user_config(user_config_filename, out_filename):

    df = pd.read_csv(user_config_filename, delim_whitespace=True, names= ['C1', 'V1', 'C2', 'V2', 'C3', 'V3']) 
    # print (df)

    Reg_Val = df_form_reg(df)

    # write out to configuration file
    f = open(out_filename, 'w')
    for i in range(len(Reg_Val)):
        f.write('0x{0:0{1}X}'.format(i,2) + ' ' + '0x{0:0{1}X}'.format(Reg_Val[i],2) )
        f.write('\n')
    f.close()

    return

#-----------------------------------------------------------------------------------#
freqency = 1000
duration = 200
#-----------------------------------------------------------------------------------#
def main():
    user_config_filename = "GBS20V1_user_config.txt"    # need to change by users
    register_filename = "step10_pam4_2V5_IL16_IM16_CTLE0_cap0.txt"   # need to change by users

    COM_Port = "COM4"                           # need to change according com port
    I2C_Addr = 0x20                             # need to change according I2C Addr

    Reg_Addr = []
    Reg_Val = []

    read_and_write_user_config(user_config_filename, register_filename)    # comment out this line if you want to use register_filename directly

    with open(register_filename, 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            Reg_Addr += [int(line.split()[0], 16)]              # read register address and value
            Reg_Val += [int(line.split()[1], 16)]

    for i in range(len(Reg_Addr)):
       print (hex(Reg_Addr[i]), hex(Reg_Val[i]))
    # print (Reg_Addr)
    # print (Reg_Val)

    # set usb-iss iic master device
    iss = UsbIss()
    iss.open(COM_Port)
    iss.setup_i2c(clock_khz=100)

    regWritelen = len(Reg_Addr)
    # print (type(I2C_Addr))
    # print (regWritelen)
    
    # write data into i2c slave
    iss.i2c.write(I2C_Addr, 0, Reg_Val)       
    time.sleep(0.02)
    print (Reg_Val) 


    read_data = []
    for i in range(regWritelen):                              # read data from i2c slave
        read_data += iss.i2c.read(I2C_Addr, Reg_Addr[i], 1)
        time.sleep(0.02)
    print (read_data)

    # compare write in data with read back data
    print('Check write-in registers:')
    for i in range(regWritelen):
        if Reg_Val[i] != read_data[i]:
            print("Read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr[i]), hex(Reg_Val[i]), hex(read_data[i])) )
    print('Write-in data check finished')


    Reg_Addr = []
    print('Read read-only registers:')
    readonlyReg_Addr = [0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26]
    readonlyReg_Val = []
    # readonlyReg_Val = [0x00, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26]
    for i in range(len(readonlyReg_Addr)):                              # read data from i2c slave
        readonlyReg_Val += iss.i2c.read(I2C_Addr, readonlyReg_Addr[i], 1)
        time.sleep(0.02)
    for i in range(len(readonlyReg_Addr)):
        print(hex(readonlyReg_Addr[i]), hex(readonlyReg_Val[i]))


    for i in range(3):                                      # if read back data matched with write in data, speaker will make a sound three times
        winsound.Beep(freqency, duration)
        time.sleep(0.01)

    print("Ok!")
#-----------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()
