import pandas as pd
import numpy as np
import requests
import json
import os

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
    'c4883baa101420590108e9ce0a2cfedd',
    '3e2acbe01c50a83bc5a44b47bde7a858', 
    'b51c10debdc93f34fb7b394bb866d8ea',
    '1c8507536f43a843bd25b9007eb638b5',
    '2355ca58db9271a092fd1fbc9be0e818',
    '34a92ac53696fc9dfc47cbdf70922449',
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
            duration = decodejson['route']['paths'][0]['duration']
            distance = decodejson['route']['paths'][0]['distance']
        elif route_type == 'walking':
            r = requests.get('https://restapi.amap.com/v3/direction/walking?', params=pa)
            decodejson = json.loads(r.text)
            duration = decodejson['route']['paths'][0]['duration']
            distance = decodejson['route']['paths'][0]['distance']
        elif route_type == 'transit':
            r = requests.get('https://restapi.amap.com/v3/direction/transit/integrated?', params=pa)
            decodejson = json.loads(r.text)
            duration = decodejson['route']['transits'][0]['duration']
            return duration
            #distance = decodejson['route']['paths'][0]['distance']
        elif route_type == 'bicycling':
            r = requests.get('https://restapi.amap.com/v4/direction/bicycling?', params=pa)
            decodejson = json.loads(r.text)
            duration = decodejson['data']['paths'][0]['duration']
            distance = decodejson['data']['paths'][0]['distance']
        result = str(duration) + ',' + str(distance)
        #print(result)
        return result 
    except:
        #print('error')
        return ','

def save_transit(file_name, key):
    def transit(origin, dest, key):
        pa = {
            'key': key,
            'origin': origin,
            'destination': dest,
            'city': '深圳' # 这里要改城市
        }
        try:
            r = requests.get('https://restapi.amap.com/v3/direction/transit/integrated?', params=pa)
            decodejson = json.loads(r.text)
            duration = decodejson['route']['transits'][0]['duration']
            #print(duration)
            return duration
        except Exception as e:
            print(e)
            return ','

    import datetime
    print(datetime.datetime.now(), file_name, ' start...')
    df = pd.read_excel(file_name)
    df['公交时间']=df.apply(lambda row: transit(row['origin'], row['dest'], key), axis=1)
    new_file_name = '公交' + file_name
    df.to_excel(new_file_name)
    print(datetime.datetime.now(), new_file_name, 'done!')

import threading
try:
    #t1 = threading.Thread(target=save_file, args=('od1.xlsx', 'driving', k_list[13],))
    #t2 = threading.Thread(target=save_transit, args=('od1.xlsx', k_list[14],))
    #t3 = threading.Thread(target=save_file, args=('od1.xlsx', 'bicycling', k_list[13],))
    #t4 = threading.Thread(target=save_file, args=('od2.xlsx', 'driving', k_list[12],))
    t5 = threading.Thread(target=save_transit, args=('od2.xlsx', k_list[12],))
    #t6 = threading.Thread(target=save_file, args=('od2.xlsx', 'bicycling', k_list[12],))
    #t1.start()
    #t2.start()
    #t3.start()
    #t4.start()
    t5.start()
    #t6.start()
except Exception as e:
    print(e)