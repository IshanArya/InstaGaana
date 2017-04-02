from bs4 import BeautifulSoup
from sys import argv
import requests
import urllib3
import json
import wget
import os
import eyed3
import eyed3.id3


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
            meta_data['album'] = song_info['album']
            meta_data['year'] = song_info['year']
            meta_data['image_url'] = song_info['image_url']
            break


def addtags(mp3_file, meta_data):
    """
    :param mp3_file: File name of song downloaded.
    :param meta_data: Contains meta data.
    """
    os.rename(mp3_file, meta_data['title'] + '.mp3')
    audiofile = eyed3.load(meta_data['title'] + '.mp3')
    audiofile.tag = eyed3.id3.Tag()
    audiofile.tag.file_info = eyed3.id3.FileInfo(unicode(meta_data['title']) + u'.mp3')
    audiofile.tag.title = unicode(meta_data['title'])
    audiofile.tag.artist = unicode(meta_data['singers'])
    # audiofile.tag.year = int(meta_data['year'])
    audiofile.tag.album = unicode(meta_data['album'])

    artwork = requests.get(meta_data['image_url'])

    audiofile.tag.images.set(3, artwork.content, "image/jpeg")
    audiofile.tag.save()


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
    cookies = {'ATC': 'Njg2OTM1Mjc1'}
    ra = '686893008'

    url = argv[1]
    html_doc = requests.get(url=url, headers=headers)

    extractdata(url, html_doc, meta_data)

    data = [
      ('url', meta_data['url']),
      ('ra', ra),
      ('__call', 'song.generateAuthToken'),
      ('_marker', 'false'),
      ('_format', 'json'),
      ('bitrate', '128'),
    ]

    response = requests.post('https://www.saavn.com/api.php', headers=headers, cookies=cookies, data=data)
    download_link = json.loads(response.content)
    mp3_file = wget.download(download_link['auth_url'])
    addtags(mp3_file, meta_data)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Process interrupted.")
exit()
