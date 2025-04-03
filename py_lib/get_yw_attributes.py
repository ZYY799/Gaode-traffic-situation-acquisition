# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:04:39 2021

@author: THC
"""

def get_xy(filename):
    import geopandas as gpd
    yw = gpd.read_file(r"%s"%filename)
    yw["center"] = yw.centroid
    ywdict = {}
    #x是网格序号
    for x in range(1,len(yw)+1):
        ywdict[x] = (yw["center"][x - 1].xy[0][0] , yw["center"][x -1].xy[1][0])
    return ywdict
