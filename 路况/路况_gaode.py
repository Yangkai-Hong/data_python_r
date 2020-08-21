import requests           
import json                       
from pymongo import MongoClient         
import time                   

client = MongoClient('localhost',27017)
db = client.Trafic
collection = db.table14_1
point_list = list()
with open("pairs_mesh_WGS84.txt", 'r', encoding='UTF-8') as txt_file:     #坐标对文件可通过arcgis生成渔网的方式加工得到
    for each_line in txt_file:
        if each_line != "" and each_line != "\n":
            # print(each_line)
            fields = each_line.split("\n")
            polygon = fields[0]
            point_list.append(polygon)
    txt_file.close()

def getjson(rectangle):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
    }
    pa = {
        'key': 'xxxxxxxxxxx',  #从控制台申请
        'level': 6,                   #道路等级为6，即返回的道路路况等级最小到无名道路这一级别
        'rectangle':rectangle,        #矩形区域
        'extensions': 'all',
        'output': 'JSON'
    }
    r = requests.get('https://restapi.amap.com/v3/traffic/status/rectangle?', params=pa, headers=headers)
    decodejson = json.loads(r.text)
    return decodejson

for each_point in point_list:
    decodejson = getjson(each_point)
    time.sleep(0.8)
    if len(decodejson)==3:
        print("No Data")
    else:
        if decodejson['trafficinfo']['roads']:
            for each in decodejson['trafficinfo']['roads']:
                try:
                    name = each['name']
                except:
                    name = None
                try:
                    status = each['status']
                except:
                    status = None
                try:
                    lcodes = each['lcodes']
                except:
                    lcodes = None
                try:
                    direction = each['direction']
                except:
                    direction = None
                try:
                    speed = each['speed']
                except:
                    speed = None
                try:
                    polyline = each['polyline'].split(';')
                    for i in range(0, len(polyline)):
                        roadloc = name + ',' + status + ',' + direction + ',' + speed + ','+ polyline[i]
                        dt = time.localtime()
                        ft = "%Y-%m-%d %H:%M:%S"
                        nt = time.strftime(ft, dt)
                        data = {'roadloc': roadloc, 'time': nt, }
                        print(data)
                        collection.insert_one(data)

                except:
                    polyline = None