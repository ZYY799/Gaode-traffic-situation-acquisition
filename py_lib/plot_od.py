# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 14:35:39 2021

@author: THC
"""
def plot_od(odfile,basefile,ywfile):
    
    import sys
    sys.path.append(r"E:BigData/tuhongchang/py_lib")
    from get_odgeo import get_odgeo

    import pandas as pd
    import numpy as np
    import math
    import matplotlib as mpl
    import geopandas as gpd
    from matplotlib import pyplot as plt
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
    
    #read files
    odpd = pd.read_csv(r'%s'%odfile)
    base = gpd.read_file(r'%s'%basefile)
    waihuan = gpd.read_file(r'E:/BigData/tuhongchang/data/新城and环/外环_线.shp')
    neihuan = gpd.read_file(r'E:/BigData/tuhongchang/data/新城and环/内环_线.shp')
    print('reading files odpd...')
    
    #set crs
    base = base.to_crs(epsg=4326)
    waihuan =waihuan.to_crs(epsg = 4326)
    neihuan =neihuan.to_crs(epsg = 4326)
    print('from odpd to odgeo...')
    odgeo = get_odgeo(odpd,ywfile,disdinct =False)
    #odgpd =gpd.GeoDataFrame(odgeo,geometry = "line")
    #odgpd = odgpd.set_crs(epsg=4326)
    
    
    #odgpd.to_file(r"E:\BigData\tuhongchang\拥堵\数据\odge_3000_new.shp")
    #odgpd = gpd.read_file(r"E:/BigData/tuhongchang/拥堵/数据/odge_3000_new.shp")
    #odgpd = odgpd.set_crs(epsg=4326)
    #odgpd["num"] = odgpd["num"].apply(lambda x: eval(x))

    
    for date in odgeo.date.unique():
        
        print('drwaing date %d'%date)
        od_date = odgeo[(odgeo["date"] == date) & (odgeo["num"]> 1)]
    
    
        fig, ax = plt.subplots(figsize = (15,15))
        ax.set_facecolor("w")
        ax.set_xlim((120.8,122.0))
        ax.set_ylim((30.65,31.55))
        #ax.set_xlim((121.2,121.8))
        #ax.set_ylim((30.95,31.45))

        cmap = mpl.colors.ListedColormap(["red"])
        date = str(date)
        if date[3] =="0":
            ax.set_title("11月%s日%s:00-%s:30"%(date[0],date[2],date[2]),fontsize = 24)
        if  date[3] =="3":
            ax.set_title("11月%s日%s:30-%s:00"%(date[0],date[2],str(int(date[2])+1)),fontsize = 24)
        base.plot(ax = ax,edgecolor="black",facecolor = "white",legend = True,linewidth =0.2)
        waihuan.plot(ax = ax,edgecolor="black",facecolor = "None",legend = True,linewidth =1)
        neihuan.plot(ax = ax,edgecolor="black",facecolor = "None",legend = True,linewidth =1)

    
        od_date.plot(ax=ax,column="num",legend = False,linewidth = (od_date["num"])/10,
                     cmap = cmap,alpha = 0.1
                     #,scheme = "user_defined",classification_kwds={'bins':[10,20,30]}
                     )
        
        #保存图片
        plt.savefig(r"E:\BigData\tuhongchang\拥堵\中间结果\od3000_new\%s.jpg"%(date),dpi = 80)
    
