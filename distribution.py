# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 13:57:14 2020

@author: arsii
"""

import numpy as np

y_1 = np.array([3,5,6,3,3,3,7,5,4])

def distribution(y,scale,window):
    s = scale
    m = window -1
    interval = s / m
    x = np.sort(y)
    y = [interval*i for i in range(1,m+2)]
    #print(y)
    sum_ab = 0
    store = 0
    
    # calculate aberration
    for c in range(0,window-1): #0 - 6
        #print("c: ",c)
        for d in range((c+1),window): # (c+1) - 7
            #print("d: ",d)
            for a in range(c,(d)):
                #print("a: ",a)
                for b in range((a+1),(d+1)):
                    store += 1
                    #print("b: ",b)
                    delta_x = x[b] -x[a]
                    #print(delta_x)
                    delta_y = y[b] -y[a]
                    #print(delta_y)
                    delta = delta_y - delta_x
                    #print(delta)
                    norm = 252
                    #print(norm)
                    ab = delta*np.heaviside(delta,0) / 1
                    #print(ab)
                    sum_ab += ab
                    #print(sum_ab)
                    #print("---")
    print(store)                     
    return 1 - sum_ab / (store*2)

D = distribution(y_1,6,7)
print(D)


y_2 = np.array([3,3,3,3,3,3,3])
y_3 = np.array([2,5,2,5,2,5,2])
y_4 = np.array([1,1,1,1,7,7,7])
y_5 = np.array([1,7,1,7,1,7,1])
y_6 = np.array([1,2,3,4,5,6,7])
y_7 = np.array([4,5,3,6,2,7,1])
#y_8 = np.array([1,2])


D_2 = distribution(y_2,6,7)
D_3 = distribution(y_3,6,7)
D_4 = distribution(y_4,6,7)
D_5 = distribution(y_5,6,7)
D_6 = distribution(y_6,6,7)
D_7 = distribution(y_7,6,7)
#D_8 = distribution(y_8,1,2)

print(D_2,D_3,D_4,D_5,D_6,D_7)


