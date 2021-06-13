#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 13:32:36 2021

@author: arsii
"""

import numpy as np
import pandas as pd
from pathlib import Path

#%%

def decode_phq9(value):
    phq_dict = {'Not at all' : 0,
                "Several days" : 1,
                "More than half the days" : 2,
                "Nearly every day" : 3
                }
    
    return phq_dict[value]

def decode_stress(value):
    stress_dict = {'Never' : 0,
                   "Almost never" : 1,
                   "Sometime" : 2,
                   "Fairly often" : 3,
                   "Very often" : 4
                   }
    
    return stress_dict[value]

def decode_lone(value, reverse = False):
    lone_dict = {'Never' : 0,
                 "Rarely" : 1,
                 "Sometimes" : 2,
                 "Often" : 3,
                  }
    
    reverse_dict = {'Never' : 3,
                    "Rarely" : 2,
                    "Sometimes" : 1,
                    "Often" : 0,
                    }
    
    if not reverse:
        print('reverse!')
        return lone_dict[value]

    return reverse_dict[value]

#%%
DATA_FOLDER = Path(r'/home/arsii/StudentLife/dataset/survey/PHQ-9.csv')

df = pd.read_csv(DATA_FOLDER)


#%%
uids = df.uid.unique()

cherry = ['u51','u02','u12','u10','u57','u35','u19','u36','u17','u08']

results = np.zeros((46,2))

for i,u in enumerate(uids,start=0):
    df_pre = df[(df['uid'] == u) & (df['type'] == 'pre')] 
    responces = df_pre.iloc[:,2:11].values
    responces = responces.flatten()
    dec_pre = sum([decode_phq9(r) for r in responces.tolist()])
    
    df_aft = df[(df['uid'] == u) & (df['type'] == 'post')] 
    responces = df_aft.iloc[:,2:11].values
    responces = responces.flatten()
    dec_aft = sum([decode_phq9(r) for r in responces.tolist()])
    
    results[i,0] = dec_pre
    results[i,1] = dec_aft
    
#%%

df_phq = pd.DataFrame(data = results,
                      index = uids,
                      columns = ['pre','post'] )

df_phq['diff'] = df_phq.post - df_phq.pre
print(df_phq.loc[cherry].median())

#%% PANAS

DATA_FOLDER = Path(r'/home/arsii/StudentLife/dataset/survey/panas.csv')

df_panas = pd.read_csv(DATA_FOLDER)


#%%

DATA_FOLDER = Path(r'/home/arsii/StudentLife/dataset/survey/FlourishingScale.csv')

df_flour = pd.read_csv(DATA_FOLDER)
df_flour['average'] = df_flour.mean(axis=1)

flo_id = df_flour[df_flour['type'] == 'post'].uid

df_flo_pre = df_flour[df_flour['type'] == 'pre']
df_flo_post = df_flour[df_flour['type'] == 'post']

df_flo_pre.index = df_flo_pre.uid
df_flo_post.index = df_flo_post.uid
 
flo_pre = df_flo_pre.loc[flo_id].average
flo_post = df_flo_post.loc[flo_id].average
flo_diff = flo_post - flo_pre

flo_df = pd.concat([flo_pre,flo_post,flo_diff],axis=1)
flo_df.columns = ['pre','post','diff']

cherry2 = ['u51','u02','u10','u35','u19','u36','u17']
print(flo_df.loc[cherry2].median())

#%%

DATA_FOLDER = Path(r'/home/arsii/StudentLife/dataset/survey/PerceivedStressScale.csv')

df_stress = pd.read_csv(DATA_FOLDER)

df_stress.fillna(value='Never',inplace=True)

uids = df_stress.uid.unique()

cherry = ['u51','u02','u12','u10','u57','u35','u19','u36','u17','u08']

stress_results = np.zeros((46,2))

for i,u in enumerate(uids,start=0):
    
    df_pre = df_stress[(df_stress['uid'] == u) & (df_stress['type'] == 'pre')] 
    responces = df_pre.iloc[:,2:12].values
    responces = responces.flatten()
    dec_pre = sum([decode_stress(r) for r in responces.tolist()])
    
    df_aft = df_stress[(df_stress['uid'] == u) & (df_stress['type'] == 'post')] 
    responces = df_aft.iloc[:,2:12].values
    responces = responces.flatten()
    dec_aft = sum([decode_stress(r) for r in responces.tolist()])
    
    stress_results[i,0] = dec_pre
    stress_results[i,1] = dec_aft
    
df_st = pd.DataFrame(data = stress_results,
                      index = uids,
                      columns = ['pre','post'] )

df_st['diff'] = df_st.post - df_st.pre
print(df_st.loc[cherry].median())

df_st.loc[cherry]

#%%

DATA_FOLDER = Path(r'/home/arsii/StudentLife/dataset/survey/LonelinessScale.csv')

df_lone = pd.read_csv(DATA_FOLDER)

#df_stress.fillna(value='Never',inplace=True)

uids = df_lone.uid.unique()

cherry = ['u51','u02','u12','u10','u57','u35','u19','u36','u17','u08']
invert = [True, False, False, False, True, True, False, False, True, True,
          False, False, False, False, True, True, False, False, True, True]

lone_results = np.zeros((46,2))

for i,u in enumerate(uids,start=0):
    
    df_pre = df_lone[(df_lone['uid'] == u) & (df_lone['type'] == 'pre')] 
    responces = df_pre.iloc[:,2:22].values
    responces = responces.flatten()
    dec_pre = sum([decode_lone(r,j) for r,j in zip(responces.tolist(),invert)])
      
    df_aft = df_lone[(df_lone['uid'] == u) & (df_lone['type'] == 'post')] 
    responces = df_aft.iloc[:,2:11].values
    responces = responces.flatten()
    dec_aft = sum([decode_lone(r,j) for r,j in zip(responces.tolist(),invert)])
    
    lone_results[i,0] = dec_pre
    lone_results[i,1] = dec_aft
    
df_loneliness = pd.DataFrame(data = lone_results,
                             index = uids,
                             columns = ['pre','post'] )

df_loneliness['diff'] = df_loneliness.post - df_loneliness.pre

print(df_loneliness.loc[cherry].median())

df_loneliness.loc[cherry]