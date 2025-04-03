# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 14:57:21 2021

@author: THC
"""
def get_odgeo(odpd,ywfile,disdinct = False):
    import sys
    sys.path.append(r"E:BigData/tuhongchang/py_lib")
    from get_yw_attributes import get_xy 
    import geopandas as gpd
    import pandas as pd
    from shapely.geometry import Point,LineString

    grid_dict = get_xy(ywfile)
    
    #生成对应的坐标和线
    
    odpd["oxy"] = [grid_dict[x] for  x in odpd["oid"].values]
    odpd["dxy"] = [grid_dict[x] for  x in odpd["did"].values]
    odpd["line"] = [LineString(z) for z in odpd[["oxy","dxy"]].values.tolist()]
    #构建geopandas
    odgeo =gpd.GeoDataFrame(odpd,geometry = "line")
    odgeo = odgeo.set_crs(epsg=4326)
    odgeo.drop(columns=["oxy","dxy"],inplace = True)
    
    if disdinct == True:
        odgeo_disdinct = None
        x= 0
        for row in odgeo[odgeo["num"] > 1].iterrows():
            x+=1
            print("\r已经处理了%d行od,共%d"%(x,len(odgeo)),end = '')
            try:
                odgeo_disdinct =  pd.concat([ odgeo_disdinct,pd.concat([row[1].to_frame().T]*row[1].num,axis = 0)],axis = 0)
            except:
                odgeo_disdinct = row[1].to_frame().T
        
        return odgeo_disdinct
    
    else:
        return odgeo