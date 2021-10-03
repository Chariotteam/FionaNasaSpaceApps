#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 23:05:44 2021

@author: timur
"""

import json
import time
from shortest_way import our_shortest_way,dfs,bfs


            
if __name__ == '__main__':         

    start_time = time.time()
    file = input()
    with open(file) as json_file:
        data_json = json.load(json_file)
        
        
    start_time = time.time()
    results = our_shortest_way(data_json)
    end_time = time.time()
    print(f"Our time in seconds: {end_time - start_time}")
    
    
    start_time = time.time()
    results = dfs(data_json)
    end_time = time.time()
    print(f"DFS time in seconds: {end_time - start_time}")
    
    """ or bfs, which takes more time for this task than dfs
    start_time = time.time()
    results = bfs(data_json)
    end_time = time.time()
    print(f"BFS time in seconds: {end_time - start_time}")
    """        
      
       