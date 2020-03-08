import scipy.io as sio
import numpy as np
import os
from chipwhisperer.common.traces.TraceContainerNative import TraceContainerNative

traces = sio.loadmat("traces.2.mat")

print traces['samples']


ntraces = len(traces['samples'])
traceLen = len(traces['samples'][0])

inp = np.uint8(traces['inout'][:, 0:16])
out = np.uint8(traces['inout'][:, 16:32])

#Save as ChipWhisperer project
tc = TraceContainerNative()
for i in range(0, ntraces):
    tc.addWave(traces['samples'][i])
    tc.addTextin(inp[i])
    tc.addTextout(out[i])
    tc.addKey([0]*16)

os.mkdir('rhme3')
tc.saveAllTraces('rhme3')
tc.config.setConfigFilename('rhme3/rhme.cfg')
tc.config.saveTrace()