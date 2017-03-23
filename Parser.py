from bs4 import BeautifulSoup
import requests
import urllib3
import json


def extractdata(url, html_doc, meta_data):
    """
    :param url: Link of the song.
    :param html_doc: Webpage corresponding to url
    :param meta_data: Saves relevant information.
    """
    soup = BeautifulSoup(html_doc.content, 'html.parser')

    song_list = map(str, soup.find_all("div", "hide song-json"))

    for x in song_list:
        song_info = json.loads(x[28:-6])
        if url[22:] == song_info['perma_url'][22:]:
            meta_data['title'] = song_info['title']
            meta_data['singers'] = song_info['singers']
            meta_data['url'] = song_info['url']
            meta_data['image_url'] = song_info['image_url']
            break


def getcookies(html_doc, cookies):
    """
    :param html_doc: Webpage containing cookies
    :param cookies: Saves relevant cookies
    """
    cookies['ATC'] = html_doc.cookies['ATC']
    cookies['CT'] = html_doc.cookies['CT']
    cookies['B'] = html_doc.cookies['B']


def main():
    urllib3.disable_warnings()

    headers = {
        'Pragma': 'no-cache',
        'Origin': 'http://www.saavn.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/57.0.2987.98 Safari/537.36',
    }

    meta_data = {}
    cookies = {}

    url = 'http://www.saavn.com/s/song/hindi/Ghazal-Legend-Farida-Khanum/Aaj-Jane-Ki-Zid-Na-Kaaro/ISYnSxZ0c3g'
    html_doc = requests.get(url=url, headers=headers)

    extractdata(url, html_doc, meta_data)
    getcookies(html_doc, cookies)

    data = [
      ('url', meta_data['url']),
      ('ra', '432295852'),
      ('__call', 'song.generateAuthToken'),
      ('_marker', 'false'),
      ('_format', 'json'),
      ('bitrate', '128'),
    ]

    response = requests.post('https://www.saavn.com/api.php', headers=headers, cookies=cookies, data=data)
    download_link = json.loads(response.content)
    print download_link  # ['auth_url']


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Process interrupted.")
