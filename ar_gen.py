#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 10:25:37 2021

@author: timur
"""

import random
import json

def save_json(dict_object, file_name):
    with open(file_name, 'w') as fp:
        json.dump(dict_object, fp)

data = {'data' : []}


n = input()

for i in range(n):
    x = random.uniform(-0.4, 0.4)
    y = random.uniform(-0.4, 0.4)
    z = random.uniform(-0.4, 0.4)
    cr = random.uniform(0.0001, 0.001)
    h = random.uniform(0.0001, 0.001)
    data['data'].append([x,y,z,cr,h])
    
print(data)
save_json(data, 'example.json')
    
    