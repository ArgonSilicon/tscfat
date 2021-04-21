#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 14:15:25 2021

@author: arsii
"""

import pandas as pd
from pathlib import Path

json_path = Path('/home/arsii/StudentLife/dataset/EMA/response/Stress/Stress_u08.json')

df_s = pd.read_json(json_path)

df_s['resp_time'] = pd.to_datetime(df_s['resp_time'],unit='s',origin='unix')
df_s = df_s.set_index('resp_time')
df_s.sort_index()
