# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:41:02 2021

@author: THC
"""
def get_odli(ywdict,read_path,save_path,save_name):
    
    import os
    import pandas as pd
    import geopandas as gpd
    import numpy as np
    import sys
    sys.path.append(r"E:BigData/tuhongchang/py_lib")
    from complex_distance import complex_distance
    
    
    odtmp = [ yy for yy in list(os.walk(r"%s"%read_path))[0][2] if ".csv" in yy]
    
    odli=[]
    for od in odtmp:
        oddf = pd.read_csv(r'%s/%s'%(read_path,od),encoding = 'utf-8') 
        for i in range(len(oddf)):
            date = oddf["date"][i]
            oid = oddf["s_id"][i]
            did_all = oddf["e_id_all"][i].split("_")
            for did_each in did_all:
                did = did_each.split("|")[0]
                num = did_each.split("|")[1]
                odli.append([oid,int(did),int(num),str(date)[-2:]+'0'+od[:3]])


    odpd = pd.DataFrame(columns = ["oid","did","num","date"],data = odli)
    odpd = odpd[odpd["oid"]!=odpd["did"]]
    
    odpd["ox"]=odpd.apply(lambda row: ywdict[int(row["oid"])][0],axis = 1)
    odpd["oy"]=odpd.apply(lambda row: ywdict[int(row["oid"])][1],axis = 1)
    odpd["dx"]=odpd.apply(lambda row: ywdict[int(row["did"])][0],axis = 1)
    odpd["dy"]=odpd.apply(lambda row: ywdict[int(row["did"])][1],axis = 1)
    
    odpd["odlen"]=odpd.apply(lambda row: complex_distance(row["ox"],row["oy"],row["dx"],row["dy"]),axis = 1)
    odpd.drop(columns = ['ox','oy','dx','dy'],inplace = True)
    
    odpd.to_csv(r"%s/%s"%(save_path,save_name),encoding = "utf-8")


