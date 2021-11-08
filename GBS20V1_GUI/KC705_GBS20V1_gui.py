import pandas as pd
import os
import sys
import time
import winsound
import socket
#from usb_iss import UsbIss, defs
from command_interpret import *
from tkinter import *

'''
@author: Peilong Wang, Lily Zhang 
@date: Oct. 12, 2021
'''

hostname = '192.168.2.3'					#FPGA IP address
port = 1024									#port number
#-----------------------------------------------------------------------------------#
freqency = 1000
duration = 200
#-----------------------------------------------------------------------------------#

## IIC write slave device
# @param mode[1:0] : '0'is 1 bytes read or wirte, '1' is 2 bytes read or write, '2' is 3 bytes read or write
# @param slave[7:0] : slave device address
# @param wr: 1-bit '0' is write, '1' is read
# @param reg_addr[7:0] : register address
# @param data[7:0] : 8-bit write data
def iic_write(mode, slave_addr, wr, reg_addr, data):
    val = mode << 24 | slave_addr << 17 | wr << 16 | reg_addr << 8 | data
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.01)
    cmd_interpret.write_pulse_reg(0x0001)           # reset ddr3 data fifo
    time.sleep(0.01)
    
#--------------------------------------------------------------------------#
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

#--------------------------------------------------------------------------#
#--------------------------------Create GUI ------------------------------ #
#--------------------------------------------------------------------------#
def main():    
#---------------------------------------------------------------------------#
    root = Tk()
    root.title("GBS20V1 GUI")

    Title = Label(root, text="GBS20V1 GUI", font='Helvetica 18 bold')
    Title.grid(row=28, column=12,columnspan=4)

    # creating a label widget
    LSBLabel = Label(root, text="LSB channel", font='Helvetica 12 bold')
    MSBLabel = Label(root, text="MSB channel", font='Helvetica 12 bold')
    # shoving it onto screen
    LSBLabel.grid(row=29, column=95,columnspan=4)
    MSBLabel.grid(row=39, column=95,columnspan=4)
    ch_item = ['CH' + str(i) for i in range(7, -1, -1)]

    lsb_ch_lb = {}
    for i in range(len(ch_item)):
        lsb_ch_lb[ch_item[i]] = Label(root, text=ch_item[i] )
    for i,lb in enumerate(lsb_ch_lb):
        lsb_ch_lb[lb].grid(row=i+31, column=93)

    lsb_msb_item = ["eRxEn", "eRxEqu1", "eRxEqu0", "PAdisCH", "PAphase", "mask"]#, "EdgeRead"]

    lsb_lb = {}
    for i in range(len(lsb_msb_item)):
        lsb_lb[lsb_msb_item[i]] = Label(root, text=lsb_msb_item[i] )
    for i,lb in enumerate(lsb_lb):
        lsb_lb[lb].grid(row=30, column=94+i)

    lsb_entry = {}
    for item in lsb_msb_item:
        lsb_entry[item] = []
    for index, key in enumerate(lsb_entry):
        for i in range(len(ch_item)):
            lsb_entry[key].append( Entry(root, width=3) )
            lsb_entry[key][i].grid(row=i+31, column=index+94, padx=3, pady=3)
            lsb_entry[key][i].insert(END, str(0))


    msb_ch_lb = {}
    for i in range(len(ch_item)):
        msb_ch_lb[ch_item[i]] = Label(root, text=ch_item[i] )
    for i,lb in enumerate(msb_ch_lb):
        msb_ch_lb[lb].grid(row=i+41, column=93)

    msb_lb = {}
    for i in range(len(lsb_msb_item)):
        msb_lb[lsb_msb_item[i]] = Label(root, text=lsb_msb_item[i] )
    for i,lb in enumerate(msb_lb):
        msb_lb[lb].grid(row=40, column=94+i)

    msb_entry = {}
    for item in lsb_msb_item:
        msb_entry[item] = []
    for index, key in enumerate(msb_entry):
        for i in range(len(ch_item)):
            msb_entry[key].append( Entry(root, width=3) )
            msb_entry[key][i].grid(row=i+41, column=index+94, padx=3, pady=3)
            msb_entry[key][i].insert(END, str(0))


    FbDivLabel = Label(root, text="FbDiv", font='Helvetica 12 bold')
    FbDiv_item = ['enTestClk1G28', 'FbDiv_enPAClk1G28', 'FbDiv_skip', 'FbDiv_enSer']
    FbDiv_default = [1,0,0,1]
    FbDiv_lb = {}
    for i in range(len(FbDiv_item)):
        FbDiv_lb[FbDiv_item[i]] = Label(root, text=FbDiv_item[i] )

    FbDivLabel.grid(row=34, column=2)
    for i,lb in enumerate(FbDiv_lb):
        FbDiv_lb[lb].grid(row=i+35, column=2)

    FbDiv_entry = []
    for i in range(len(FbDiv_item)):
        FbDiv_entry.append( Entry(root, width=3) )
        FbDiv_entry[i].grid(row=i+35, column=3, padx=3, pady=3)
        FbDiv_entry[i].insert(END, str(FbDiv_default[i]))

    AFCLabel = Label(root, text="AFC", font='Helvetica 12 bold')
    AFC_item = ['AFC_Start', 'AFC_RST', 'AFC_overriseCtrl', 'AFC_OverrideCtrl_val1<5:0>']
    AFC_default = [0,0,1,20]
    AFC_lb = {}
    for i in range(len(AFC_item)):
        AFC_lb[AFC_item[i]] = Label(root, text=AFC_item[i] )

    AFCLabel.grid(row=40, column=2)
    for i,lb in enumerate(AFC_lb):
        AFC_lb[lb].grid(row=i+41, column=2)

    AFC_entry = []
    for i in range(len(AFC_item)):
        AFC_entry.append( Entry(root, width=3) )
        AFC_entry[i].grid(row=i+41, column=3, padx=3, pady=3)
        AFC_entry[i].insert(END, str(AFC_default[i]))


    PLLLabel = Label(root, text="PLL", font='Helvetica 12 bold')
    PLL_item = ['PLL_ENABL EPLL', 'PLL_vcoDAC<3:0>', 'PLL_vcoRailMode', 'PLL_overrideVc', 'PLL_BIASGEN_CONFIG<3:0>', 'PLL_CONFIG_I_PLL<3:0>', 'PLL_CONFIG_P_PLL<3:0>', 'PLL_PLL_R_CONFIG<3:0>']
    PLL_default = [1,8,1,0,8,10,10,8]
    PLL_lb = {}
    for i in range(len(PLL_item)):
        PLL_lb[PLL_item[i]] = Label(root, text=PLL_item[i] )

    PLLLabel.grid(row=30, column=5)
    for i,lb in enumerate(PLL_lb):
        PLL_lb[lb].grid(row=i+31, column=5)

    PLL_entry = []
    for i in range(len(PLL_item)):
        PLL_entry.append( Entry(root, width=3) )
        PLL_entry[i].grid(row=i+31, column=6, padx=3, pady=3)
        PLL_entry[i].insert(END, str(PLL_default[i]))

    ENCLabel = Label(root, text="ENC", font='Helvetica 12 bold')
    ENC_item = ['ENC_seedLSB<6:0>', 'Enc_Rst', 'ENC_seedMSB<6:0>', 'Enc_Enable']
    ENC_default = [67,1,22,1]
    ENC_lb = {}
    for i in range(len(ENC_item)):
        ENC_lb[ENC_item[i]] = Label(root, text=ENC_item[i] )

    ENCLabel.grid(row=40, column=5)
    for i,lb in enumerate(ENC_lb):
        ENC_lb[lb].grid(row=i+41, column=5)

    ENC_entry = []
    for i in range(len(ENC_item)):
        ENC_entry.append( Entry(root, width=3) )
        ENC_entry[i].grid(row=i+41, column=6, padx=3, pady=3)
        ENC_entry[i].insert(END, str(ENC_default[i]))

    PALabel = Label(root, text="PA", font='Helvetica 12 bold')
    PA_item = ['PA_cpcurrent<3:0>', 'PA_dllstartVoltage<1:0>', 'PA0_clkInvert', 'PA0_edgeResetN', 'PA0_enEdgeDetect', 'PA0_dllFD', 'PA0_dllcapReset', 'PA0_dllEn', 'PA1_clkInvert','PA1_edgeResetN', 'PA1_enEdgeDetect', 'PA1_dllFD', 'PA1_dllcapReset', 'PA1_dllEn']
    PA_default = [4,1,0,0,1,0,0,0,0,1,0,0,0,0]
    PA_lb = {}
    for i in range(len(PA_item)):
        PA_lb[PA_item[i]] = Label(root, text=PA_item[i] )

    PALabel.grid(row=30, column=10)
    for i,lb in enumerate(PA_lb):
        PA_lb[lb].grid(row=i+31, column=10)

    PA_entry = []
    for i in range(len(PA_item)):
        PA_entry.append( Entry(root, width=3) )
        PA_entry[i].grid(row=i+31, column=11, padx=3, pady=3)
        PA_entry[i].insert(END, str(PA_default[i]))


    CoreLabel = Label(root, text="Core", font='Helvetica 12 bold')
    Core_item = ['Core_Sel2V5', 'Core_disLA', 'Core_disCombine', 'Core_CTLE<2:0>', 'Core_capLoad<4:0>', 'Core_iLSBSel<4:0>', 'Core_iMSBSel<4:0>', 'IBIAS_BIAS<4:0>']
    Core_default = [1,0,0,0,0,16,16,0]
    Core_lb = {}
    for i in range(len(Core_item)):
        Core_lb[Core_item[i]] = Label(root, text=Core_item[i] )

    CoreLabel.grid(row=30, column=12)
    for i,lb in enumerate(Core_lb):
        Core_lb[lb].grid(row=i+31, column=12)

    Core_entry = []
    for i in range(len(Core_item)):
        Core_entry.append( Entry(root, width=3) )
        Core_entry[i].grid(row=i+31, column=13, padx=3, pady=3)
        Core_entry[i].insert(END, str(Core_default[i]))


    StartupLabel = Label(root, text="Startup", font='Helvetica 12 bold')
    Startup_item = ['RefClk_enRx', 'Ser_txDataRate']
    Startup_default = [1,1]
    Startup_lb = {}
    for i in range(len(Startup_item)):
        Startup_lb[Startup_item[i]] = Label(root, text=Startup_item[i] )

    StartupLabel.grid(row=30, column=2)
    for i,lb in enumerate(Startup_lb):
        Startup_lb[lb].grid(row=i+31, column=2)

    Startup_entry = []
    for i in range(len(Startup_item)):
        Startup_entry.append( Entry(root, width=3) )
        Startup_entry[i].grid(row=i+31, column=3, padx=3, pady=3)
        Startup_entry[i].insert(END, str(Startup_default[i]))


    Run_item = ['Port', 'I2C']
    Run_default = ['COM5', '0x20']
    Run_lb = {}
    for i in range(len(Run_item)):
        Run_lb[Run_item[i]] = Label(root, text=Run_item[i], fg='red' )

    for i,lb in enumerate(Run_lb):
        Run_lb[lb].grid(row=i+46, column=2)

    Run_entry = []
    for i in range(len(Run_item)):
        Run_entry.append( Entry(root, width=7) )
        Run_entry[i].grid(row=i+46, column=3, padx=5, pady=5)
        Run_entry[i].insert(END, Run_default[i])

    # readonly section
    ReadonlyLabel = Label(root, text="Readonly", font='Helvetica 12 bold')
    Readonly_item = ['AFCcalCap<5:0>', 'AFCbusy', 'INSTLOCK_PLL', 'PA0_testEdge<0>', 'PA1_testEdge<0>'] 
    Readonly_lb = {}
    for i in range(len(Readonly_item)):
        Readonly_lb[Readonly_item[i]] = Label(root, text=Readonly_item[i] )
    ReadonlyLabel.grid(row=31, column=101)
    # ReadonlyLabel.grid(row=29, column=100)
    for i,lb in enumerate(Readonly_lb):
        Readonly_lb[lb].grid(row=i+34, column=101)

    Readonly_var = [] # readonly value
    for i in range(len(Readonly_item)):
        Readonly_var.append( StringVar() )
        Readonly_var[i].set('0')
    Readonly_var_lb = {}
    for i in range(len(Readonly_item)):
        Readonly_var_lb[Readonly_item[i]] = Label(root, textvariable = Readonly_var[i], padx=15 )
    for i,lb in enumerate(Readonly_var_lb):
        Readonly_var_lb[lb].grid(row=i+34, column=102)

    # readonly2 section
    Readonly2_item = ['PA0_edge<7:0>']
    Readonly2_lb = {}
    ## shoving readonly2 label to screen
    for i in range(len(Readonly2_item)):
        Readonly2_lb[Readonly2_item[i]] = Label(root, text=Readonly2_item[i] )
    for i,lb in enumerate(Readonly2_lb): 
        Readonly2_lb[lb].grid(row=30, column=104+i)

    ## shoving ch* lable to screen
    Readonly2_ch_lb = {}
    for i in range(len(ch_item)):
        Readonly2_ch_lb[ch_item[i]] = Label(root, text=ch_item[i] )
    for i,lb in enumerate(Readonly2_ch_lb): 
        Readonly2_ch_lb[lb].grid(row=i+31, column=103)

    ## create readonly2 
    Readonly2_var = {} 
    for item in Readonly2_item:
        Readonly2_var[item] = []
    for index, key in enumerate(Readonly2_var):
        for i in range(len(ch_item)):
            Readonly2_var[key].append( StringVar() )
            Readonly2_var[key][i].set('0')
    ## shoving readonly2 value to screen
    Readonly2_var_lb = {} 
    for item in Readonly2_item:
        Readonly2_var_lb[item] = []
    for index, key in enumerate(Readonly2_var_lb):
        for i in range(len(ch_item)):
            Readonly2_var_lb[key].append( Label(root, textvariable = Readonly2_var[key][i], borderwidth=5) )
            Readonly2_var_lb[key][i].grid(row=i+31, column=index+104, padx=3, pady=3)

    # readonly3 section
    Readonly3_item = ['PA1_edge<7:0>']
    Readonly3_lb = {}
    # shoving readonly2 label to screen
    for i in range(len(Readonly3_item)):
        Readonly3_lb[Readonly3_item[i]] = Label(root, text=Readonly3_item[i] )
    for i,lb in enumerate(Readonly3_lb): 
        Readonly3_lb[lb].grid(row=40, column=104+i)

    ## shoving ch* lable to screen
    Readonly3_ch_lb = {}
    for i in range(len(ch_item)):
        Readonly3_ch_lb[ch_item[i]] = Label(root, text=ch_item[i] )
    for i,lb in enumerate(Readonly3_ch_lb): 
        Readonly3_ch_lb[lb].grid(row=i+41, column=103)

    ## create readonly2 
    Readonly3_var = {} 
    for item in Readonly3_item:
        Readonly3_var[item] = []
    for index, key in enumerate(Readonly3_var):
        for i in range(len(ch_item)):
            Readonly3_var[key].append( StringVar() )
            Readonly3_var[key][i].set('0')
    ## shoving readonly2 value to screen
    Readonly3_var_lb = {} 
    for item in Readonly3_item:
        Readonly3_var_lb[item] = []
    for index, key in enumerate(Readonly3_var_lb):
        for i in range(len(ch_item)):
            Readonly3_var_lb[key].append( Label(root, textvariable = Readonly3_var[key][i], borderwidth=5) )
            Readonly3_var_lb[key][i].grid(row=i+41, column=index+104, padx=3, pady=3)


    # I2C status 
    I2C_writein = StringVar()
    I2C_writein.set('Status: None')
    I2C_writein_lb = Label(root, textvariable = I2C_writein, borderwidth=5)
    I2C_writein_lb.grid(row=48, column=5)

    def gui_form_reg():
        rN = []

        # REG_00 to 05
        l = []
        for e in lsb_entry["eRxEn"]:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( l[0] << 7 | l[1] << 6 | l[2] << 5 | l[3] << 4 | l[4] << 3 | l[5] << 2 | l[6] << 1 | l[7] )

        l = []
        for e in msb_entry["eRxEn"]:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( l[0] << 7 | l[1] << 6 | l[2] << 5 | l[3] << 4 | l[4] << 3 | l[5] << 2 | l[6] << 1 | l[7] )

        l = []
        for e in lsb_entry["eRxEqu1"]:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( l[0] << 7 | l[1] << 6 | l[2] << 5 | l[3] << 4 | l[4] << 3 | l[5] << 2 | l[6] << 1 | l[7] )

        l = []
        for e in msb_entry["eRxEqu1"]:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( l[0] << 7 | l[1] << 6 | l[2] << 5 | l[3] << 4 | l[4] << 3 | l[5] << 2 | l[6] << 1 | l[7] )

        l = []
        for e in lsb_entry["eRxEqu0"]:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( l[0] << 7 | l[1] << 6 | l[2] << 5 | l[3] << 4 | l[4] << 3 | l[5] << 2 | l[6] << 1 | l[7] )

        l = []
        for e in msb_entry["eRxEqu0"]:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( l[0] << 7 | l[1] << 6 | l[2] << 5 | l[3] << 4 | l[4] << 3 | l[5] << 2 | l[6] << 1 | l[7] )

        # REG_06 to 07
        l = []
        for e in FbDiv_entry:
            l.append( e.get() )
        l = [int(i) for i in l]
        rFbDiv = l[0] << 3 | l[1] << 2 | l[2] << 1 | l[3]

        rRefClk = int( Startup_entry[0].get() )

        l = []
        for e in AFC_entry:
            l.append( e.get() )
        l = [int(i) for i in l]
        rAFC = l[0] << 2 | l[1] << 1 | l[2]
        rAFC_Overide = l[3]

        rN.append( rFbDiv << 4 | rRefClk << 3 | rAFC )
        rN.append( rAFC_Overide )

        # REG_08 to 0A
        rSer_tx = int( Startup_entry[1].get() )

        l = []
        for e in PLL_entry:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( rSer_tx << 7 | l[0] << 6 | l[1] << 2 | l[2] << 1 | l[3] )
        rN.append( l[4] << 4 | l[5] )
        rN.append( l[6] << 4 | l[7] )

        # REG_0B to 0C
        l = []
        for e in lsb_entry["mask"]:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( l[0] << 7 | l[1] << 6 | l[2] << 5 | l[3] << 4 | l[4] << 3 | l[5] << 2 | l[6] << 1 | l[7] )

        l = []
        for e in msb_entry["mask"]:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( l[0] << 7 | l[1] << 6 | l[2] << 5 | l[3] << 4 | l[4] << 3 | l[5] << 2 | l[6] << 1 | l[7] )

        # REG_0D to 0E
        l = []
        for e in ENC_entry:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( l[0] << 1 | l[1] )
        rN.append( l[2] << 1 | l[3] )

        # REG_0F to 10
        l = []
        for e in lsb_entry["PAdisCH"]:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( l[0] << 7 | l[1] << 6 | l[2] << 5 | l[3] << 4 | l[4] << 3 | l[5] << 2 | l[6] << 1 | l[7] )

        l = []
        for e in msb_entry["PAdisCH"]:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( l[0] << 7 | l[1] << 6 | l[2] << 5 | l[3] << 4 | l[4] << 3 | l[5] << 2 | l[6] << 1 | l[7] )

        # REG_11 to 14
        l = []
        for e in lsb_entry["PAphase"]:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( l[6] << 4 | l[7] )
        rN.append( l[4] << 4 | l[5] )
        rN.append( l[2] << 4 | l[3] )
        rN.append( l[0] << 4 | l[1] )

        # REG_15 to 18
        l = []
        for e in msb_entry["PAphase"]:
            l.append( e.get() )
        l = [int(i) for i in l]
        rN.append( l[6] << 4 | l[7] )
        rN.append( l[4] << 4 | l[5] )
        rN.append( l[2] << 4 | l[3] )
        rN.append( l[0] << 4 | l[1] )

        # REG_19 to 1B
        l_PA = []
        for e in PA_entry:
            l_PA.append( e.get() )
        l_PA = [int(i) for i in l_PA]

        # REG_1C
        l_Core = []
        for e in Core_entry:
            l_Core.append( e.get() )
        l_Core = [int(i) for i in l_Core]

        rN.append( l_PA[0] << 4 | l_PA[1] << 2 | l_PA[8] << 1 | l_PA[2] )
        rN.append( l_Core[0] << 5 | l_PA[3] << 4 | l_PA[4] << 3 | l_PA[5] << 2 | l_PA[6] << 1 | l_PA[7] )
        rN.append( l_Core[1] << 6 | l_Core[2] << 5 | l_PA[9] << 4 | l_PA[10] << 3 | l_PA[11] << 2 | l_PA[12] << 1 | l_PA[13] )
        rN.append( l_Core[3] << 5 | l_Core[4] )
        rN.append( l_Core[5] )
        rN.append( l_Core[6] )
        rN.append( l_Core[7] )

        # print (rN)
        for i in range(len(rN)):
            print('0x{0:0{1}X}'.format(i,2) + ' ' + '0x{0:0{1}X}'.format(rN[i],2) )

        print ('End')

        return rN


    def write_user_config(Reg_Val, out_filename):
        # write out to configuration file
        f = open(out_filename, 'w')
        for i in range(len(Reg_Val)):
            f.write('0x{0:0{1}X}'.format(i,2) + ' ' + '0x{0:0{1}X}'.format(Reg_Val[i],2) )
            f.write('\n')
        f.close()

        return
    # May have problem, set COM_Port, becasue we no need use com_port in here.
    def button_read():
        COM_Port = Run_entry[0].get()
        I2C_Addr = int(Run_entry[1].get(), 0)

        # # set usb-iss iic master device
        # iss = UsbIss()
        # iss.open(COM_Port)
        # iss.setup_i2c(clock_khz=100)


        # check read-only register data
        print('Read read-only registers:')
        readonlyReg_Addr = [0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26]
        readonlyReg_Val = []
        for i in range(len(readonlyReg_Addr)):                              # read data from i2c slave
            #readonlyReg_Val += iss.i2c.read(I2C_Addr, readonlyReg_Addr[i], 1)
            #iic_write(1, I2C_Addr, 0,  Reg_Addr0[i], Reg_Val0[i])
            #read_data1 += [iic_read(0, I2C_Addr, 1, Reg_Addr1[i] )]
            readonlyReg_Val += [iic_read(0, I2C_Addr, 1, readonlyReg_Addr[i] )]
            time.sleep(0.5)
        for i in range(len(readonlyReg_Addr)):
            print(hex(readonlyReg_Addr[i]), hex(readonlyReg_Val[i]))

        # 'AFCcalCap<5:0>', 'AFCbusy', 'INSTLOCK_PLL', 'PA0_testEdge<0>', 'PA1_testEdge<0>'
        global Readonly_var 
        Readonly_var[0].set( str(readonlyReg_Val[0]) )
        Readonly_var[1].set( str(readonlyReg_Val[1]) )
        Readonly_var[2].set( str(readonlyReg_Val[2]) )
        Readonly_var[3].set( str(readonlyReg_Val[5]) )
        Readonly_var[4].set( str(readonlyReg_Val[6]) )

        PA0_binary = '{0:08b}'.format(readonlyReg_Val[3])
        global Readonly2_var
        for i in range(8):
            Readonly2_var[Readonly2_item[0]][i].set( PA0_binary[i] )

        PA1_binary = '{0:08b}'.format(readonlyReg_Val[4])
        global Readonly3_var
        for i in range(8):
            Readonly3_var[Readonly3_item[0]][i].set( PA1_binary[i] )

        return

    def button_run():
        # get entry values from GUI
        Reg_Val = gui_form_reg()

        register_filename = "GBS20V1_gui_register_config.txt"   # need to change by users

        COM_Port = Run_entry[0].get()
        I2C_Addr = int(Run_entry[1].get(), 0)                             # need to change according I2C Addr
        print (COM_Port, I2C_Addr)

        # Write GUI value to txt
        write_user_config(Reg_Val, register_filename)    
        

        Reg_Addr = []
        Reg_Val = []

        with open(register_filename, 'r') as infile:                  # read configuration file
            for line in infile.readlines():
                Reg_Addr += [int(line.split()[0], 16)]              # read register address and value
                Reg_Val += [int(line.split()[1], 16)]

        regWritelen = len(Reg_Addr)
        print ('I2C Addr:',hex(I2C_Addr))
        #print (regWritelen)
        
        print ('Reg Addr:')
        print (Reg_Addr)
        print ('Write-in Reg values:')
        print (Reg_Val)

        # # set usb-iss iic master device
        # iss = UsbIss()
        # iss.open(COM_Port)
        # iss.setup_i2c(clock_khz=100)

        # write data into i2c slave
        #[iic_read(0, I2C_Addr, 1, Reg_Addr1[i] )]
        #iic_write(1, I2C_Addr, 0,  Reg_Addr0[i], Reg_Val0[i])
        #iss.i2c.write(I2C_Addr, 0, Reg_Val)
        for i in range(regWritelen): 
            iic_write(1, I2C_Addr, 0,  Reg_Addr[i], Reg_Val[i])       
            time.sleep(0.02)

        read_data = []
        for i in range(regWritelen):                              # read data from i2c slave
            #read_data += iss.i2c.read(I2C_Addr, Reg_Addr[i], 1)
            read_data += [iic_read(0, I2C_Addr, 1, Reg_Addr[i] )]
            time.sleep(0.02)

        print ('Read-back Reg values:')   
        print (read_data)
        # compare write in data with read back data
        errFlag = 0
        print('Check write-in and Read-back data:')
        for i in range(regWritelen):
            if Reg_Val[i] != read_data[i]:
                print("ERROR! Read-back didn't match with write-in: {} {} {}".format(hex(Reg_Addr[i]), hex(Reg_Val[i]), hex(read_data[i])) )
                errFlag = 1

        # if write-in successful, sound once, else sound 3 times
        global I2C_writein
        if errFlag == 0:
            I2C_writein.set('Passed')
            for i in range(3): 
                winsound.Beep(freqency, duration)
                time.sleep(0.01)
        else: 
            I2C_writein.set('Error')
            for i in range(5): 
                winsound.Beep(freqency, duration)
                time.sleep(0.01)


        print("PASS!")
        print("**********************************************************************************")

        return 

    bt_run = Button(root, text='Run', fg='red', command=button_run, pady=15)
    bt_run.grid(row=46, column=5, rowspan=2)


    bt_run = Button(root, text='Read', fg='blue', command=button_read, pady=15)
    bt_run.grid(row=32, column=101,rowspan=2)


    root.mainloop()
#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#
if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#initial socket
    s.connect((hostname, port))								#connect socket
    cmd_interpret = command_interpret(s)					#Class instance
    main()													#execute main function
    s.close()												#close socket

