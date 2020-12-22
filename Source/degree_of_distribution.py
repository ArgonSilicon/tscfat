# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 13:57:14 2020

@author: arsii
"""

import numpy as np
import pytest



def distribution_degree(y,scale,window):
    s = scale
    m = window -1
    interval = s / m
    x = np.sort(y)
    y = np.array([interval*i for i in range(1,m+2)])
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
                store += d - a
                delta_x = x[a+1:d+1] - x[a]
                delta_y = y[a+1:d+1] - y[a]
                delta = delta_y - delta_x
                ab = delta*np.heaviside(delta,0) / 1
                sum_ab += np.sum(ab)
                '''
                for b in range((a+1),(d+1)):
                    store += 1
                    #print("b: ",b)
                    delta_x = x[b] -x[a]
                    #print(delta_x)
                    delta_y = y[b] -y[a]
                    #print(delta_y)
                    delta = delta_y - delta_x
                    #print(delta)
                    #norm = 252
                    #print(norm)
                    ab = delta*np.heaviside(delta,0) / 1
                    #print(ab)
                    sum_ab += ab
                    #print(sum_ab)
                    #print("---")
                    '''
   # print(store)                     
    return 1 - sum_ab / (store*2)
'''
store += d-a
delta_x = x[a+1:d+1] - x[a]
delta_y = y[a+1:d+1] - y[a]
delta = delta_y - delta_x
ab = delta*np.heaviside(delta,0) / 1
sum_ab += np.sum(ab)
'''

def test_fluctuation_intensity():
    y_1 = np.array([3,5,6,3,3,3,7,5,4])
    y_2 = np.array([3,3,3,3,3,3,3])
    y_3 = np.array([2,5,2,5,2,5,2])
    y_4 = np.array([1,1,1,1,7,7,7])
    y_5 = np.array([1,7,1,7,1,7,1])
    y_6 = np.array([1,2,3,4,5,6,7])
    y_7 = np.array([4,5,3,6,2,7,1])
 
    assert distribution_degree(y_1,6,7) == pytest.approx(0.41666666666666663)
    assert distribution_degree(y_2,6,7) == pytest.approx(0.0)
    assert distribution_degree(y_3,6,7) == pytest.approx(0.5515873015873016)
    assert distribution_degree(y_4,6,7) == pytest.approx(0.6349206349206349)
    assert distribution_degree(y_5,6,7) == pytest.approx(0.6349206349206349)
    assert distribution_degree(y_6,6,7) == pytest.approx(1.0)
    assert distribution_degree(y_7,6,7) == pytest.approx(1.0)


