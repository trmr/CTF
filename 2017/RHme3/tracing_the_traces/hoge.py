# new script base on https://forum.newae.com/viewtopic.php?f=9&t=362
import scipy.io as sio
import numpy as np
import ctypes
import os
import subprocess
from chipwhisperer.common.traces.TraceContainerNative import TraceContainerNative

#convert the traces to version 6
subprocess.call(["octave-cli","--eval",'load "traces.mat" ; save -6 "traces_6.mat"'])
traces = sio.loadmat("traces_6.mat")

ntraces = len(traces['samples'])
traceLen = len(traces['samples'][0])


inp = np.uint8(traces['inout'][:, 0:16])
out = np.uint8(traces['inout'][:, 16:32])

#If you'd like to plot a trace to see it
import matplotlib.pyplot as plt
plt.plot(traces['samples'][0,:], 'r')
plt.plot(traces['samples'][1,:], 'b')
plt.show()

#Save as ChipWhisperer project
tc = TraceContainerNative()
for i in range(0, ntraces):
    tc.addWave(traces['samples'][i])
    tc.addTextin(inp[i])
    tc.addTextout(out[i])

    #Temp - add fake key info. Required on Linux possibly, will be fixed to avoid this. Be sure to turn
    #highlight key off to avoid being confused.
    tc.addKey([0]*16)

os.mkdir('rhme3')
tc.saveAllTraces('rhme3')
tc.config.setConfigFilename('rhme3/rhme.cfg')
tc.config.saveTrace()