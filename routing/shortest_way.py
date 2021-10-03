#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 22:11:37 2021

@author: timur
"""


import json
import requests




def our_way(data, column, zScale = True, go_back = True):
    params = {"data": [{"column": column, "go_back":str(go_back).lower(), "z_score": str(zScale).lower()}, data]}
    
    rest_url='https://chariot-maria.space/api/v1.0/shortest_way'
    headers = {}
    headers["Content-Type"] = "application/json; charset=UTF-8"
    headers["Accept"] = "application/json; charset=UTF-8"
    
    rest_response = requests.request("POST", rest_url, headers=headers, json=params)
    
    return rest_response.json()

def our_shortest_way(json_val):
    
    params = json_val
    
    rest_url='https://chariot-maria.space/api/v1.0/shortest_way'
    headers = {}
    headers["Content-Type"] = "application/json; charset=UTF-8"
    headers["Accept"] = "application/json; charset=UTF-8"
    
    rest_response = requests.request("POST", rest_url, headers=headers, json=params)
    
    return rest_response.json()

def distanse_matrix(json_val):
    
    params = json_val
    
    rest_url='https://chariot-maria.space/api/v1.0/distanse_matrix'
    headers = {}
    headers["Content-Type"] = "application/json; charset=UTF-8"
    headers["Accept"] = "application/json; charset=UTF-8"
    
    rest_response = requests.request("POST", rest_url, headers=headers, json=params)
    
    return rest_response.json()


def operation(path,temp_path, claster_dict,go_back):
    if(len(temp_path) == 0):
        dist = 0.0
        
        if go_back:
            dist = claster_dict[path[0]+"-"+path[-1]]
                   
        for i in range(len(path)-1):
            item = path[i]
            item2 = path[i+1]
            dist += claster_dict[item+"-"+item2]
        return dist, path
    else:
        
        min_dist = -1
        min_path = []
        for i in range(len(temp_path)):
            new_path = path[:]
            new_path.append(temp_path[i])
            new_temp = temp_path[:i] + temp_path[i+1:]
            dist_temp = operation(new_path,new_temp, claster_dict,go_back)
            if(dist_temp[0] < min_dist or  min_dist == -1):
                min_dist = dist_temp[0]
                min_path = dist_temp[1]
        return min_dist,min_path
            
        

def dfs(json_val):
    result = []
    name_column = json_val['data'][0]["column"]
    dist_matrix = distanse_matrix(json_val)['results']
    go_back = json_val['data'][0]["go_back"]
    for i,cluster in enumerate(json_val['data'][1]):
        
            points = cluster[name_column]
            
           
            path = [points[0]]
            temp_path = points[1:]
            claster_dict = dist_matrix[i]["dict"]
            res = operation(path,temp_path, claster_dict,go_back)[1]
            result.append(res)
    return {"results":result}
            
def bfs(json_val):
    result = []
    name_column = json_val['data'][0]["column"]
    dist_matrix = distanse_matrix(json_val)['results']
    go_back = json_val['data'][0]["go_back"]
    for i,cluster in enumerate(json_val['data'][1]):
        
            points = cluster[name_column]
            
            initPath = points[0]
            pathQueue = [[initPath]]
            min_dist = -1
            min_path = []
            claster_dict = dist_matrix[i]["dict"]
            while len(pathQueue) != 0:
                tmpPath = pathQueue.pop(0)
                
                if(len(tmpPath) == len(points)):
                    dist = 0.0
                    if go_back:
                        dist = claster_dict[initPath+"-"+tmpPath[-1]]
                    
                    for i in range(len(tmpPath)-1):
                        item = tmpPath[i]
                        item2 = tmpPath[i+1]
                        dist += claster_dict[item+"-"+item2]
                    if(dist < min_dist or min_dist == -1):
                        min_dist = dist
                        min_path = tmpPath
                        
                else:
                    
                    for nextNode in points:
                        if nextNode not in tmpPath:
                            
                            newPath = tmpPath + [nextNode]
                            pathQueue.append(newPath)
                        
                        
                
            result.append(min_path)
    
    return {"results":result}
            

      
       