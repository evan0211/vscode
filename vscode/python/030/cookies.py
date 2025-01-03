import requests
from bs4 import BeautifulSoup
url = 'https://www.ptt.cc/bbs/Gossiping/index.html'

headers = {
'cookie': 'over18=1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}
r = requests.get(url, headers=headers).content
soup = BeautifulSoup(r,'html.parser')
text_titles = soup.find_all('div', class_='title')

for title in text_titles:
    if title.a != None:
        print(title.a.string)