import numpy
import matplotlib.pyplot as plt
from binascii import hexlify
import scipy.io as sio
from Crypto.Cipher import AES

SAMPLES = 100

traces = sio.loadmat("traces.2.mat")

fig = plt.figure()

ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

for i in range(SAMPLES):
    ax1.plot(traces['samples'][i])

# Sum of absolute difference
def synchronize(trace, reference, window=[-1,1], max_offset=500):
    if window[0] == -1:
        window[0] = 0
    if window[1] == 1:
        window[1] = len(reference) -1

    window_size = window[1] - window[0]
    reference_window = reference[window[0]:window[1]]
    sad = [0] * (max_offset*2 + 1)
    for x in range(0, max_offset*2 + 1):
        trace_slice = trace[window[0]-max_offset+x:window[1]-max_offset+x]
        sad[x] = numpy.sum(numpy.abs(reference_window - trace_slice))
    sad_idx = numpy.argmin(sad)
    offset = -max_offset + sad_idx
    synchronized_trace = trace
    if offset < 0:
        synchronized_trace = numpy.concatenate(([0]*abs(offset), synchronized_trace[:-abs(offset)]))
    elif offset > 0:
        synchronized_trace = numpy.concatenate((synchronized_trace[abs(offset):], [0]*abs(offset)))
    return synchronized_trace

reference_trace = traces['samples'][0]
sync_traces = reference_trace

i = 0
for trace in traces['samples'][1:SAMPLES+1]:
    synchronized_trace = synchronize(trace, reference_trace, [2500, 4000])
    sync_traces = numpy.vstack((sync_traces, synchronized_trace))
    i += 1
    if i % 10 == 0:
        print i

for i in range(SAMPLES):
    ax2.plot(sync_traces[i])

plt.show()