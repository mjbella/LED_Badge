
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
for i in range(2, 199, 2):
    ref1 = "D{}".format(i-1)
    ref2 = "D{}".format(i)
    ref3 = "D{}".format(i+1)

    # Connect each one from the output of the first to the input of the second
    tmp1 = tmp_padlist[ref1]
    tmp2 = tmp_padlist[ref2]
    tmp3 = tmp_padlist[ref3]

    # connect back to the previous LED
    bclocks = tmp1[2]
    bdatas  = tmp1[3]
    bclocke = tmp2[0]
    bdatae  = tmp2[1]

    # connect forward to the next LED
    fclocks = tmp2[2]
    fdatas  = tmp2[3]
    fclocke = tmp3[0]
    fdatae  = tmp3[1]

    conns = [(bclocks,bclocke), (bdatas, bdatae),
             (fclocks, fclocke), (fdatas, fdatae)]

    for start, end in conns:
        print start, end

        t = TRACK(pcb)
        pcb.Add(t)
        t.SetStart(pcbnew.wxPoint(*start))
        t.SetEnd(pcbnew.wxPoint(*end))
        t.SetNetCode(0)
        t.SetLayer(31)



