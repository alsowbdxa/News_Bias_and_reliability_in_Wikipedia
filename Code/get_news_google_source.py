#file_name = r"E:\Project 2(Bias and reability on wiki and news)/news_google.txt"
# to search the news source of news.google urls
#for news.google, we search it on the website and extract the news sources from it.
# an example can be found below
#https://news.google.com/newspapers?id=xaU9AAAAIBAJ&sjid=DykDAAAAIBAJ&pg=5655,5310963&dq=prince-william-of-baden&hl=en
#
import requests
from bs4 import BeautifulSoup
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

file_name = r"news_google.txt" # this file contains all the urls which includes 'new.google'
# read the file
urls = []
for line in open(file_name,"r"): #
    urls.append(line.strip())

name=dict()
ip = []
for line in open("F:/1688/ip(3.14).txt","r",encoding='utf8'): 
    ip.append(line.strip())


def get_name(i):
    if i in name:
        return
    proxy = {'http':random.choice(ip)}
    try:
        data = requests.get(i,headers=header,timeout=20,proxies=proxy).content.decode('utf8')
        d = BeautifulSoup(data,'html.parser')
    except:
        try:
            data = requests.get(i,headers=header,timeout=20).content.decode('utf8')
            d = BeautifulSoup(data,'html.parser')
        except:
            name[i] = ''
            return
    try:
        news_name = d.find('div',{'id':'volume_title'}).text.strip().split('\xa0')[0]
    except:
        try:
            news_name = d.find('div',{'id':'volume_title'}).find('a').get('href')
            news_name = news_name.split('nid=')[1].split('&')[0]
        except:
            news_name = ''
    name[i] = news_name
    with open(r"googlenews_source.pkl",'ab') as f:
        pickle.dump(name,f)
    time.sleep(1)
    
count1 = 0
count2 = 0
for i in tqdm(urls):
    header={
            'User-Agent': random.choice(ua)
            ,'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            ,'cookie': 'USE YOUR COOKIE'            }
    get_name(i)
    # if name[i]=='':
    #     get_name(i)
    if name[i]=='':
        count1 +=1
        count2 = 1
    else:
        count1 = 0
        count2 = 0
    if count1>10:
        header['cookie'] = ''
        count1 = 0
        count2 = 0
        
import pickle
with open(r"googlenews_source.pkl",'wb') as f:
    pickle.dump(name,f)
        
with open(r"googlenews_source.pkl",'rb') as f:
    googlenews_source = pickle.load(f)
#################################################################
