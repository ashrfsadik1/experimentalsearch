import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

# done
def google(s):
    links = []
    text = []
    youtubeides=[]
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    headers = {"user-agent": USER_AGENT}
    r = requests.get("https://www.google.com/search?q=" + s, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    for g in soup.find_all('div', class_='nhaZ2c'):
    
        a = g.find('a')
        t = g.find('h3')
        fullurl=a.get("href")
        links.append(a.get('href'))
        
        youtubeides.append( parse_qs(urlparse(fullurl).query).get('v'))
        
        text.append(t.text)
    #return links, text
    for g in soup.find_all('div', class_='yuRUbf'):
    #    for g in soup.select('div.nhaZ2c, div.yuRUbf'):
        a = g.find('a')
        t = g.find('h3')
       
        links.append(a.get('href'))
        text.append(t.text)
    return links, text

