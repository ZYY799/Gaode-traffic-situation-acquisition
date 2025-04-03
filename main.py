# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 01:02:51 2021

@author: Administrator
"""

# %%

import osmnx as ox
import pandas as pd
import numpy as np
import requests
import codecs
import time

import sys
sys.path.append(r'"C:\Users\ZY\Desktop\早高峰数据抓取\py_lib"')
import Lzuobiao 
# %%
subprocessID = int(sys.argv[1])
print("开始任务", subprocessID)
time_now = time.strftime("%Y-%m-%d-%H-%M",time.localtime())
print("%s"%time.strftime("%Y-%m-%d-%H-%M",time.localtime()))
# %%
# 读取路网节点列表
G = ox.io.load_graphml(r"C:\Users\ZY\Desktop\早高峰数据抓取\路网节点列表\shh2021_fix.graphml")

# %%
def merge_status( tmp_status ):
    tdf = pd.DataFrame(tmp_status)
    tdf["distance"] = tdf["distance"].apply(lambda x:float(x))
    # 如果只有一种交通状态
    if len(tdf["status"].unique()) == 1:
        return tmp_status[0]["status"]
    
    total_dist = tdf["distance"].sum() 
    # 未知、畅通、缓行、拥堵、严重拥堵
    
    if "严重拥堵" in tdf["status"].values:
        return "严重拥堵"
    elif ( tdf[tdf["status"]=="严重拥堵"]["distance"].sum() + tdf[tdf["status"]=="拥堵"]["distance"].sum() ) / total_dist >= 0.5:
        return "拥堵"
    elif ( tdf[tdf["status"]=="严重拥堵"]["distance"].sum() + tdf[tdf["status"]=="拥堵"]["distance"].sum() + 
                      tdf[tdf["status"]=="缓行"]["distance"].sum()  ) / total_dist >= 0.5:
        return "缓行"
    else:
        return "畅通"
# %%
# 高德请求函数
keys = ['XXXXXX',
        'XXXXXX'
]


def get_api_timecost(ind, xys):
    global keys
    key = keys[int(ind) % len(keys)]

    gcj_xys = [Lzuobiao.wgs84togcj02(xx, yy) for xx, yy in xys]

    ori = "{},{}".format(*gcj_xys[0])
    des = "{},{}".format(*gcj_xys[-1])
    waypoints = ";".join(["{},{}".format(xx, yy) for xx, yy in gcj_xys[1:-1]])

    URL = "https://restapi.amap.com/v3/direction/driving?parameters"
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "DNT": "1",
               'User-Agent': 'Mozilla/5.0 ;Windows NT 6.1; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/36.0.1985.143 Safari/537.36',
               'Referer': r'http://ditu.amap.com/',
               'X-Forwarded-For': "%s.%s.%s.%s" % (np.random.randint(1, 240), np.random.randint(1, 240), np.random.randint(1, 240), np.random.randint(1, 240))
               }

    for _try in range(3):
        params = {
            "origin": ori,
            "destination": des,
            "key": key,
            "strategy": "0",  # 0 速度
            "waypoints": waypoints
        }

        response = requests.get(
            URL, params=params, headers=headers, timeout=60)
        answer = response.json()

        if answer["info"] == 'OK':
            return answer

        # DAILY_QUERY_OVER_LIMIT 开发者的日访问量超限，被系统自动封停，第二天0:00会自动解封。
        # ACCESS_TOO_FREQUENT 开发者的单位时间内（1分钟）访问量超限，被系统自动封停，下一分钟自动解封。
        elif answer["info"] == 'DAILY_QUERY_OVER_LIMIT' or answer["info"] == 'ACCESS_TOO_FREQUENT':
            ind += 1
            key = keys[int(ind) % len(keys)]
        else:
            raise

    if _try == 2:
        raise


# %%
# 请求并存储

df = pd.read_csv(r"C:\Users\ZY\Desktop\早高峰数据抓取\generated_cover0505 (1).csv")

# 用于保存
w = codecs.open(r"C:\Users\ZY\Desktop\早高峰数据抓取\15min数据爬取\%s_%d.txt" % (time_now,
                subprocessID), 'a', encoding="utf-8")  # 'a'添加, 'w'新建, 'r'读取
w.write("ind\tpolyline\tspeed\tstatus\n")  # 表头


for ind, line in enumerate(df.values[(subprocessID-1)*1500:subprocessID*1500]):
    print("\r正在处理第%d" % ind, end="")
    # 请求数据
    xys = [[G.nodes[xx]["x"], G.nodes[xx]["y"]] for xx in line]
    answer = get_api_timecost(ind, xys)

    # 判断是否成功
    if answer["status"] == '1':
        pass
    else:
        print("第 {} 行失败".format(ind))
        continue

    # 计算
    steps = answer["route"]["paths"][0]["steps"]
    ttt= pd.DataFrame(steps)[["polyline",'distance','duration','tmcs']]
    ttt["speed"] = ttt.apply(lambda row: float(row["distance"])/float(row["duration"])*3.6,axis = 1)
    # ttt["status"] = ttt["tmcs"].apply(lambda x: merge_status(x))
    #遍历大段
    for i in ttt.index:
        speed = ttt["speed"].at[i]
        tmcs = ttt["tmcs"].at[i]
        for tmc in tmcs:
            line = "\t".join([str(ind), str(tmc['polyline']), str(speed), str(tmc['status'])])+ "\n"
            w.write(line)


    # 存储


w.close()
print("%s"%time.strftime("%Y-%m-%d %H:%M",time.localtime()))

