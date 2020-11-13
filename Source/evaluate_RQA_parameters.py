#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 13:03:35 2020

@author: ikaheia1
"""


#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""FNN for time series from the Henon map.
As expected, the FNN fraction goes to zero at an embedding dimension
equal to 2.
"""

from nolitsa import data, dimension
import matplotlib.pyplot as plt
import numpy as np

# Generate data.
x = data.henon(length=5000)[:, 0]
#%%
dim = np.arange(1, 10 + 1)
f1, f2, f3 = dimension.fnn(x, tau=1, dim=dim, window=1, metric="cityblock",maxnum=100)

plt.title(r'FNN for Henon map')
plt.xlabel(r'Embedding dimension $d$')
plt.ylabel(r'FNN (%)')
plt.plot(dim, 100 * f1, 'bo--', label=r'Test I')
plt.plot(dim, 100 * f2, 'g^--', label=r'Test II')
plt.plot(dim, 100 * f3, 'rs-', label=r'Test I + II')
plt.legend()

plt.show()

#%%

"""Time delay estimation for time series from the Henon map.
For map like data, the redundancy between components of the time delayed
vectors decrease drastically (or equivalently, the irrelevance increases
rapidly).  Best results are often obtained with a time delay of 1.
Here, we see that for data coming out of the Henon map, the delayed
mutual information curve (which does not have any local minima) gives
us a very bad estimate of the time delay.
"""

import numpy as np
import matplotlib.pyplot as plt
from nolitsa import data, delay
from scipy.signal import argrelextrema

x = data.henon()[:, 0]
x = amplitude

#%% Compute autocorrelation and delayed mutual information.
lag = np.arange(50)
r = delay.acorr(x, maxtau=50)
i = delay.dmi(x, maxtau=50)
a = delay.adfd(x,maxtau=50)

r_delay = np.argmax(r < 1.0 / np.e)
print(r'Autocorrelation time = %d' % r_delay)

# for local minima
locmin = argrelextrema(i, np.less)
print(r'Local minimums: {}'.format(*locmin))

plt.figure(1)

plt.subplot(311)
plt.title(r'Delay estimation for Henon map')
plt.ylabel(r'Delayed mutual information')
plt.plot(lag, i)

plt.subplot(312)
plt.xlabel(r'Time delay $\tau$')
plt.ylabel(r'Autocorrelation')
plt.plot(lag, r, r_delay, r[r_delay], 'o')

plt.subplot(313)
plt.title(r'ADFD from the diagonal')
plt.ylabel(r'ADFD')
plt.plot(lag, a)

plt.figure(2)
plt.subplot(121)
plt.title(r'Time delay = 10')
plt.xlabel(r'$x(t)$')
plt.ylabel(r'$x(t + \tau)$')
plt.plot(x[:-10], x[10:], '.')

plt.subplot(122)
plt.title(r'Time delay = %d' % r_delay)
plt.xlabel(r'$x(t)$')
plt.ylabel(r'$x(t + \tau)$')
plt.plot(x[:-r_delay], x[r_delay:], '.')

plt.show()