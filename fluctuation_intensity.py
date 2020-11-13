<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 13:02:27 2020

@author: arsii
"""

import numpy as np
import matplotlib.pyplot as plt

# permutation entropy
# correlation dimension -> complexity
# Luyapunov exponent -> chaotiticity
# fluctuation intensity -> how much time series fluctuate
# Distribution -> how widely the values are distributed (deviance from equally distributed data)

x = np.linspace(0,8,num = 9)
y_1 = np.array([3,5,6,3,3,3,7,5,4])

figure = plt.figure(figsize=(6,6))
plt.plot(x, y_1,'-o')
plt.ylim(0,8)
plt.show()

def fluctuation_intensity(y,scale,window):
    # scale
    s = scale
    # max fluctuations
    m = window - 1
    
    y = np.diff(y)
    y = np.append(y,0)
    print(y)
    
    # intialize variables
    l = 1
    diff = 0
    diff_arr= []
    
    for i in range(window-1):
        print("i: ",i)
        
        if np.sign(y[i]) == np.sign(y[i+1]): # continues growing / decreasing
            print("continue")
            
            # add difference and length
            diff += y[i]
            l += 1
        
        else: # change of sign
            print("stop")
            
            # add difference and append value
            diff += y[i]
            diff_arr.append(abs(diff/l))
            
            # reset variables
            diff = 0
            l = 1
    
    print(sum(diff_arr))
    print(s)
    print(m)
    # calculate fluctuation intesity
    F = sum(diff_arr) / (s*m)
    return F

fi_1 = fluctuation_intensity(y_1,6,7)

y_2 = np.array([3,3,3,3,3,3,3])
y_3 = np.array([2,5,2,5,2,5,2])
y_4 = np.array([1,1,1,1,7,7,7])
y_5 = np.array([1,7,1,7,1,7,1])
y_6 = np.array([1,2,3,4,5,6,7])
y_7 = np.array([4,5,3,6,2,7,1])


fi_2 = fluctuation_intensity(y_2,6,7)
fi_3 = fluctuation_intensity(y_3,6,7)
fi_4 = fluctuation_intensity(y_4,6,7)
fi_5 = fluctuation_intensity(y_5,6,7)
fi_6 = fluctuation_intensity(y_6,6,7)
fi_7 = fluctuation_intensity(y_7,6,7)
=======
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 13:02:27 2020

@author: arsii
"""

import numpy as np
import matplotlib.pyplot as plt

# permutation entropy
# correlation dimension -> complexity
# Luyapunov exponent -> chaotiticity
# fluctuation intensity -> how much time series fluctuate
# Distribution -> how widely the values are distributed (deviance from equally distributed data)

x = np.linspace(0,8,num = 9)
y_1 = np.array([3,5,6,3,3,3,7,5,4])

figure = plt.figure(figsize=(6,6))
plt.plot(x, y_1,'-o')
plt.ylim(0,8)
plt.show()

def fluctuation_intensity(y,scale,window):
    # scale
    s = scale
    # max fluctuations
    m = window - 1
    
    y = np.diff(y)
    y = np.append(y,0)
    print(y)
    
    # intialize variables
    l = 1
    diff = 0
    diff_arr= []
    
    for i in range(window-1):
        print("i: ",i)
        
        if np.sign(y[i]) == np.sign(y[i+1]): # continues growing / decreasing
            print("continue")
            
            # add difference and length
            diff += y[i]
            l += 1
        
        else: # change of sign
            print("stop")
            
            # add difference and append value
            diff += y[i]
            diff_arr.append(abs(diff/l))
            
            # reset variables
            diff = 0
            l = 1
    
    print(sum(diff_arr))
    print(s)
    print(m)
    # calculate fluctuation intesity
    F = sum(diff_arr) / (s*m)
    return F

fi_1 = fluctuation_intensity(y_1,6,7)

y_2 = np.array([3,3,3,3,3,3,3])
y_3 = np.array([2,5,2,5,2,5,2])
y_4 = np.array([1,1,1,1,7,7,7])
y_5 = np.array([1,7,1,7,1,7,1])
y_6 = np.array([1,2,3,4,5,6,7])
y_7 = np.array([4,5,3,6,2,7,1])


fi_2 = fluctuation_intensity(y_2,6,7)
fi_3 = fluctuation_intensity(y_3,6,7)
fi_4 = fluctuation_intensity(y_4,6,7)
fi_5 = fluctuation_intensity(y_5,6,7)
fi_6 = fluctuation_intensity(y_6,6,7)
fi_7 = fluctuation_intensity(y_7,6,7)
>>>>>>> 1c86f2ee1a63d54ea6a092c3d0964a766f57cfa0
