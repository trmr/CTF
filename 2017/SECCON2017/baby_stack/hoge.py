import os
import sys

fd = sys.stdout

print fd.fileno()

r = os.read(fd.fileno(), 1)

print r