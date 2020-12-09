#name= Ladi's Midi Fighter3D

import midi
import ui
import sys
import mixer
import transport
import device
import patterns
import mixer
import arrangement
import general
import launchMapPages
import playlist
import math
import utils

#print(transport.__file__)

class MidiControllerConfig():
    
    def __init__(self):
        self.page = 0 #the four buttons at the top
        self.shift = 0 #controls the semitons shifted from C3 + Cset
        self.Cset = 12 #controls what octave or how many semitons away from C3 to be the first loew left note on page 1
        self.root = 36 + self.Cset #sets the rote note of the device
        self.scaleNum = 0 #[Chromatic *0*,Major*1*, minor*2*]
        self.Move = self.Cset + self.shift #tells the program how manne semitones the note should be moved after calculations
        self._shiftUp12_key = [22 + self.Move,28 + self.Move,34 + self.Move,40 + self.Move] #represents notes shifting up an octave
        self._shiftDown12_key = [21 + self.Move,27 + self.Move,33 + self.Move,39 + self.Move] #represets notes that shift down an octave
        self._record_key = [20 + self.Move, 26 + self.Move, 32 + self.Move, 38 + self.Move] #represents notes that controll recording
        self._shiftUp_key = [25 + self.Move,31 + self.Cset,37 + self.Move,43 + self.Move] #represents shifting up one semi
        self._shiftDown_key = [24 + self.Move,30 + self.Move,36 + self.Move,42 + self.Move] #represents shifting down one semi
        self._harm_key = [23 + self.Move,29 + self.Move,35 + self.Move,41 + self.Move] #changes the key you want 
    
    def OnInit(self):
        print('init ready')

    def OnDeInit(self):
        print('deinit ready')
    
    def OnMidiOutMsg(self, event):
        #print(utils.GetNoteName(event.data1), event.note)
        #print(device.midiOutMsg(event.midiId, event.midiChan, event.data1, event.data2))
        #print("scaleNum: ", self.scaleNum)
#----------------------------------------------------------Scale LED's ----------------------------------------------------------------------#
        if self.scaleNum > 0:
            #MAJOR-----------------------
            if self.scaleNum == 1: 
                ui.setHintMsg("Major")
                i = 36
                while i < 100:
                    keyRoot = i % 12
                    if keyRoot == 0 or keyRoot == 2 or keyRoot == 4 or keyRoot == 5 or keyRoot == 7 or keyRoot == 9 or keyRoot == 11:
                        device.midiOutMsg(144, 2,  i, 68)
                        event.handled = True
                    else:  
                        device.midiOutMsg(144, 2,  i, 0)
                        event.handled = True
                    i += 1
              
            #MINOR-------------------------
            if self.scaleNum == 2:
                ui.setHintMsg("Natural Minor")   
                i = 36
                while i < 100:
                    keyRoot = i % 12
                    if keyRoot == 0 or keyRoot == 2 or keyRoot == 3 or keyRoot == 5 or keyRoot == 7 or keyRoot == 8 or keyRoot == 10:
                        device.midiOutMsg(144, 2,  i, 68)
                        event.handled = True
                    else:  
                        device.midiOutMsg(144, 2,  i, 0)
                        event.handled = True
                    i += 1
        #Chromatic------------------------   
        else:
            ui.setHintMsg("Chromatic")
            i = 36
            while i < 100:
                device.midiOutMsg(144, 2, i, 0)
                i += 1
#-------------------------------------------------------------------------------------------------------------------------------------------------------#            
        
    def OnMidiMsg(self, event):
        event.handled = False
        event.velocity = 100 #set all notes velocity to fl studios defualt, which is 100 or 78% of 127 rounded up.

        #print("midi ID:", event.midiId, "Midi Chan: ", event.midiChan, "Data1: ", event.data1,"Data2: ", event.data1, "Port: ", event.port, "Note: ",event.note, "controlNum: ", event.controlNum,"controlVal: ", event.controlVal,"Event: ", event.outEv, "progNum: ", event.progNum, "midiChanEx: ", event.midiChanEx)


#----------------------------------------------------------Controls Note shifting ----------------------------------------------------------------------#
        self.Move = self.Cset + (self.shift) 
        
        #left-side 
        self._shiftUp12_key = [22 + self.Move,28 + self.Move,34 + self.Move,40 + self.Move] 
        self._shiftDown12_key = [21 + self.Move,27 + self.Move,33 + self.Move,39 + self.Move]
        self._record_key = [20 + self.Move, 26 + self.Move, 32 + self.Move, 38 + self.Move]

        #rightside
        self._shiftUp_key = [25 + self.Move,31 + self.Move,37 + self.Move,43 + self.Move]
        self._shiftDown_key = [24 + self.Move,30 + self.Move,36 + self.Move,42 + self.Move]
        self._harm_key = [23 + self.Move,29 + self.Move,35 + self.Move,41 + self.Move]

        
        event.data1 += self.Move #how much each note should be shifted is applied
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
       
       
       
#-------------------------------------------Scales Baby--------------------------------------------------------------------------------------------------#       
        if event.midiId == 0x90 and event.data1 == self._harm_key[self.page]:
            self.scaleNum += 1
            self.scaleNum = self.scaleNum % 3
            OnMidiOutMsg(event)
            event.handled = True
#---------------------------------------------------------------------------------------------------------------------------------------------------------#




#-------------------------------------------------------------Handles what page youre on------------------------------------------------------------------#
        if event.note < self.root:
            event.handled = True

        if event.midiId == 0x90 and event.data1 == 0 + self.Move:
            self.page = 0
            event.handled = True
        if event.midiId == 0x90 and event.data1 == 1 + self.Move:
            self.page = 1
            event.handled = True
        if event.midiId == 0x90 and event.data1 == 2 + self.Move:
            self.page = 2
            event.handled = True
        if event.midiId == 0x90 and event.data1 == 3 + self.Move:
            self.page = 3
            event.handled = True
#-------------------------------------------------------------------------------------------------------------------------------------------------------#








#------------------------------------------------Check if shifting buttons are pressed----------------------------------------------------------------------#
        if event.midiId == 0x90 and event.data1 == self._shiftUp_key[self.page]:
            self.shift += 1
            self.root += 1
            ui.setHintMsg(str(utils.GetNoteName(self.root)))
            event.handled = True
        if event.midiId == 0x90 and event.data1 == self._shiftDown_key[self.page]:
            self.shift -= 1
            self.root -= 1
            ui.setHintMsg(str(utils.GetNoteName(self.root)))
            event.handled = True
        if event.midiId == 0x90 and event.data1 == self._shiftUp12_key[self.page]:
            if event.pmeFlags & midi.PME_System !=0:
                self.shift += 12
                self.root += 12
                ui.setHintMsg(str(utils.GetNoteName(self.root)))
                event.handled = True
        if event.midiId == 0x90 and event.data1 == self._shiftDown12_key[self.page]:
            if event.pmeFlags & midi.PME_System !=0:
                self.shift -= 12
                self.root -= 12
                ui.setHintMsg(str(utils.GetNoteName(self.root)))
                event.handled = True
  #-------------------------------------------------------------------------------------------------------------------------------------------------------#      






  #-------------------------------------------------------------Checks if record button is pressed--------------------------------------------------------#
        if event.midiId == 0x90 and event.data1 == self._record_key[self.page]:
            if event.pmeFlags & midi.PME_System !=0:
                if transport.isRecording() == True and not transport.isPlaying():
                    pass
                else:
                    transport.record()
                transport.start()
                event.handled = True
#---------------------------------------------------------------------------------------------------------------------------------------------------------#


            
            

  

#------------------------------------------------------------Runnig the code-------------------------------------------------------------------------------#
MidiFighter3D = MidiControllerConfig()

def OnInit():
	MidiFighter3D.OnInit()

def OnDeInit():
    MidiFighter3D.OnDeInit()


def OnMidiMsg(event):
    MidiFighter3D.OnMidiMsg(event)

def OnMidiOutMsg(event):
    MidiFighter3D.OnMidiOutMsg(event)
#-------------------------------------------------------------------------------------------------------------------------------------------------------#