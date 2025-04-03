# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import os
import geopandas as gpd


fishnet_path = r"E:/BigData/tuhongchang/手机信令/辽宁手机数据/anshan_1.shp"
csvpack_path = r"E:\BigData\tuhongchang\手机信令\辽宁手机数据\鞍山数据"
shp_path = r"E:\BigData\tuhongchang\手机信令\辽宁手机数据\鞍山shp"
fishnet = gpd.read_file(fishnet_path)


for i in range(1,len(list(os.walk(csvpack_path)))):
    newshp = fishnet.copy()
    if "OD" in list(os.walk(csvpack_path))[0][1][i-1]:
        for csvfile in list(os.walk(csvpack_path))[i][2]:
            csvdf = pd.read_csv(os.path.join(list(os.walk(csvpack_path))[i][0],csvfile))
            newcol = [x[-9:] for x in csvdf.columns.values.tolist()]
            csvdf.columns = newcol
            
            s_df = csvdf.groupby("s_id",as_index = False).sum()
            s_df.drop(columns = ["e_id"],inplace = True)
            s_newcol = [x[-9:] +"s" if x !="s_id" else x for x in s_df.columns.values.tolist() ]
            s_df.columns = s_newcol
            
            e_df = csvdf.groupby("e_id",as_index = False).sum()
            e_df.drop(columns = ["s_id"],inplace = True)
            e_newcol = [x[-9:] +"e" if x !="e_id" else x for x in e_df.columns.values.tolist() ]
            e_df.columns = e_newcol
            
            newshp =pd.merge(newshp, s_df, left_on='TID',right_on ="s_id", how='left')
            newshp =pd.merge(newshp, e_df, left_on='TID',right_on ="e_id", how='left')
            newshp.drop(columns = ["s_id","e_id"],inplace = True)
            
        newshp.to_file(os.path.join(shp_path,list(os.walk(csvpack_path))[0][1][i-1]),encoding = 'utf-8')

        
        
    else:
        for csvfile in list(os.walk(csvpack_path))[i][2]:
            csvdf = pd.read_csv(os.path.join(list(os.walk(csvpack_path))[i][0],csvfile))
            newcol = [x[-10:] for x in csvdf.columns.values.tolist()]
            csvdf.columns = newcol
            newshp =pd.merge(newshp, csvdf, left_on='TID',right_on ="tid", how='left')
            newshp.drop(columns = ["tid"],inplace = True)
            
        newshp.to_file(os.path.join(shp_path,list(os.walk(csvpack_path))[0][1][i-1]),encoding = 'utf-8')

