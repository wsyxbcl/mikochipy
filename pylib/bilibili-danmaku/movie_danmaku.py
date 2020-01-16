#!/usr/bin/python3
from datetime import date, timedelta
import requests
import time
import xml.etree.ElementTree as ET 

import numpy as np
import selenium.webdriver

# def Danmaku():

def get_movie_danmaku(session, oid, date, header, save=True):
    """
    GET .xml file by oid and date through bilibili API
    """
    danmaku = []
    url = "https://api.bilibili.com/x/v2/dm/history?type=1&oid={}date={}".format(oid, date)
    print("GET "+url)
    response = session.get(url, headers=header)
    response.encoding = 'utf-8'
    if save:
        with open('./data/xml/'+oid+'_'+date+'.xml', 'w') as f:
            f.write(response.text)
    xml_root = ET.fromstring(response.text)
    for d in xml_root.findall('d'):
        danmaku.append([d.get('p'), d.text])
    return danmaku

if __name__ == '__main__':
    # Date
    start_date = date(2019, 12, 25)
    end_date = date(2020, 1, 10)
    dates = []
    delta = timedelta(days=1)
    while start_date <= end_date:
        dates.append(start_date.strftime("%Y-%m-%d"))
        start_date += delta
    danmaku_list = []
    oid = '112148195&'
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0'} 
    
    # Manual login first
    driver = selenium.webdriver.Chrome()
    driver.get("https://www.bilibili.com")
    while input("Waiting for login, 'CHECK' to continue: ") != 'CHECK':
        pass
    print("GOTCHA")
    
    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    for date in dates:
        danmaku_list += get_movie_danmaku(s, oid, date, header)
        time.sleep(10)
