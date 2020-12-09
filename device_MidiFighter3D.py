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

#print(midi.__file__)

class MidiControllerConfig():
    
    def __init__(self):
        self.page = 0 #the four buttons at the top
        self.shift = 0 #controls the semitons shifted from C3 + Cset
        self.Cset = 12 #controls what octave or how many semitons away from C3 to be the first loew left note on page 1
        self.root = 36 + self.Cset #sets the rote note of the device
        self.Move = self.Cset + self.shift #tells the program how manne semitones the note should be moved after calculations
        self._shiftUp12_key = [22 + self.Move,28 + self.Move,34 + self.Move,40 + self.Move] #represents notes shifting up an octave
        self._shiftDown12_key = [21 + self.Move,27 + self.Move,33 + self.Move,39 + self.Move] #represets notes that shift down an octave
        self._record_key = [20 + self.Move, 26 + self.Move, 32 + self.Move, 38 + self.Move] #represents notes that controll recording
        self._shiftUp_key = [25 + self.Move,31 + self.Cset,37 + self.Move,43 + self.Move] #represents shifting up one semi
        self._shiftDown_key = [24 + self.Move,30 + self.Move,36 + self.Move,42 + self.Move] #represents shifting down one semi
    def OnInit(self):
        print('init ready')

    def OnDeInit(self):
        print('deinit ready')
    
    def OnMidiOutMsg(self, event):
        #print(utils.GetNoteName(event.data1), event.note)
        #device.midiOutSysex(bytes([0xF0, 0x00, 0x20, 0x6B, 0x7F, 0x42]) + bytes([0xF7]))
        pass

    def OnMidiMsg(self, event):
        event.handled = False
        event.velocity = 100 #set all notes velocity to fl studios defualt, which is 100 or 78% of 127 rounded up.

        #print(event.handled, event.midiId, event.midiChan, event.data1, event.data2)
        print("midi ID:", event.midiId,"Data: ", event.data1, "Port: ", event.port, "Note: ",event.note, "controlNum: ", event.controlNum,"controlVal: ", event.controlVal,"Event: ", event.outEv)


#----------------------------------------------------------Controls Note shifting ----------------------------------------------------------------------#
        self.Move = self.Cset + (self.shift) 
        self._shiftUp12_key = [22 + self.Move,28 + self.Move,34 + self.Move,40 + self.Move] 
        self._shiftDown12_key = [21 + self.Move,27 + self.Move,33 + self.Move,39 + self.Move]
        self._record_key = [20 + self.Move, 26 + self.Move, 32 + self.Move, 38 + self.Move]
        self._shiftUp_key = [25 + self.Move,31 + self.Move,37 + self.Move,43 + self.Move]
        self._shiftDown_key = [24 + self.Move,30 + self.Move,36 + self.Move,42 + self.Move]

        
        event.data1 += self.Move #how much each note should be shifted is applied
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
       
       
       
       
       
        OnMidiOutMsg(event)






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



        if event.midiId == 0x90 and event.data1 + self.Move != self._shiftUp12_key[self.page] or event.data1 + self.Move != self._shiftDown12_key[self.page] or event.data1 + self.Move != self._record_key[self.page]:
            print(utils.GetNoteName(event.data1), event.note)
            
            

  

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