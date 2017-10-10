# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 19:36:33 2017

@author: neutron
"""

try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu

import serial
import time
import thread

SERIAL_PORT = "COM47"
BAUD_RATE = 57600
READ_TIMEOUT = 3 #seconds
init_time_out_period = 10 #Initialisation time of device in seconds

port = serial.Serial(SERIAL_PORT,baudrate=BAUD_RATE,timeout=READ_TIMEOUT)

voltageValue=''

class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('./pps_gui_test.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('Frame_1', master)
        
        self.DataBox = builder.get_object('Entry_2', master)
        
        self.Label = builder.get_object('Label_1', master)


def port_init():
    #wait until Port is open
    while port.isOpen() == False:
        pass
    
    print "Serial Port Configuration: "+port.name+" @ "+str(BAUD_RATE) + " Read Timeout: "+str(READ_TIMEOUT)+"s"
    
    port.readlines()
    """
    line = "no"
    
    starting_time = time.time()
    while line != "OK\r\n":
        port.write(b"govt\r")
        line = port.readline()
        if(time.time() - starting_time > init_time_out_period):
                #print "Device Not responding, check firmware or Connection"
                raise Exception("DEVICE_NOT_RESPONDING")
    """


def updateDataBox():
    global app
    print "volts: "+str(voltageValue)
    app.Label.config(text=voltageValue)
    #app.DataBox.config(text=str(voltageValue))


def readData():
    global voltageValue
    global runThread
    readIntervals = 0.1#seconds
    currentTimeStamp = 0    
    while runThread==True:
        if time.time()-currentTimeStamp > readIntervals:
            print "sending cmd"        
            port.write('govt\r')
            time.sleep(0.01)#wait for 100ms
            data = port.readlines(5)#this is 5 bytes; OK\r\n is 4 bytes which is first line
            #so it will read OK\r\n and the next line.
            print "data read is: "+str(data)        
            if data[0].strip('\r\n') == 'OK':
                voltageValue = data[1].strip('\r\n')+'V'
            else:
                print 'readError!'
            
            updateDataBox()
            #update timeStamp for loop to continue after delay
            currentTimeStamp = time.time()





if __name__ == "__main__":
    try:
        port_init()
        print "Device Initialised"
        
        root = tk.Tk()
        app = Application(root)
        
        app.Label.config(text='Volts')
        
        #have not been able to write into databox yet, need to check that
        app.DataBox.insert(0,'Volts')
        #we have to use insert and delete methods of Databox/Entry
        #so my understanding is that we should stick to labels for displaying text
        #instead make background white and use a font commonly available on
        #windows and linux which is royalty free.        
        
        print str(app.DataBox.keys())

        runThread=True
        thread.start_new_thread(readData,())
        print "Started logging data"
        
        #font has been set to Arial but I think I need to find a font
        #which looks good on both linux and windows and has customisations
        #available like sizes, italics etc        
        root.mainloop()
        #root.destroy() # optional; see description below
        runThread = False
        
        #close Serial Port
        port.close()
    
    except Exception as e:
        print "There has been an Exception, find details below:"        
        print str(e)        
        if(port.isOpen()):
            print "Closing Port"
            port.close()