import scipy.io as sio
import numpy as np
import os
import matplotlib.pyplot as plt
from chipwhisperer.common.traces.TraceContainerNative import TraceContainerNative

traces = open("traces.txt")

tlist = []

for line in traces:
    l = map(int, line.strip().split(" "))
    tlist.append(l)

#plt.plot(tlist[0])
#plt.plot(tlist[1])
#plt.plot(tlist[2])
#plt.show()


ntraces = len(tlist)
assert ntraces == 100000, "cannot read correctly"

traceLen = len(tlist[0])
assert traceLen == 180, "trace length is wrong"

plaintext = open("plaintexts.txt")

plist = []

for line in plaintext:
    l = map(int, line.strip().split(" "))
    plist.append(l)

ntraces = len(plist)
assert ntraces == 100000, "cannot read correctly"

traceLen = len(plist[0])
assert traceLen == 16, "trace length is wrong"

inp = np.uint8(plist)

print inp

#Save as ChipWhisperer project
tc = TraceContainerNative()
for i in range(0, ntraces):
    tc.addWave(tlist[i])
    tc.addTextin(inp[i])
    tc.addTextout([0]*16)
    tc.addKey([0]*16)

os.mkdir('aes')
tc.saveAllTraces('aes')
tc.config.setConfigFilename('aes/aes.cfg')
tc.config.saveTrace()