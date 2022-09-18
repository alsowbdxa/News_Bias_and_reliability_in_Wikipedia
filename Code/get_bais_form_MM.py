# -*- coding: utf-8 -*-
"""
"""
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlrd
import re
import math
import time
import random
import json
from tqdm import tqdm
import csv

#extract the news bias scores from the media monitor 
# example link: https://twitter-app.mpi-sws.org/media-bias-monitor/search.php?query=guardian
ua = [
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
  		'Opera/8.0 (Windows NT 5.1; U; en)',
  		'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
  		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
  		'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
  		'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
  		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
  		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
  		'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
  		'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
  		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
  		'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
  		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
  		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
  		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
  		'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
  		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
      ]


header = {
    'Connection': 'close',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Origin': 'https://twitter-app.mpi-sws.org',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://twitter-app.mpi-sws.org/media-bias-monitor/search.php?query=worcest',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': #use youself cookie
}
#read the domain file
file_name = #input the domain name to extract the data from Media Bias Monitor, which you can get from the main dataset: Wikipedia Citations
list_domain = []
for line in open(file_name,"r"): 
    list_domain.append(line.strip())

# send the parm to the url and get it's url and interest_id,which could be used to 
# get the second page of more details.
# change the variable query to search different news sources
# First page: query
def search_news(domain_name):
    # proxy = {'http':random.choice(ip)}
    url = 'https://twitter-app.mpi-sws.org/media-bias-monitor/exec_process.php'
    # data = {"op":"2",'query':'guardian'}
    payload = {"op":"2",'query':domain_name}
    res = requests.post(url=url,data=payload,headers=header)
    time.sleep(random.randint(1,6))
    try:
        res = json.loads(res.text)
    except:
        res = {'status': 'False', 'response': []}
    return res

# Second page
# contains political bias scores, age, education, gender, incom_level an so on
# the interest_id got from the first step need to be used as query parm here
def get_detail(interest_id):
    # proxy = {'http':random.choice(ip)}
    details_url = 'https://twitter-app.mpi-sws.org/media-bias-monitor/exec_process.php'
    # payload = {"op":"1",'query':'6002989675044'}
    payload = {"op":"1",'query':interest_id}
    try:
        res1 = requests.post(url=details_url,data=payload,headers=header)
        res1 = json.loads(res1.text)
        time.sleep(random.randint(1,5))
    except:
        time.sleep(random.randint(1,5))
        res1 = requests.post(url=details_url,data=payload,headers=header)
        res1 = json.loads(res1.text)
    return res1
##############################################################################################
#start to extract, here the list_domain is a unique list of domain name
page_1 = dict()#this dictionary is to store the relationship between domain and
               #related results, we use the interesi_id here to get details of domain
page_2 = dict()#this dict is use to store the detail information for each results
short_break = 1

for i in tqdm(list_domain):
    if i in page_1:
        continue   
    while 1:       
       try: 
            header['User-Agent'] = random.choice(ua)
            result_1 = search_news(i)
            if result_1['status'] == 'ok':
                page_1[i] = result_1
                with open(r"MM_page1.txt",'a',encoding='utf8') as f:
                    f.write(str([i,result_1]))
                    f.write('\n')
                if result_1['response'] == '' or result_1['response'] == []:
                    break
                else:
                    t = dict()
                    for info in tqdm(result_1['response'][:100]):
                        detail = get_detail(info['interest_id'])
                        t[info['title']] = detail
                    page_2[i] = t
                  
                    with open(r"MM_page2.txt",'a',encoding='utf8') as f:
                        f.write(str([i,t]))
                        f.write('\n')
                    break
            else:
                break
       except:
            time.sleep(10)
       if short_break >3:
           short_break = 1
           break
       else:
           short_break+=1 
#save the data and they will be used later in analysis file.
with open("MM_page1_dict.pkl",'wb') as f:
    pickle.dump(page_1,f)

with open(r"MM_page2_dict.pkl",'wb') as f:
    pickle.dump(page_2,f)
