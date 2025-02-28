# -*- coding: utf-8 -*-

import os
import re
import json
import datetime
import time
import requests


pat_info = re.compile('var def =(.*);!?')
pat_fin = re.compile("hasFlag: '(\d)',")
common_path = "/resource"

campus = None

def modify_json(res_json: dict, load_addr:bool = True) -> dict:
    # load default geo_api_info
    if load_addr:
        with open(os.path.join(common_path, f'{campus}.json'), 'r') as ifile:
            res_json['geo_api_info'] = json.load(ifile)

        res_json['province'] = res_json['geo_api_info']['addressComponent']['province']
        res_json['city'] = res_json['geo_api_info']['addressComponent']['city']
        res_json['address'] = res_json['geo_api_info']['formattedAddress']
        res_json['area'] = ' '.join([
            res_json['province'],
            res_json['city'],
            res_json['geo_api_info']['addressComponent']['district']
        ])
    res_json['date'] = datetime.datetime.now().strftime("%Y%m%d")
    res_json['created'] = int(time.time())
    res_json['ismoved'] = 0
    return res_json


def checkin(cookies_dict: dict, version:int = 1)->bool:
    """
    Args:
        cookies_dict (dict): _description_
        isV2 (bool, optional): V2 no need for addr info. Defaults to False.

    Returns:
        bool: whether suceed to checkin
    """
    # base data
    session = requests.session()
    url = 'https://wfw.scu.edu.cn/ncov/wap/default/index'
    cookiesJar = requests.utils.cookiejar_from_dict(
        cookies_dict, cookiejar=None, overwrite=True)
    session.cookies = cookiesJar
    resp = session.get(url=url)
    if resp.status_code != 200:
        print('[ERROR]', resp.status_code)
        return False

    html = resp.content.decode('utf-8')

    status = len(pat_fin.findall(html)) == 1
    if status: # had checkin
        print("[ERROR] already checkin today")
        session.close()
        return False

    res = pat_info.findall(html)
    if len(res) == 0:
        print('[ERROR] not found')
        return False
    res_json = json.loads(res[0])
    
    # load geo info & modify data
    modify_json(res_json, version == 1)

    # post checkin data
    url = 'https://wfw.scu.edu.cn/ncov/wap/default/save'
    resp = session.post(url=url, data=res_json)
    if resp.status_code == 200:
        resp_json = json.loads(resp.content.decode('utf-8'))
        print(f'[INFO] 签到结果:{resp_json["m"]}')
        return True
    else:
        print(f'[ERROR] 签到失败:{resp.status_code} {resp.content.decode("utf-8")}')
        return False

def all_checkin(file:str, version:int = 1):
    with open(file) as fd:
        data = json.loads(fd.read())
    for person in data:
        if version == 1:
            global campus
            campus=person["CAMPUS"]
        if checkin({
            'eai-sess': person["EAI_SESS"],
            'UUkey': person["UUKEY"]
        },version):
            print(person["name"]+" has checkin")
        else:
            print(person["name"]+" failed to checkin")


if __name__ == '__main__':
    if os.path.exists(f"{common_path}/people.json"):
        print(datetime.datetime.now().strftime("%Y%m%d %H:%M"),end=">>>\n")
        all_checkin(f"{common_path}/people.json",2)
    else:
        print("[ERROR] 文件不存在")
    print("-------------\n") # delim for log
