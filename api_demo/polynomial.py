#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Oct  3 01:24:12 2021

@author: timur
"""

import json
import requests




def predict_val(degrees, predict, x, y, subsets = 300, sampling_param = 2):
    params =  {"degrees": degrees, "predict": predict, "x":x, "y":y,"subsets": subsets, "sampling_param":sampling_param}

    
    rest_url='https://chariot-maria.space/api/v1.0/validating_pol'
    headers = {}
    headers["Content-Type"] = "application/json; charset=UTF-8"
    headers["Accept"] = "application/json; charset=UTF-8"
    
    rest_response = requests.request("POST", rest_url, headers=headers, json=params)

    return rest_response.json()




            
if __name__ == '__main__':         

        
    with open('example_polynomial.json') as json_file:
        data_json = json.load(json_file)
        
    
    degrees = list(range(1,16))
    print(degrees)
    predict = 'last+1'
    x = data_json["index"]
    y = data_json["value"]
    
    res = predict_val(degrees, predict, x, y)

    print(res)
            
      
       
