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

file_name = r"E:\Project 2(Bias and reability on wiki and news)/news_google.txt" # this file contains all the urls which includes 'new.google'
# read the file
urls = []
for line in open(file_name,"r"): #
    urls.append(line.strip())

name=dict()
ip = []
for line in open("F:/1688/ip(3.14).txt","r",encoding='utf8'): #设置文件对象并读取每一行文件
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
    with open(r"E:\Project 2(Bias and reability on wiki and news)/googlenews_source.pkl",'ab') as f:
        pickle.dump(name,f)
    time.sleep(1)
    
count1 = 0
count2 = 0
for i in tqdm(urls[:20000]):
    header={
            'User-Agent': random.choice(ua)
            ,'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            ,'cookie': 'CONSENT=YES+TW.zh-CN+20160703-06-0; HSID=Af7CXxDBYqPMmKvbw; SSID=A-sr1yLdpMC34O7im; APISID=_lSxPlsWnNJQ6SOy/AiYxSaHhARFGSh2Ij; SAPISID=bqRIpyi2ufDaKpi5/AuCReqJuDM93SMdKy; __Secure-1PAPISID=bqRIpyi2ufDaKpi5/AuCReqJuDM93SMdKy; __Secure-3PAPISID=bqRIpyi2ufDaKpi5/AuCReqJuDM93SMdKy; SID=EQiV81LsUmfpDOQ0MDh_3mkUxpyj0HQk7yeSEKbvTNZhCDeuC_IBK7eJZzQs36RsvXSotw.; __Secure-1PSID=EQiV81LsUmfpDOQ0MDh_3mkUxpyj0HQk7yeSEKbvTNZhCDeu9ixdDCztX5VYZdLgwtrsGg.; __Secure-3PSID=EQiV81LsUmfpDOQ0MDh_3mkUxpyj0HQk7yeSEKbvTNZhCDeu9wK4VHSVsv5iQlFX7eHcSg.; OGPC=19010602-1:19015941-1:19008572-1:; 1P_JAR=2021-12-08-10; OGP=-19010602:-19015941:-19008572:; NID=511=Rmbk9RsgIpi1-2vWahaRr44h664mPck_XhBAz_7zh7ZSzoH8Wf_Lr2BWSRyVm3MxUmtJ_0DR7ffHoHqTsJgVQsd1EzjxVfvuf3KpDI8DN8g898JQGgunx1RPQM8RMnK3cSyQGBWDOCuZhmkQL78_FXr3bRwzhr1vBrVCvNqlWqDgUoBiEvrvWm0uThNDQc9GaKUCzAyWAt8; GOOGLE_ABUSE_EXEMPTION=ID=db33f79c2f4dfaf3:TM=1639045992:C=r:IP=24.132.64.125-:S=4b6RzAHnJ2YBHtUH3zrv02w; GN_PREF=W251bGwsIkNBSVNDd2lRdDhlTkJoRDQtZmhSIl0_; _ga=GA1.3.1751834713.1639046034; _gid=GA1.3.1476904321.1639046035; OTZ=6279034_52_52_123900_48_436380; SIDCC=AJi4QfHFqP6B8DU4TH-iXYSiwBXr0uNYO4idKWj5NBdrqFirCXtI7S3F7_Xld1ca-Gk0ejqEr1M; __Secure-3PSIDCC=AJi4QfGs_PPIvRjZbZhG0apW0JWbAGdWfKH2AmUNRjCeZEly8ZJo4V5rVdamFQ763-6UrfPilg'
            }
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
        header['cookie'] = 'CONSENT=YES+TW.zh-CN+20160703-06-0; HSID=Af7CXxDBYqPMmKvbw; SSID=A-sr1yLdpMC34O7im; APISID=_lSxPlsWnNJQ6SOy/AiYxSaHhARFGSh2Ij; SAPISID=bqRIpyi2ufDaKpi5/AuCReqJuDM93SMdKy; __Secure-1PAPISID=bqRIpyi2ufDaKpi5/AuCReqJuDM93SMdKy; __Secure-3PAPISID=bqRIpyi2ufDaKpi5/AuCReqJuDM93SMdKy; SID=EQiV81LsUmfpDOQ0MDh_3mkUxpyj0HQk7yeSEKbvTNZhCDeuC_IBK7eJZzQs36RsvXSotw.; __Secure-1PSID=EQiV81LsUmfpDOQ0MDh_3mkUxpyj0HQk7yeSEKbvTNZhCDeu9ixdDCztX5VYZdLgwtrsGg.; __Secure-3PSID=EQiV81LsUmfpDOQ0MDh_3mkUxpyj0HQk7yeSEKbvTNZhCDeu9wK4VHSVsv5iQlFX7eHcSg.; OGPC=19010602-1:19015941-1:19008572-1:; 1P_JAR=2021-12-08-10; OGP=-19010602:-19015941:-19008572:; NID=511=Rmbk9RsgIpi1-2vWahaRr44h664mPck_XhBAz_7zh7ZSzoH8Wf_Lr2BWSRyVm3MxUmtJ_0DR7ffHoHqTsJgVQsd1EzjxVfvuf3KpDI8DN8g898JQGgunx1RPQM8RMnK3cSyQGBWDOCuZhmkQL78_FXr3bRwzhr1vBrVCvNqlWqDgUoBiEvrvWm0uThNDQc9GaKUCzAyWAt8; GN_PREF=W251bGwsIkNBSVNDd2lRdDhlTkJoRDQtZmhSIl0_; _gid=GA1.3.1476904321.1639046035; _ga=GA1.3.1751834713.1639046034; OTZ=6279034_52_52_123900_48_436380; SIDCC=AJi4QfFl7bmpCbSru0_1Z7weh3aDI7lRGogyzJaDgqdt7Xm-ToISeKLM-Lk-BSQjR8O1PMyRMP0; __Secure-3PSIDCC=AJi4QfERMrXPEmiZ4vPPPEunIKdThhHZXTNRSiK7Q59sWSMHgo__kXcWHtR6KzZ77uWXBrzXDw'
        # input('update the cookie')
        count1 = 0
        count2 = 0
        
import pickle
with open(r"E:\Project 2(Bias and reability on wiki and news)/googlenews_source.pkl",'wb') as f:
    pickle.dump(name,f)
        
with open(r"E:\Project 2(Bias and reability on wiki and news)/googlenews_source.pkl",'rb') as f:
    googlenews_source = pickle.load(f)
#################################################################
