from audioop import reverse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from django.urls import reverse
from urllib.parse import quote


# done
def google(s):
    links = []
    text = []
    
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    headers = {"user-agent": USER_AGENT}
    r = requests.get("https://www.google.com/search?q=" + s, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    for g in soup.find_all('div', class_='nhaZ2c'):
    
        a = g.find('a')
        t = g.find('h3')
        fullurl=a.get("href")
        youtube_id = parse_qs(urlparse(fullurl).query).get('v', [None])[0]
        display_url = reverse('display_video', kwargs={'url': youtube_id})
        links.append(display_url)
        
        
        
       
        
        text.append(t.text)
    #return links, text
    for g in soup.find_all('div', class_='yuRUbf'):
    
        a = g.find('a')
        t = g.find('h3')
        furl=a.get("href")
        encoded_url = quote(furl, safe='')
        display_url = reverse('display_web', kwargs={'url': encoded_url})
        
                
        links.append(display_url)
        text.append(t.text)
    return links, text

