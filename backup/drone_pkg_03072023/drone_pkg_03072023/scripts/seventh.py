#!/usr/bin/env python3
import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.reset_input_buffer()
    while True:
        line1 = ser.readline().decode('utf-8').rstrip()
        if(len(line1)==13 and line1[6]=='_' and line1[12]=='/'):
            line2 = line1.split('_')
    
            cable_ph1 =line2[0]
            cable_ph2 = str(cable_ph1[1:6])
            cable_ph  = int(cable_ph2) - 50000
            
            cable_th1 =line2[1]
            cable_th2 = str(cable_th1[0:5])
            cable_th  = int(cable_th2) - 50000
            print(str(cable_ph)+" "+str(cable_th))
        time.sleep(0.001)
