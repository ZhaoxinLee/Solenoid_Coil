import numpy as np
import time
from piDIO import PIDIO
from fieldManager import FieldManager

field = FieldManager(PIDIO())

# Field amplitude
amplX = 0 #[mT]
amplY = 10 #[mT]
amplZ = 10 #[mT]
# Frequency
freqX = -50 #[Hz]
freqY = -50 #[Hz]
freqZ = 50 #[Hz]

# Maximum running time.
tMax = 10 #[s]
# Begin timer.
tStart = time.time() #[s]
t = time.time() - tStart #[s]

while t < tMax:
#     bX = amplX
    bX = amplX*np.cos(2*np.pi*freqX*t)
#     bY = amplY
    bY = amplY*np.sin(2*np.pi*freqY*t)
#     bZ = amplZ
    bZ = amplZ*np.sin(2*np.pi*freqZ*t)
    field.setX(bX)
    field.setY(bY)
    field.setZ(bZ)
    #print('t: ', ('{0:0.3f}'.format(t)).rjust(3), 's; ', end=' ')
    #print('Xd: ', ('{0:.2f}'.format(bX)).rjust(5), ' mT; ')
    t = time.time() - tStart #[s]
field.setXYZ(0,0,0)
