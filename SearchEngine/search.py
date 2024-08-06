from audioop import reverse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from django.urls import reverse
from urllib.parse import quote
import re

# done





def google(s):
    links = []
    text = []
    images = []  # لإضافة الصور
    searchtxt=s  
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    headers = {"user-agent": USER_AGENT}
    r = requests.get("https://www.google.com/search?q=" + s, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    
    # استخلاص فيديوهات اليوتيوب
    for g in soup.find_all('div', class_='nhaZ2c'):
        a = g.find('a')
        t = g.find('h3')
        fullurl = a.get("href")
        youtube_id = parse_qs(urlparse(fullurl).query).get('v', [None])[0]
        thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/hqdefault.jpg"
        display_url = reverse('display_video', kwargs={'url': youtube_id,'searchtxt':searchtxt})
        
        links.append(display_url)
        text.append(t.text)
       
        images.append(thumbnail_url)    
            
    
    # استخلاص مواقع الإنترنت
    for g in soup.find_all('div', class_='yuRUbf'):
        a = g.find('a')
        t = g.find('h3')
        furl = a.get("href")
        encoded_url = quote(furl, safe='')
        display_url = reverse('display_web', kwargs={'url': encoded_url,'searchtxt':searchtxt})
        
        links.append(display_url)
        text.append(t.text)
        
        # للحصول على صورة للموقع (يحتاج إلى خدمة خارجية)
        site_thumbnail_url = f"https://api.page2images.com/directlink?p2i_url={encoded_url}&p2i_key=bf036f37d1181016"
        images.append(site_thumbnail_url)
    
    return links, text, images

# ملاحظة: تأكد من استبدال `YOUR_API_KEY` بمفتاح API الخاص بك لخدمة التقاط الصور من صفحة الويب.

    # Somethime request.code == 500
def yahoo(s):
    links = []
    text = []
    url = "https://search.yahoo.com/search?q=" + s + "&n=" + str(10)
    raw_page = requests.get(url)
    print(raw_page)
    soup = BeautifulSoup(raw_page.text, "html.parser")
    #for link in soup.find_all(attrs={"class": "ac-algo fz-l ac-21th lh-24"}):
    for link in soup.find_all(attrs={"class": "dd fst algo algo-sr relsrch richALgo"}):    
        links.append(link.get('href'))
        text.append(link.text)
    return links, text


# done

def duck(s):
    links = []
    text = []
    images=[]
    searchtxt=s
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    headers = {'user-agent': userAgent}
    r = requests.get('https://duckduckgo.com/html/?q=' + s, headers=headers)
    s = BeautifulSoup(r.content, "html.parser")
    
    for i in s.find_all('div', attrs={'class': 'results_links_deep'}):
        a = i.find('a', attrs={'class': 'result__a'})
        fullurl=a.get('href')
        # تعبير منتظم للتحقق من أن URL يخص يوتيوب
        youtube_pattern = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+'
       )
        if youtube_pattern.match(fullurl):
             youtube_id = parse_qs(urlparse(fullurl).query).get('v', [None])[0]
             thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/hqdefault.jpg"
             display_url = reverse('display_video', kwargs={'url': youtube_id,'searchtxt':searchtxt})
             
             images.append(thumbnail_url) 
             
             links.append(display_url)
        else:
             encoded_url = quote(fullurl, safe='')
             #display_url = reverse('display_web', kwargs={'url': encoded_url,'searchtxt':searchtxt})    
             #display_url="{% url 'display\display_web' url="+ encoded_url+" searchtxt="+searchtxt +"%}"
             display_url = reverse('display_web', kwargs={'url': encoded_url, 'searchtxt': searchtxt})
             links.append(display_url)
             # للحصول على صورة للموقع (يحتاج إلى خدمة خارجية)
             site_thumbnail_url = f"https://api.page2images.com/directlink?p2i_url={encoded_url}&p2i_key=bf036f37d1181016"
             images.append(site_thumbnail_url)
        #links.append(a.get('href'))
        text.append(a.text)
  #  if len(links) > 0:
   #      links.pop(0)
    #     text.pop(0)
    return links, text,images


# # done
def ecosia(s):
    links = []
    text = []
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    headers = {'user-agent': userAgent}
    r = requests.get('https://www.ecosia.org/search?q=' + s, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    #for i in soup.find_all("h2", attrs={'class': 'result-firstline-title'}):
    for i in soup.find_all("h2", attrs={'class': 'result__body'}):
        #a = i.find("a", attrs={'class': 'result__title'})
        a = i.find("a", attrs={'class': 'js-result-title'})
        text.append(a.text)
        links.append(a.get('href'))
    return links, text

def bing(search):
    userAgent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36')
    headers = {'user-agent' : userAgent}
    URL = ('https://www.bing.com/search?q='+search)
    request = requests.get(URL, headers=headers)

    soup = BeautifulSoup(request.content, "html.parser")
    results = []
    texts = []
    images=[]
    searchtxt=search
    
    for i in soup.find_all('li', {'class' : 'b_algo'}):
        link = i.find_all('a')
        link_text = i.find('a')
        links = link[0]['href']
        fullurl=links
        # تعبير منتظم للتحقق من أن URL يخص يوتيوب
        youtube_pattern = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+'
       )
        if youtube_pattern.match(fullurl):
             youtube_id = parse_qs(urlparse(fullurl).query).get('v', [None])[0]
             thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/hqdefault.jpg"
             display_url = reverse('display_video', kwargs={'url': youtube_id,'searchtxt':searchtxt})
             
             images.append(thumbnail_url) 
             
             results.append(display_url)
        else:
             encoded_url = quote(fullurl, safe='')
             #display_url = reverse('display_web', kwargs={'url': encoded_url,'searchtxt':searchtxt})    
             #display_url="{% url 'display\display_web' url="+ encoded_url+" searchtxt="+searchtxt +"%}"
             display_url = reverse('display_web', kwargs={'url': encoded_url, 'searchtxt': searchtxt})
             results.append(display_url)
             # للحصول على صورة للموقع (يحتاج إلى خدمة خارجية)
             site_thumbnail_url = f"https://api.page2images.com/directlink?p2i_url={encoded_url}&p2i_key=bf036f37d1181016"
             images.append(site_thumbnail_url)
        

        #results.append(links)
        texts.append(link_text.text)

    return(results, texts,images)

def givewater(search):
    userAgent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36')
    URL = ('https://search.givewater.com/serp?q='+search)
    headers = {'user-agent' : userAgent}
    request = requests.get(URL, headers=headers)
    
    soup = BeautifulSoup(request.content, 'html.parser')
    results = []
    texts = []

    for i in soup.find_all('div', {'class' : 'web-bing__result'}):
        link = i.find_all('a')
        link_text = i.find('a')
        links = link[0]['href']
        results.append(links)
        texts.append(link_text.text)
    
    return(results, texts)
