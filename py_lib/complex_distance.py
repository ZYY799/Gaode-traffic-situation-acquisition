# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:36:53 2021

@author: THC
"""
def complex_distance( lon1, lat1, lon2, lat2):
    import numpy as np
    lon1, lat1, lon2, lat2 = map(np.deg2rad, [lon1, lat1, lon2, lat2])   
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2  
    c = 2 * np.arcsin(np.sqrt(a))   
    return c * 6371 * 1000  # r = 6371 # the avg radius of earth, km
