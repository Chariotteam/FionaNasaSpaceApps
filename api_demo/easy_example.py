#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Oct  3 01:22:53 2021

@author: timur
"""

import requests



def compare_values(y, arrays):
    params = {'y': y, 'with': arrays}
    rest_url='https://chariot-maria.space/api/v1.0/linear/compare_values'
    headers = {}
    headers["Content-Type"] = "application/json; charset=UTF-8"
    headers["Accept"] = "application/json; charset=UTF-8"
    
    rest_response = requests.request("POST", rest_url, headers=headers, json=params)
    
    return rest_response.json()



def predict_val(degrees, predict, x, y, subsets = 300, sampling_param = 2):
    params =  {"degrees": degrees, "predict": predict, "x":x, "y":y,"subsets": subsets, "sampling_param":sampling_param}

    
    rest_url='https://chariot-maria.space/api/v1.0/validating_pol'
    headers = {}
    headers["Content-Type"] = "application/json; charset=UTF-8"
    headers["Accept"] = "application/json; charset=UTF-8"
    
    rest_response = requests.request("POST", rest_url, headers=headers, json=params)

    return rest_response.json()



def clustering(data, k ,column, size_min, size_max, max_attemps = 300, zScale = False):
    params = {"data": [{"column": column, "k": k, "attemps": max_attemps, "size_min":size_min, "size_max":size_max, "z_score": str(zScale).lower()}, data]}
    
    rest_url='https://chariot-maria.space/api/v1.0/constrained_clustering'
    headers = {}
    headers["Content-Type"] = "application/json; charset=UTF-8"
    headers["Accept"] = "application/json; charset=UTF-8"
    
    rest_response = requests.request("POST", rest_url, headers=headers, json=params)
    
    return rest_response.json()


def km_clustering(data, k ,column, max_attemps = 300, zScale = False):
    params = {"data": [{"column": column, "k": k, "attemps": max_attemps, "z_score": str(zScale).lower()}, data]}
    
    rest_url='https://chariot-maria.space/api/v1.0/kmean'
    headers = {}
    headers["Content-Type"] = "application/json; charset=UTF-8"
    headers["Accept"] = "application/json; charset=UTF-8"
    
    rest_response = requests.request("POST", rest_url, headers=headers, json=params)
    
    return rest_response.json()

