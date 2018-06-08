
import sys
import os
from pcbnew import *
from time import sleep

# Get the board
pcb = GetBoard()

# Find the pins we need on each LED
tmp_padlist = {}
for mod in pcb.GetModules():
    refdes = mod.GetReference().encode('utf-8')
    if refdes.startswith('D'):
        clkin = None
        din = None
        clkout = None
        dout = None

        for pad in mod.Pads():
            print "====", refdes, "===="
            
            padn = int(pad.GetPadName())
            pad_position = pad.GetPosition()
            if padn == 3:
                #print 'clkin'
                clkin = pad_position
            elif padn == 2:
                #print 'din'
                din = pad_position
            elif padn == 6:
                #print 'clkout'
                clkout = pad_position
            elif padn == 1:
                #print 'dout'
                dout = pad_position
        # Store the pad locations to use for the next LED
        tmp_padlist[refdes] = (clkin, din, clkout, dout)

# Add traces!
for i in range(1, 20, 2):
    ref1 = "D{}".format(i)
    ref2 = "D{}".format(i+1)
    print ref1, ref2
    # Connect each one from the output of the first to the input of the second
    tmp1 = tmp_padlist[ref1]
    tmp2 = tmp_padlist[ref2]

    start1 = tmp1[2]
    end1   = tmp2[0]
    start2 = tmp1[3]
    end2   = tmp2[1]

    print start1, end1
    print start2, end2

    t1 = TRACK(pcb)
    pcb.Add(t1)
    t1.SetStart(pcbnew.wxPoint(*start1))
    t1.SetEnd(pcbnew.wxPoint(*end1))
    t1.SetNetCode(0)
    t1.SetLayer(31)

    t2 = TRACK(pcb)
    pcb.Add(t2)
    t2.SetStart(pcbnew.wxPoint(*start2))
    t2.SetEnd(pcbnew.wxPoint(*end2))
    t2.SetNetCode(0)
    t2.SetLayer(31)

