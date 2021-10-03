#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 05:17:11 2021

@author: timur
"""


import requests
import folium
import webbrowser
import os
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon



def get_ways(values_clusters, name_column,go_back = False):
    colors = ['darkgreen', 'darkblue', 'pink', 'purple', 'lightgreen', 'beige', 'lightgray', 'lightblue', 'darkred', 'gray', 'black', 'lightred', 'cadetblue', 'red', 'darkpurple', 'orange', 'blue', 'green', 'white']
    values_clusters = []
    for i,cluster in enumerate(clusters):
       
        values_cluster = {"ID" :[],  "Lat":[], "Long":[]}
        values_cluster["ID"].append("main")
        values_cluster["Lat"].append(float(main_loc[0]))
        values_cluster["Long"].append(float(main_loc[1]))
        for item in cluster["items"]:
            init_point = item.split('-')[0]
            location = loc_by_id[init_point]
            values_cluster["ID"].append(item)
            values_cluster["Lat"].append(float(location[1]))
            values_cluster["Long"].append(float(location[0]))
        values_clusters.append(values_cluster)
        
        
    #shortest way (our)
    ways = shortest_way(values_clusters, name_column,go_back = False)['results']
    #print(ways)
    tooltip = 'Click to see the name'
    maps = folium.Map(location=loc_by_id["main"], zoom_start=12) 
    
    for i,way in enumerate(ways):
        #print(len(way))
        line_points = []
        for j,point in enumerate(way):
            for micro_point in point.split("-"):
                location = loc_by_id[micro_point]
                
                line_points.append(loc_by_id[micro_point])
                if micro_point != "main":
                    folium.Marker(location, popup=f'<i>{j}){micro_point}</i>', tooltip=tooltip,icon=folium.Icon(color=colors[i])).add_to(maps)
            
        folium.PolyLine(line_points,color=colors[i],weight=3,opacity=0.8).add_to(maps)
        
    map_file_name = f"{window}.html"
    maps.save(map_file_name)
    webbrowser.open('file://' +os.path.realpath(map_file_name),new=2)



def move_item(item1, item2, clusters):
    updated_clusters =[]
    for i,cluster in enumerate(clusters):
       
        new_cluster = {}
        new_cluster['centroid'] = cluster['centroid']
        new_cluster['items'] =  []
        for item in cluster["items"]:
            arr_item = item.split('-')
            if item2 in arr_item:
                new_cluster["items"].append(item1)
            if item1 in arr_item:
                arr_item.remove(item1)
            updated_item =  "-".join(arr_item)
            if len(arr_item) <= 0:
                continue
            new_cluster["items"].append(updated_item)
           
        updated_clusters.append(new_cluster)
    return updated_clusters

def distance(item1,item2):
    return Point(item1[0],item1[1]).distance(Point(item2[0], item2[1]))

def save_json(dict_object, file_name):
    with open(file_name, 'w') as fp:
        json.dump(dict_object, fp)

def shortest_way(data, column, zScale = True, go_back = True):
    params = {"data": [{"column": column, "go_back":str(go_back).lower(), "z_score": str(zScale).lower()}, data]}
    
    rest_url='https://chariot-maria.space/api/v1.0/shortest_way'
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


def show_polygon(poly_data, location):
    colors = ['darkgreen', 'darkblue', 'pink', 'purple', 'lightgreen', 'beige', 'lightgray', 'lightblue', 'darkred', 'gray', 'black', 'lightred', 'cadetblue', 'red', 'darkpurple', 'orange', 'blue', 'green', 'white']
    poly_map = folium.Map(location=loc_by_id["main"], zoom_start=12)
    for i,polygon in enumerate(poly_data):
        points = []
        for point in polygon["points"]:
            points.append([point[1], point[0]])
        points.append(points[0])
        folium.PolyLine(points,color=colors[i],weight=3,opacity=0.8).add_to(poly_map)
        
    map_file_name = f"polygons.html"
    poly_map.save(map_file_name)
    webbrowser.open('file://' +os.path.realpath(map_file_name),new=2)


data_file_name = input("File name:")
f = open (data_file_name, "r") 
  
data = json.loads(f.read())

f.close()


poly_file_name = input("Polygon file name:")
f = open (poly_file_name, "r") 
  
poly_data = json.loads(f.read())

f.close()


main_loc = [71.53352566795104,51.17567195495563]



locations = []


loc_by_id = {}


loc_by_id["main"] = [main_loc[1], main_loc[0]]

show_polygon(poly_data, loc_by_id["main"])

windows = {}

for i,item in enumerate(data):
    try:
        adr = item["address"]
        object_id = str(item["object_id"])
        time_val = item["name"]
        if time_val not in list(windows.keys()):
            windows[time_val] = {"ID" :[], "Adr":[], "Lat":[], "Long":[], "Polygon":[]}
        windows[time_val]["ID"].append(object_id)
        windows[time_val]["Adr"].append(adr)
        
        loc = item["geopoint"].split(",")
        windows[time_val]["Lat"].append(float(loc[0]))
        windows[time_val]["Long"].append(float(loc[1]))
        polygon_val = 0
        for polygon in poly_data:
            item_point = Point(float(loc[0]), float(loc[1]))
            points = polygon["points"]
            polygon_obj = Polygon(points)
            if polygon_obj.contains(item_point):
                polygon_val = polygon["value"]
                break
        windows[time_val]["Polygon"].append(polygon_val)
                
            
        location = [float(loc[1]), float(loc[0])]
        loc_by_id[object_id] = location
        

    except Exception as error:
        print(error, item)


k = int(input("k:")) #k=2 for hard test
size_min = 1


name_column = "ID"


for window in windows.keys():
    all_values = windows[window]
    added = []
    data = {"ID" :[], "Lat":[], "Long":[], "Polygon":[]}
    for i,name in enumerate(all_values["ID"]):
        if name in added:
            continue
        name_val = name
        
        data["ID"].append(name_val)
        data["Lat"].append(all_values["Lat"][i])
        data["Long"].append(all_values["Long"][i])
        data["Polygon"].append(all_values["Polygon"][i])
        
        
                    

    size_max = len(data["ID"]) - 1
    
    print(data)
    save_json(data, "data_for_request.json")
    res = clustering(data, k ,name_column, size_min, size_max)
    
    print(res)
    
    print("clustered")
    
    clusters = res["clusters"]
    

    
    get_ways(clusters, name_column,go_back = False)
    
        





