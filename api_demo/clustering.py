
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 01:22:44 2021

@author: timur
"""

import json
import requests




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


            
if __name__ == '__main__':         

        
    with open('example_clustering.json') as json_file:
        data_json = json.load(json_file)
        
    #number of clusters
    k = 7
    #column with items names
    column = "ID"
    
    #minimum number of elements in cluster
    size_min = 3
    
    #maximum number of elements in cluster 
    size_max = 9
    
    constrained = clustering(data_json, k, column,size_min, size_max)
    km = km_clustering(data_json, k, column)
    print('results:')
    print(constrained)
    print(km)
            
      
       
