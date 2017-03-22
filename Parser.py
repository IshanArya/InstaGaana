from bs4 import BeautifulSoup
import requests
import urllib3
import json

urllib3.disable_warnings()

headers = {
    'Pragma': 'no-cache',
    'Origin': 'http://www.saavn.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
}

url = 'http://www.saavn.com/s/song/hindi/Ghazal-Legend-Farida-Khanum/Aaj-Jane-Ki-Zid-Na-Kaaro/ISYnSxZ0c3g'
html_doc = requests.get(url=url, headers=headers)
soup = BeautifulSoup(html_doc.content, 'html.parser')

meta_data = {'title': None, 'singers': None, 'url': None, 'image_url': None}

song_list = map(str, soup.find_all("div", "hide song-json"))

for x in song_list:
    song_info = json.loads(x[28:-6])
    if url[22:] == song_info['perma_url'][22:]:
        meta_data['title'] = song_info['title']
        meta_data['singers'] = song_info['singers']
        meta_data['url'] = song_info['url']
        meta_data['image_url'] = song_info['image_url']
        break

print meta_data
