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
file_dir = '.../data/dataset.parquet/' # this file include the whole dataset
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
    chunk.to_parquet(r'...\data\page&url_'+str(chunksize).zfill(3)+'.parquet')

# for the next time reading, the whole data is 6.51 GB
file_dir = r'...\data\'
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
data = read_dataset(file_dir) #size is 29276667, read the file with your direction
citations_web = data[data['type_of_citation']=='cite web'] #the size is 17297863
citations_news= data[data['type_of_citation']=='cite news'] #the size is 5070203

# method to extract the domain name from URL 
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
        domain = '.'.join(tldextract.extract(url.split('/',1)[-1]))
    else:
        domain = '.'.join(tldextract.extract(url))
    if domain[0]=='.':
        domain = domain[1:]
    return domain

archive_source = [archive_filter(x) for x in archive_url] #size sis 38654
c_archive = Counter(archive_source) # size is 14802
dic_archive = dict(c_archive.most_common(100))
x = list(dic_archive.keys())
y = list(dic_archive.values())
#################################################################

#read the googlenews_source, after getting the sources of "news.google" url by script get_news_google_source.py
with open(r"googlenews_source.pkl",'rb') as f:
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

# calculate the domain for all the url
def archive_filter(url):
    if ('http:/w' or 'https:/w') in url:
        domain = '.'.join(tldextract.extract(url.split('/',1)[-1]))
    else:
        domain = '.'.join(tldextract.extract(url))
    if domain[0]=='.':
        domain = domain[1:]
    return domain

def get_domain_name(x):
    # to delete some symbols from the url
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
    domain = '.'.join(tldextract.extract(x))
    if domain[0]=='.':
        domain = domain[1:]
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

###################################################################################################################
# plot the cumlative distribution of top 10w domains of all, these 10w domains can be used in script:get_bais_form_MM.py to extract bias data.
l1 = list(data.domain.value_counts(normalize=True,dropna=False).cumsum(axis=0))
x = range(len(l1))
# plt.figure(dpi=900)
plt.rcParams['figure.dpi'] = 600
plt.ticklabel_format(style='plain')#
plt.plot(x,l1)
plt.title('cumulative number of domain')
plt.xlabel("unique domains",fontsize=12)
plt.ylabel("percentage of citations", fontsize=12)
plt.xticks([i*200000 for i in range(9)],['0','200k','400k','600k','800k','1000k','1200k','1400k','1600k'],fontsize=12)
position = 100000  #
plt.axvline(x[position], color='r', linestyle='--')
plt.text(x[position], l1[position], ' (%d,%.2f)' % (x[position],l1[position]), ha='left', va= 'top',fontsize=10)
plt.tight_layout()
###################################################################################################################

# then match the domain with political bias from Media Bias Monitor(https://twitter-app.mpi-sws.org/media-bias-monitor/)
# you can find more detail about how to extract in the script "get_bais_form_MM.py"
with open(r"\MM_page1_dict.pkl",'rb') as f:
    MM_page1_dict = pickle.load(f)

with open(r"\MM_page2_dict.pkl",'rb') as f:
    MM_page2_dict = pickle.load(f)
    
###################################################################################################################
#match bias score from MBM
def match_mm(x):
    try:
        return MM_page1_dict[x]
    except:
        return None
    
data['data'] = data.domain.progress_apply(lambda x:match_mm(x))

data_mm = data.dropna(subset=['data'])#size is 4866655, None is 24410012
len(data_mm.page_title.unique()) #1180508

data_mm['cate_num_data'] = data_mm['data'].progress_apply(lambda x: '10+' if str(x).count('interest_id')>10 else str(str(x).count('interest_id')))

#plot the distribution of MM results and domains.
x = list(dict(data_mm["cate_num_data"].value_counts()).keys())
y = list(dict(data_mm["cate_num_data"].value_counts()).values())
x.append('NaN')
y.append(24410012)
py = [i/sum(y) for i in y]#percentage

plt.figure(dpi=900)
plt.ticklabel_format(style='plain')
ax = sns.barplot(x=x,y=py,order=['1','2','3','4','5','6','7','8','9','10','10+','NaN'],color="#0000ff")
plt.xlabel("Number of results in MBM",fontsize=12)
plt.ylabel("citations", fontsize=12)
plt.tight_layout()
###plot the distribution of MM results and domains end.
###################################################################################################################

unique_s_data = data_mm[['domain','data']].drop_duplicates(['domain']) #5220

#use this method to extract bias score(with average bias score)
from urllib.parse import urlparse#some urls have subdictionary

def bias_score2(x1,x2): #x1 is data, x2 is domain
    try:
        # domain_mm = [get_domain_name(i['url']) for i in x1]
        domain_mm = [urlparse(i['url']).path for i in x1]
        title_mm = [i['title'] for i in x1]
        # title = [i['title'] for i in x1]
        # dic = eval(domain2mm[x2])
        xname = x2.replace('www.','')
        if (xname in domain_mm) or (xname in title_mm):# if exactly match, use it       
            try:
                return MM_page2_dict[title_mm[domain_mm.index(xname)]]['political_bias']
            except: #if doesn't have exact match, use the average score
                bias_score = np.mean([MM_page2_dict[i]['political_bias'] for i in title_mm])
                return bias_score
        else:#if cannot exactly match, use average score
            bias_score = np.mean([MM_page2_dict[i]['political_bias'] for i in title_mm])
            return bias_score
    except:# if doesn't have match result, ignore it
        return None  
unique_s_data['bias_score_avg'] = unique_s_data.progress_apply(lambda x: bias_score2(x['data'],x['domain']),axis=1)
#size is 5220

match_bias = unique_s_data[['domain','bias_score_avg']].copy() 
# final_data: citations with bias score
final_data = pd.merge(data_mm,match_bias,on='domain',how='left')#size is 4866655
# drop the final_data without the bias scores
final_data.dropna(subset=['bias_score_avg'],inplace=True) #size is 4866377

#final_data.domain.to_list().count('www.youtube.com')#size is 412424
#final_data_noyoutube = final_data[final_data['domain']!='www.youtube.com')|final_data['domain']!='youtube.com')]# use if needed

###################################################################################################################
# Now we have equipped each domain with their bias score, then we are going to analyse and visualize it.
# plot the kde plot
sns.set_style('whitegrid')
plt.rcParams['figure.dpi'] = 600
plt.figure(figsize=(12,8))
plt.ticklabel_format(style='plain')
ax1 = sns.distplot(final_data['bias_score_avg'], hist=False, kde_kws={'label':'bw=0.5','bw':0.5},bins=10, color="#0000ff") # binwidth=0.2, ax=ax1)
ax1.axvline(final_data['bias_score_avg'].mean(),color='red',ls='-',label='mean(%.2f)'%(final_data['bias_score_avg'].mean()))
ax1.axvline(final_data['bias_score_avg'].median(),color='black',ls='dotted',label='median(%.2f)'%(final_data['bias_score_avg'].median()))
ax1.legend(fontsize=14)
ax1.tick_params(labelsize=15)
ax1.set_xlabel('Bias score', fontsize=20)
ax1.set_ylabel('Kde', fontsize=20)
plt.tight_layout()
###################################################################################################################

###################################################################################################################
#Then let's match topic to final_data
# here the topic file can be found in https://github.com/alsowbdxa/Code-of-Science-in-Wikipedia/blob/main/Code/Adding_topic_from_Wikipedia_API.py
# read the final topic dataset,size is 3744440
with open('page2topic_final.pkl','rb') as f:
    page2topic = pickle.load(f)
    
def match_topic(x):
    try:
        return page2topic[x]
    except:
        return None
final_data['new_topic'] = final_data['page_title'].progress_apply(lambda x:match_topic(x))

citations_bias_features = final_data.dropna(subset=['new_topic']) #size is 4828650

#remove the page without topic
mask = (
    (citations_bias_features['new_topic']=='') |
    (citations_bias_features['new_topic']=='[[], []]')
    )

citations_bias_features = citations_bias_features[~mask] #size is 4820380
#
#plot the top10 and macro topic with avg_bias_score and their percentage of wiki articles
unique_page_title = citations_bias_features.drop_duplicates(subset=['page_title'])#size is 1167389

# we use fractional counting in our analysis
#this method for all topics
def fract_topic(x):
    c = Counter()
    for i in x:    
        t = eval(i)
        frac_t = [i/sum(t[1]) for i in t[1]]
        c1 = Counter(dict(zip(t[0],frac_t)))
        c.update(c1)
    return c
# this one onle for 4 macro topics
def fract_topic(x): #this for main topic
    c = Counter()
    for i in x:    
        t = [n.split('.')[0] for n in eval(i)[0]]
        frac_t = dict()
        for topic in list(set(t)):
            # frac_t[topic] = round(t.count(topic)/len(t),2)
            frac_t[topic] = t.count(topic)/len(t)
        c.update(frac_t)
    return c

##############################################################################
#top10 version
top10 = [i[0] for i in l.most_common(10)]
l = [[],[]]
for i in tqdm(top10):
    t = unique_page_title[unique_page_title['new_topic'].str.contains(i)]['bias_score_avg'].to_list()
    l1[0].extend([i]*len(t))
    l1[1].extend(t)
top10_violin = pd.concat([pd.DataFrame(i) for i in l],axis=1)#size is 2446985
top10_violin.columns=['topic','bias_score_avg']
##############################################################################
#macro topic version
macro_topic = [i[0] for i in l.most_common()]
l = [[],[]]
for i in tqdm(macro_topic):
    t = unique_page_title[unique_page_title['new_topic'].str.contains(i)]['bias_score_avg'].to_list()
    l1[0].extend([i]*len(t))
    l1[1].extend(t)
macro_violin = pd.concat([pd.DataFrame(i) for i in l],axis=1)#size is 2446985
macro_violin.columns=['topic','bias_score_avg']
##############################################################################
#plot the violin figure 
#for top10 topics
x = top10
y = [i[1]/sum(l.values()) for i in l.most_common(10)]
#
#for macro topic
x = macro_topic
y = [i[1]/sum(l.values()) for i in l.most_common(10)]
##############################################################################
###plot the top10 version of topic
pl = sns.color_palette("Blues_r",15)
plt.figure(dpi=600)
grid = plt.GridSpec(1, 7, wspace=0.2, hspace=0.5)
plt.subplot(grid[0,0:5])
ax1 = sns.violinplot(y=top10_violin["topic"], x=top10_violin["bias_score_avg"],order=x,palette=pl)
ax1.set_title('Distribution of top10 topics bias score', fontsize=10)
ax1.set_xlabel('Bias score', fontsize=10)
ax1.set_ylabel('Topics', fontsize=10)
ax1.set_yticklabels([i.split('*')[0] for i in x])
plt.subplot(grid[0,5:7])
ax2 = sns.barplot(x=y, y=x, palette=pl)
ax2.set_yticklabels([])
ax2.set_xlabel('Percentage of articles', fontsize=10)
##############################################################################
#for macro topic
pl = sns.color_palette("Blues_r",15)
plt.figure(dpi=600)
grid = plt.GridSpec(1, 7, wspace=0.2, hspace=0.5)
plt.subplot(grid[0,0:5])
ax1 = sns.violinplot(y=macro_violin["topic"], x=macro_violin["bias_score_avg"],order=x,palette=pl)
ax1.set_title('Distribution of macro topics bias score', fontsize=10)
ax1.set_xlabel('Bias score', fontsize=10)
ax1.set_ylabel('Topics', fontsize=10)
ax1.set_yticklabels([i.split('*')[0] for i in x])
plt.subplot(grid[0,5:7])
ax2 = sns.barplot(x=y, y=x, palette=pl)
ax2.set_yticklabels([])
ax2.set_xlabel('Percentage of articles', fontsize=10)
##############################################################################
###################################################################################################################

# use fractional counting for wk_projects, to plot the distribution of project in different bias score group
def get_project(x):
    try:
        return page2project[x]
    except:
        return None
final_data['wk_project'] = final_data['page_title'].progress_apply(lambda x: get_project(x))

citations_bias_project = final_data.dropna(subset=['wk_project']) #size is 801329
unique_page_title = citations_bias_project.drop_duplicates(subset=['page_title'])#size is 107653

##############################################################################
def fract_project(x):#use fractional counting to project
    c = Counter()
    for i in x:
        t = eval(i)
        t1 = list(set(t))
        n = [t.count(i)/len(t) for i in t1] 
        c.update(dict(zip(t1,n)))
    return c

l_project = fract_project(unique_page_title['wk_project'].to_list()) #size is 2582
#top10 projects
top10 = [i[0] for i in l_project.most_common(10)]
l1 = [[],[]]
for i in tqdm(top10):
    t = unique_page_title[unique_page_title['wk_project'].str.contains(i)]['bias_score_avg'].to_list()
    l1[0].extend([i]*len(t))
    l1[1].extend(t)
top10_violin = pd.concat([pd.DataFrame(i) for i in l1],axis=1)
top10_violin.columns=['wk_project','bias_score_avg']

x = top10
y = [i[1]/sum(l_project.values()) for i in l_project.most_common(10)]
###############################################################################
###plot top10 project
# pl = sns.color_palette("Greens_r",15)
pl = sns.color_palette("Blues_r",15)
plt.figure(dpi=600)
grid = plt.GridSpec(1, 7, wspace=0.2, hspace=0.5)
plt.subplot(grid[0,0:5])
ax1 = sns.violinplot(y=top10_violin["wk_project"], x=top10_violin["bias_score_avg"], order=x, palette=pl)
ax1.set_title('Distribution of top10 wk_project bias score', fontsize=10)
ax1.set_xlabel('Bias score', fontsize=10)
ax1.set_ylabel('Wiki_project', fontsize=10)
ax1.set_yticklabels(x)
plt.subplot(grid[0,5:7])
ax2 = sns.barplot(x=y, y=x, palette=pl)
ax2.set_yticklabels([])
ax2.set_xlabel('Percentage of articles', fontsize=10)
###############################################################################
    
###################################################################################################################
# Reliability part, get data from script "get_reliability_form_MBFC.py"
#read mbfc data, whihc is extracted from Media Bias Fact Check(https://mediabiasfactcheck.com/)
mbfc = pd. read_excel('mbfc.xlsx') 

mbfc_data = mbfc[['Title','URL','cate','bias_rating','Factual Label','Country','Traffic/Popularity']]
mbfc_data.columns = ['news_source','url','bias','bias_rating','factual','country','traffic']

mbfc_data = mbfc_data[mbfc_data['factual']!='Not Found'] #not found has 99 data
mbfc_data['domain'] = mbfc_data.url.progress_apply(lambda x:get_domain_name(x))

match = mbfc_data[['domain','factual']]# size is 3586
match['code'] = match['domain'].progress_apply(lambda x:x.replace('www.',''))

final_data['code'] = final_data['domain'].progress_apply(lambda x:x.replace('www.',''))#4866377

citations_bias_factual = pd.merge(final_data,match,on='code',how='left')#size is 5150954

citations_bias_factual.dropna(subset=['factual'],inplace=True)#size is 3041283

###############################################################################
#plot the distribution of factual and bias
pl = sns.diverging_palette(140,15,s=100,l=60,n=6)
plt.figure(figsize=(10,6),dpi=900)
plt.ticklabel_format(style='plain')
ax = sns.countplot(x='factual',data=citations_bias_factual,order=['VERY HIGH','HIGH','MOSTLY FACTUAL','MIXED','LOW','VERY LOW'],palette=pl)
plt.tick_params(labelsize=14)
plt.xlabel('Reliability', fontsize=14)
plt.ylabel('Citation count', fontsize=14)
ax.tick_params(labelsize=14)
plt.tight_layout()
###############################################################################

match['url'] = match['code'].progress_apply(lambda x:'www.'+x)
match_test = match.drop_duplicates(subset=['url'])
domain2factual = dict(zip(match_test['url'],match_test['factual'])) #size is 3557

###############################################################################
# plot top10 news resource with their reliability in different bias level
citations_categories_not_null = citations_bias_factual[~citations_bias_factual['factual'].isnull()]
#size is 3041283, the same with citations_bias_factual
citations_bias_factual.columns
citations_categories_not_null['discretized_score'] = pd.cut(
    citations_categories_not_null['bias_score_avg'],
    bins=[-2.0, -1.0, 0, 1.0, 2.0], 
    labels=['-2 to -1', '-1 to 0', '0 to 1', '1 to 2'])

aggregated_discretized_cat = citations_categories_not_null[['discretized_score', 'domain_x']].groupby(
    'discretized_score')['domain_x'].apply(list).reset_index()
aggregated_discretized_cat['count_categories'] = aggregated_discretized_cat['domain_x'].progress_apply(
    lambda x: Counter([item for item in x]) )
discretized_labels = list(aggregated_discretized_cat['discretized_score'])
aggregated_discretized_cat
aggregated_discretized_cat.columns
fig, axes = plt.subplots(2, 2, figsize=(25, 25))
plt.subplots_adjust(wspace=0.6)
axes = axes.flatten()
al = sns.color_palette("Dark2",6)
plt.figure(dpi=600)
for index in range(len(discretized_labels)):
    discretized_label_score = aggregated_discretized_cat[
        aggregated_discretized_cat['discretized_score'] == discretized_labels[index]][
        'count_categories'].values[0].most_common(10)
    subset_cat = pd.DataFrame(discretized_label_score)
    sum_subset_cat = subset_cat[1].sum()
    subset_cat[1] = subset_cat[1].apply(lambda x: float(x) / sum_subset_cat)#calculate the percentage of factual
    subset_cat[2] = subset_cat[0].apply(lambda x: domain2factual[x] if 'www.' in x else domain2factual['www.'+x])
    ax = sns.barplot(x=1, y=0, hue=2, data=subset_cat, ax=axes[index],palette=al,dodge=False,hue_order=['VERY HIGH','HIGH','MOSTLY FACTUAL','MIXED','LOW','VERY LOW'])
    ax.set_title(discretized_labels[index], fontsize=30)
    ax.set_xlabel('', fontsize=20)
    ax.set_ylabel('', fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=25)
    ax.tick_params(axis='both', which='minor', labelsize=25)
    ax.legend(title='reliability')
    plt.setp(ax.get_legend().get_texts(), fontsize='25') # for legend text    
    plt.setp(ax.get_legend().get_title(), fontsize='25') # for legend title
plt.tight_layout()
###############################################################################
# Reliability part end
###################################################################################################################

###################################################################################################################
##### The Third Block: Regression analysis #####
################################################
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.formula.api import ols 
from statsmodels.formula.api import poisson

citations_bias_reg = citations_bias_factual[['bias_score_avg','new_topic','wk_project','factual']]#size is 3041283

citations_bias_reg_notnull = citations_bias_reg.dropna().reset_index()#604459
citations_bias_reg_notnull.drop(columns=['index'],inplace=True)
###############################################################################
# process the topic and wikiproject
#if one topic exist, we give it 1,if not, we give 0
def reg_topic(x):
    c = {'Geography':0,'Culture':0,'History_and_Society':0,'STEM':0}  
    t = eval(x)
    t0 = list(set([i.split('.')[0] for i in t[0]]))
    for i in t0:
        c[i]+=1
    l.append(list(c.values()))
    
l=[]
citations_bias_reg_notnull['new_topic'].progress_apply(lambda x:reg_topic(x))
r_topic = pd.DataFrame(l)
r_topic.columns = ['Geography','Culture','History_and_Society','STEM']
# citations_bias_reg_notnull = pd.concat([citations_bias_reg_notnull,r_topic])
citations_bias_reg_notnull['Geography']=r_topic['Geography'].to_list()
citations_bias_reg_notnull['Culture']=r_topic['Culture'].to_list()
citations_bias_reg_notnull['History_and_Society']=r_topic['History_and_Society'].to_list()
citations_bias_reg_notnull['STEM']=r_topic['STEM'].to_list()
###############################################################################
#only give 0 or 1 if the project exists
def reg_project(x):
    c = dict(zip(top10_project,[0]*10))
    c['Other']=0
    t = eval(x)
    t1 = list(set([i if i in top10_project else 'Other' for i in t]))
    for i in t1:
        c[i]+=1
    l.append(list(c.values()))

l=[]
citations_bias_reg_notnull['wk_project'].progress_apply(lambda x:reg_project(x))
r_project = pd.DataFrame(l)
r_project.columns = top10_project+['Other']
for i in top10_project+['Other']:
    citations_bias_reg_notnull[i]=r_project[i].to_list()
###############################################################################
# rename the columns
citations_bias_reg_notnull.columns = ['bias_score_avg', 'new_topic', 'wk_project', 'factual', 'Geography',
       'Culture', 'History_and_Society', 'STEM', 'Biography', 'Medicine',
       'Biography_science_and_academia_work_group', 'United_States',
       'Articles_for_creation', 'Politics', 'India', 'Pharmacology', 'Lists',
       'Military_history', 'Other']

model_ols = smf.ols(formula="bias_score_avg ~ C(factual, Treatment(reference='MOSTLY FACTUAL')) + Geography + Culture + History_and_Society + STEM + Biography + Medicine + Biography_science_and_academia_work_group + United_States + Articles_for_creation+ Politics + India + Pharmacology + Lists + Military_history + Other",data=citations_bias_reg_notnull)

res_ols = model_ols.fit()
print(res_ols.summary())
###############################################################################
##### The Third Block: Regression analysis end #####

# This is the end of analysis

