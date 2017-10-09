# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 23:27:28 2017

@author: neutron

This is the PPS Control Panel application code:

We need to add a signal to Serial Port selection Combobox to rescan available
ports as soon as we click on it.

and once the port is selected we need to derive its info and display it in the 
label above it by updating the label text

Automatically fill the port combobox with first available port or smallest port 
on load or create an Ini file to save last used port and load from it in the beginning.
if any last saved port info is available in ini file then load it, otherwise load
the first available port in the system.

if the port is present then display its info otherwise show port not connected/not found
the connect mechanism should be capable of handling and displaying connectivity failures.


By default Voltage and current should be ticked and Power should unticked.

Battery voltage and device uptime should be polled less frequently

all uart polling functions should be in same thread so that we there is arbitration of
commands.

Device settings check boxes should have signals attached to them to perform actions.


use tkFileDialog to choose logging file name and path and display the path in the 
entry box.

use serial.tools.list_ports.comports generator to get available ports and its properties


use the checkboxes called display to control logging traces and plotting also.
if display doesn't sound fit in here we can change the string to acquire.

When Plotting we need to stop updating the values in main screen.
Probably we should do it while logging also, as it will help in acquiring faster.


once logging starts Display checkboxes should be grayed out.

The check boxes in plotting group will be superseeded by the checkboxes in display
group.

Those enabled in there only will be enabled in here.

However since the data of plot will be displayed from the log file which is a temporary
file it will be the same file as log file just in different name.
So when we click save log file it will just create this file in that location
rather then in the same folder were it is running and will have user given name.


"""
import Tkinter as tk  # for python 2
import tkFileDialog
import pygubu

DEBUG = 0

#import serial
import time
import thread
import serial.tools.list_ports

class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('./pps_control_panel.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('Frame_1', master)
        
        self.chooseLogFileBtn = builder.get_object('Button_9', master)
        self.LogFileEntryBox = builder.get_object('Entry_5', master)
        self.selectPortComboBox = builder.get_object('Combobox_1', master)
        self.comboBoxTextVar = ''
        self.PortInfoLabel = builder.get_object('Label_12', master)
        
def guiInit(mainApp):
    mainApp.chooseLogFileBtn.config(command=selectLogFile)
    portDict = enumerateSerialPorts()
    portList = portDict.keys()
    portList.sort()
    if DEBUG == 1:
        print str(portList)
    mainApp.selectPortComboBox.config(textvariable=mainApp.comboBoxTextVar,values=portList)
    mainApp.selectPortComboBox.set(portList[0])
    comboBoxSelected(1)
    mainApp.selectPortComboBox.bind('<<ComboboxSelected>>', comboBoxSelected)
    

def comboBoxSelected(event):   
    global app
    portSelected = app.selectPortComboBox.get()
    portDict = enumerateSerialPorts()
    portInfo = ''    
    if portDict.has_key(portSelected):
        portInfo = 'Port Info: '+str(portDict.get(portSelected))
    else:
        portInfo = 'Port Info: '+str(portSelected)+' Not Found!'
    app.PortInfoLabel.config(text=portInfo)
    


def enumerateSerialPorts():
    portDict = {}
    for port, desc, hwid in serial.tools.list_ports.comports():
        portDict[str(port)] = desc
    return portDict

def selectLogFile():
    fileName = tkFileDialog.asksaveasfilename(defaultextension=".csv")
    global app
    app.LogFileEntryBox.delete(0,tk.END)
    app.LogFileEntryBox.insert(0,fileName)
    return fileName


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = Application(root)
        guiInit(app)
        if DEBUG == 1:        
            print str(app.selectPortComboBox.get())
        root.mainloop()
        
    except Exception as e:
        print "There has been an Exception, find details below:"        
        print str(e)        