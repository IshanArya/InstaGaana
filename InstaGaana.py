from bs4 import BeautifulSoup
from sys import argv
from random import randint
import requests
import urllib3
import json
import wget
import os
import eyed3
import eyed3.id3
import argparse

# TODO:
"""
    Full album download
    Argv parameter not inserted try catch
    GUI
    Song search direct
    Python3 support
"""


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
            meta_data['image_url'] = song_info['image_url']
            break


def cookie_data():
    datadump = {'0': {'cookie': {'ATC': 'Njg2OTM1Mjc1'}, 'ra': '686893008'},
                '1': {'cookie': {'ATC': 'MTQyNTA1NDU1'}, 'ra': '142463188'},
                '2': {'cookie': {'ATC': 'OTg4NDgxOTUz'}, 'ra': '988439686'},
                '3': {'cookie': {'ATC': 'ODEyNDM2ODg0'}, 'ra': '812394617'},
                '4': {'cookie': {'ATC': 'MTk3MzgyOTcxMg=='}, 'ra': '1973787445'},
                '5': {'cookie': {'ATC': 'MTk1MzQ4NjgyMA=='}, 'ra': '1953444553'},
                '6': {'cookie': {'ATC': 'MTg0MzgwNzU4OA=='}, 'ra': '1843765321'},
                '7': {'cookie': {'ATC': 'MTk5NDEzNjAwOQ=='}, 'ra': '1994093742'},
                '8': {'cookie': {'ATC': 'MTMzMTEyMjUxMA=='}, 'ra': '1331080243'},
                '9': {'cookie': {'ATC': 'MTg2NDY2NTQ2Nw=='}, 'ra': '1864623200'},
                '10': {'cookie': {'ATC': 'MzE1NjMzMzY='}, 'ra': '31521069'},
                }

    num = str(randint(0, 10))
    return datadump[num]['cookie'], datadump[num]['ra']


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
    audiofile.tag.album = unicode(meta_data['album'])

    artwork = requests.get(meta_data['image_url'][:-11] + '500x500.jpg')

    audiofile.tag.images.set(3, artwork.content, "image/jpeg")
    audiofile.tag.save()


def downloadmusic(url):
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
    html_doc = None

    try:
        html_doc = requests.get(url=url, headers=headers)
    except Exception as e:
        print "Unexpected Error: " + str(e) + "\nCheck URL."
        exit()

    extractdata(url, html_doc, meta_data)

    if meta_data == {}:
        print "Can't extract meta data."
        print "Make sure url " + url + " is complete and belongs to a song (not album) on saavn.com."
        print "Otherwise, Report bug at LinuxSDA@gmail.com"

    else:
        cookie, ra = cookie_data()

        data = [
              ('url', meta_data['url']),
              ('ra', ra),
              ('__call', 'song.generateAuthToken'),
              ('_marker', 'false'),
              ('_format', 'json'),
              ('bitrate', '128'),
                ]

        response = requests.post('https://www.saavn.com/api.php', headers=headers, cookies=cookie, data=data)
        download_link = json.loads(response.content)
        mp3_file = wget.download(download_link['auth_url'])
        addtags(mp3_file, meta_data)


def main():
    urllib3.disable_warnings()

    parser = argparse.ArgumentParser(description="InstaGaana: Instant Music Downlaoder for Saavn.")

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-s', action="store", nargs='+', help="Name of song.")
    group.add_argument('-l', action="store", nargs=1, help="Song link.")

    if len(argv) == 1:
        parser.print_help()

    result = parser.parse_args()

    if result.s:
        print "Still in development. Use -l."
        # Show Result List and Find Link
        # downloadmusic(put link here)

    elif result.l:
        downloadmusic(result.l[0])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Process interrupted.")
exit()
