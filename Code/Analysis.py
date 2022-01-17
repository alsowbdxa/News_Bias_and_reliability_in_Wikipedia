# -*- coding: utf-8 -*-
import os
import pandas as pd
from tqdm import tqdm
from urllib.parse import urlparse
import tldextract #another way to extract the domain name, also works for Ipv6
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import re
import time
import random
tqdm.pandas()

############# The First Block: read the whole dataset of wikipedia ############
# Input the whole WikipediaCitations 
# Read the whole WikipediaCitations
# start

# extract the data from the whole dataset
# read only type_of_citation, URL, citations, page_title, Title
# all the variable description :https://github.com/Harshdeep1996/cite-classifications-wiki/wiki/Taxonomy-of-the-parent-dataset-(1)

#read 200 files
def read_file(INPUT_DATA):
    citations = pd.read_parquet(INPUT_DATA)
    citations_news = citations[['type_of_citation','page_title','Title','citations','URL']]
    return citations_news

# use os to find all the file_name in the dir and read it in order
file_dir = 'E:/First Project/data/dataset.parquet/' # this file include the whole dataset
dirs = sorted(os.listdir(file_dir))[2:] # delete first 2 unrelated files
dataset_news = [] # create a new DataFram to save all the data
for i in tqdm(dirs):  
    content = read_file(file_dir+i)
    dataset_news.append(content)
# cost around 90s
#concat and save the data
result = pd.concat(dataset_news)

# split the data into 100 chunks and save it, the total size is 29276667
for chunksize in tqdm(range(101)):
    chunk = result.iloc[int(len(result)/100)*chunksize:int(len(result)/100)*(chunksize+1)]
    chunk.to_parquet(r'E:\Project 2(Bias and reability on wiki and news)\data\page&url_'+str(chunksize).zfill(3)+'.parquet')

# for the next time reading, the whole data is 6.51 GB
file_dir = r'E:\Project 2(Bias and reability on wiki and news)\data/'
def read_dataset(file_dir):
    dirs = sorted(os.listdir(file_dir))
    data_list = [] # create a new DataFram to save all the data
    for i in tqdm(dirs):  # cost about 67 seconds for 100 files
        content = pd.read_parquet(file_dir+i)
        data_list.append(content)
    data = pd.concat(data_list) #it is the whole dataset we will use
    return data

data = read_dataset(file_dir) #size is 29276667
#test = data.dropna(subset=['URL'])# size is 24956769

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth',100)
data.head()#show the first 5 rows
###################################################################################

############# The Second Block: analysis the filtered dataset with [type_of_citation, URL, citations, page_title, Title] ############
# start analysis
data = read_dataset(file_dir) #size is 29276667
citations_web = data[data['type_of_citation']=='cite web'] #the size is 17297863
citations_news= data[data['type_of_citation']=='cite news'] #the size is 5070203
# for the citations_web part
#test = citations_web.dropna(subset=['URL'])# size is 17203966
#l1=test['URL'].to_list()
# len(set(l1))
# Out[26]: 13386520

# 2 methods to extract the domain name from URL 
from urllib.parse import urlparse # method 1
import tldextract #another way to extract the domain name, also works for Ipv6

data = data.dropna(subset=['URL'])# size is 24956769
data = data[['page_title','URL']]
list_pagetitle = data['page_title'].to_list()
list_url = data['URL'].to_list()

# extract the domain name from the url
#for some urls like:
#'https://web.archive.org/web/20040930213309/http://www.whammo.com.au/encyclopedia.asp?articleid=950'
#it's a archive so need to be edited, it has 38654 urls out of total, and 31369 uniques

#calculate the distribution of archive
#filter the web.archive
t = [x for x in list_url if 'web.archive' in x]
archive_url=[]
for i in tqdm(t):
    try:
        archive_url.append(i[i[4:].index('http')+4:])
    except:
        archive_url.append(i.split('/',5)[-1])
        
#for the case: http:/,use below function to filter
def archive_filter(url):
    if ('http:/w' or 'https:/w') in url:
        return tldextract.extract(url.split('/',1)[-1])[1]
    else:
        return tldextract.extract(url)[1]
archive_source = [archive_filter(x) for x in archive_url] #size sis 38654
c_archive = Counter(archive_source) # size is 14802
dic_archive = dict(c_archive.most_common(100))
x = list(dic_archive.keys())
y = list(dic_archive.values())
#################################################################

#read the googlenews_source, after getting the sources of "news.google" url by script get_news_google_source.py
with open(r"E:\Project 2(Bias and reability on wiki and news)/googlenews_source.pkl",'rb') as f:
    googlenews_source = pickle.load(f)
#already get the google_news sources, which is googlenews_source(a dict)
#replace the news.google with their news sources, costs 17s
for i in tqdm(range(len(list_url))):
    try:
        t = googlenews_source[list_url[i]]
        list_url[i] = t
    except:
        continue

# plot the distribution of new.google source
google_news = [i for i in list_url if 'news.google' in i]#urls contains news.google
google_source = [googlenews_source[i] for i in google_news]
google_source.count('') #12179 not matched

import seaborn as sns

c_google = Counter(google_source)
dic_google = dict(c_google.most_common(100))
x = list(dic_google.keys())
y = list(dic_google.values())
plt.figure(dpi=1080)
sns.set(font_scale=0.6)
sns.barplot(y[1:31],x[1:31],orient='h',color='b')
plt.ylabel('source', fontsize=12)
plt.xlabel('counts', fontsize=12)
####################################################

# re-calculate the domain for all the url
def get_domain_name(x):
    # to delete some symbols from the url, or we may get some wrong domains or raise an error
    x = x.replace('[','')
    x = x.replace(']','')
    x = x.replace(',','')
    # to address the case web.archive
    if 'web.archive' in x:
        try:
            t = x[x[4:].index('http')+4:]
        except:
            t = x.split('/',5)[-1]
        return archive_filter(t)
    domain = tldextract.extract(x)[1] 
    #'http://espn.go.com/nfl/team/transactions/_/name/car/carolina-panthers'
    # will be extract domain 'go'
    if domain =='go' and tldextract.extract(x)[0]!='':
        domain = tldextract.extract(x)[0] 
        if '.' in domain:
            domain  = tldextract.extract(domain)[1] 
    return domain

#update the url list with news.google source
for i in tqdm(range(len(list_url))):  #26s
    try:
        t = googlenews_source[list_url[i]].lower()
        list_url[i] = t
    except:
        continue

archive_map = ''#the dict copy from the github
#https://github.com/Harshdeep1996/politicalBiasSem/blob/main/dataset/archive_mapping.json
for i in tqdm(range(len(list_url))):#10s
    try:
        t = archive_map[list_url[i]]
        list_url[i] = t
    except:
        pass

list_domain = [get_domain_name(x) for x in tqdm(list_url)]# 3m23s, size is 24956769

def count_top(data,top_num):   
    c_ = Counter(data)
    dic_ = dict(c_.most_common(top_num))
    x = list(dic_.keys())
    y = list(dic_.values())
    return x,y

remove_list = ['google','archive','youtube','go','imdb','amazon','twitter',
               'facebook']
#we remove above domain from our domain list









