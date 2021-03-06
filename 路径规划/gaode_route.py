# coding=utf-8
import pandas as pd
import numpy as np
import requests
import json

k_list = [
    '5d4b115272a3ab7e871d1a719012b2a2',
    '7e3ca10787de5a314b6d85c6030b31e3',
    '3b90335174433a8a08014077a16ab202',
    '4dd40b220165ad9cd73d0c829b377d8a',
    '630f9c0cfe7e7dbad380fd447d268fcd',
    '9580b7a69f1f05dcd74d32e349c5bc0b',
    '8f5ae1c47298ba3954f05e6b48effdb1',
    '83853b0648f942f8fc3833d0de260976',
    '999450bcf9bf1f545ca3e3a9bc105ca1',
    'cb90b8b2e5083286c4fd5336e0554ce5',
    'c4883baa101420590108e9ce0a2cfedd', # 吴泽宇 30000
    '3e2acbe01c50a83bc5a44b47bde7a858', # 吴泽宇 30000
    'b51c10debdc93f34fb7b394bb866d8ea', # 吴泽宇 30000
    '1c8507536f43a843bd25b9007eb638b5', # 吴泽宇 30000
    '2355ca58db9271a092fd1fbc9be0e818', # 吴泽宇 30000
    '34a92ac53696fc9dfc47cbdf70922449', # 2000
]

def gaode_direction(origin, dest, route_type, key):
    pa = {
        'key': key,
        'origin': origin,
        'destination': dest
    }
    try:
        if route_type == 'driving':
            r = requests.get('https://restapi.amap.com/v3/direction/driving?', params=pa)
            decodejson = json.loads(r.text)
            duration = decodejson['route']['paths'][0]['duration'] # 秒
            distance = decodejson['route']['paths'][0]['distance'] # 米
            return str(duration) + ',' + str(distance)
        elif route_type == 'bicycling':
            r = requests.get('https://restapi.amap.com/v4/direction/bicycling?', params=pa)
            decodejson = json.loads(r.text)
            duration = decodejson['data']['paths'][0]['duration'] # 秒
            distance = decodejson['data']['paths'][0]['distance'] # 米
            return str(duration) + ',' + str(distance)
    except:
        return ','

def save_data(file_name, key, method):
    import datetime
    print(datetime.datetime.now(), file_name, ' start...')
    df = pd.read_excel(file_name)
    if method == 'bicycling':
        df['duration_distance_bicycling']=df.apply(lambda row:gaode_direction(row['居民点location'],row['设施点location'],'bicycling',key),axis=1)
        df.to_excel('ssd79_bicycling.xlsx')
    elif method == 'driving':
        df['duration_distance']=df.apply(lambda row:gaode_direction(row['居民点location'],row['设施点location'],'driving',key),axis=1)
        df.to_excel('ssd79_driving.xlsx')
    print(datetime.datetime.now(), file_name, ' done!')

# 多线程爬数据
import threading
try:
    t1 = threading.Thread(target=save_data, args=('ssd79.xlsx', k_list[0], 'bicycling'))
    t2 = threading.Thread(target=save_data, args=('ssd79.xlsx',k_list[1], 'driving'))
    t1.start()
    t2.start()
except Exception as e:
    print(e)