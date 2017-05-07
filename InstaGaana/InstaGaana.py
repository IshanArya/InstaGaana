#! /usr/bin/env python

from __future__ import print_function
from bs4 import BeautifulSoup
from sys import argv, platform, version_info
from random import randint
import requests
import json
import wget
import os
import eyed3
import eyed3.id3
import argparse
import re


if version_info > (3, 0):                           # Version Compatibility
    from urllib.parse import quote
    unicode = str
    raw_input = input

else:
    from urllib import quote
    import urllib3

# TODO:
"""
    Full album download
    Playlist download
"""


def extractdata(url, html_doc, meta_data_list):
    """
    :param url: Link of the song.
    :param html_doc: Webpage corresponding to url
    :param meta_data_list: Saves relevant information.
    """
    count = 0

    # Removes quotes from Title name.
    html_doc = re.sub(r'\(From .*?\)', "", html_doc.decode('utf-8'))
    # Visit https://github.com/LinuxSDA/InstaGaana/issues/2 for more info.

    soup = BeautifulSoup(html_doc, 'html.parser')

    song_list = map(str, soup.find_all("div", "hide song-json"))

    for x in song_list:
        count += 1
        try:
            song_info = json.loads(x[28:-6])
        except Exception as e:
            print("Unexpected Error: " + str(e) + "\nReport Bug.")
            continue

        meta_data = {}

        if url is None or url[22:] == song_info['perma_url'][22:]:
            meta_data['title'] = song_info['title']
            meta_data['singers'] = song_info['singers']
            meta_data['url'] = song_info['url']
            meta_data['album'] = song_info['album']
            meta_data['image_url'] = song_info['image_url']
            meta_data['duration'] = song_info['duration']
            meta_data['year'] = song_info['year']
            meta_data['perma_url'] = song_info['perma_url']
            meta_data['album_url'] = song_info['album_url']

            meta_data_list.append(meta_data)

            if url is not None or count == 5:
                break


def cookie_data():
    """
    :return: Corresponding pair of ATC and Cookies.
    """

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


def addtags(mp3_file, meta_data_list):
    """
    :param mp3_file: File name of song downloaded.
    :param meta_data_list: Contains meta datas.
    """

    path = ''                                                           # Location: Current Directory.

    if platform.startswith('win'):                                      # Location: C:\users\username\Music
        path = os.path.expanduser('~')+'\\Music\\'

    elif platform.startswith('linux'):                                  # Location: /home/username/Music
        path = os.path.expanduser('~') + '/Music/'

    filename = path + meta_data_list[0]['title'] + '.mp3'

    try:
        os.rename(mp3_file, filename)                                   # Rename to song name.
    except OSError:
        print("Replacing duplicate file...")                            # Windows' Crap.
        os.remove(filename)
        os.rename(mp3_file, filename)

    audiofile = eyed3.load(filename)
    audiofile.tag = eyed3.id3.Tag()
    audiofile.tag.file_info = eyed3.id3.FileInfo(unicode(filename))
    audiofile.tag.title = unicode(meta_data_list[0]['title'])
    audiofile.tag.artist = unicode(meta_data_list[0]['singers'])
    audiofile.tag.album = unicode(meta_data_list[0]['album'])
    audiofile.tag.recording_date = unicode(meta_data_list[0]['year'])
    artwork = requests.get(meta_data_list[0]['image_url'][:-11] + '500x500.jpg')        # High resolution link.

    audiofile.tag.images.set(3, artwork.content, "image/jpeg")
    audiofile.tag.save(version=(1, None, None))                                         # WMP Compatibility.
    audiofile.tag.save(version=(2, 3, 0))                                               # WMP Album Art Compatibility.
    audiofile.tag.save()


def downloadmusic(url, meta_data_list):
    """
    :param url: Either None or song url.
    :param meta_data_list: Either empty (if song url) or Contains meta data (of selected song through query).
    """

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

    if not meta_data_list:                          # Extract meta data of url provided.

        html_doc = None

        try:
            html_doc = requests.get(url=url, headers=headers)
        except Exception as e:
            print("Unexpected Error: " + str(e) + "\nCheck URL.")
            exit()

        extractdata(url, html_doc.content, meta_data_list)

        if meta_data_list[0] == {}:
            print("Can't extract meta data.")
            print("Make sure url " + url + " is complete and belongs to a song (not album) on saavn.com.")
            print("Otherwise, Report bug at LinuxSDA@gmail.com")
            exit()

    cookie, ra = cookie_data()

    data = [
          ('url', meta_data_list[0]['url']),
          ('ra', ra),
          ('__call', 'song.generateAuthToken'),
          ('_marker', 'false'),
          ('_format', 'json'),
          ('bitrate', '128'),
            ]

    response = requests.post('https://www.saavn.com/api.php', headers=headers, cookies=cookie, data=data)
    download_link = json.loads(response.content.decode('utf-8'))

    mp3_file = None

    if platform.startswith('win'):                              # Location: C:\users\username\Music
        path = os.path.expanduser('~')+'\\Music'

    elif platform.startswith('linux'):                          # Location: /home/username/Music
        path = os.path.expanduser('~') + '/Music'

    else:
        path = ''                                               # Location: Current Directory

    try:
        mp3_file = wget.download(download_link['auth_url'], path)
    except IOError:
        print("This track on Saavn is either disabled, greyed out, or not available.")
        exit()
    except Exception as e:
        print("Unexpected Error: " + str(e) + "\nTry Again or Report Bug.")
        exit()

    try:
        print("\n")
        addtags(mp3_file, meta_data_list)
    except TypeError:
        print("Can't add tags. EyeD3 version<0.8 is not compatible with Python3 or Report Bug?")


def fetchresult(query):
    """
    :param query: Query provided by user.
    :return: Meta data of song chosen in provided list.
    """

    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/57.0.2987.98 Safari/537.36',
    }

    meta_data_list = []
    url = "http://saavn.com/search/" + quote(query)
    page = None

    try:
        page = requests.get(url=url, headers=headers)
    except Exception as e:
        print("Unexpected Error: " + str(e) + "\nTry Later.")
        exit()

    print("..." * 25)
    extractdata(None, page.content, meta_data_list)

    for x in range(0, min(5, len(meta_data_list))):
        print(str(x+1) + ". ", end='')
        print(meta_data_list[x]['title'] + ", " + meta_data_list[x]['album'])
        print("   " + meta_data_list[x]['singers'] + ", " + meta_data_list[x]['year'])
        print("   " + str(int(int(meta_data_list[x]['duration']) / 60)) + "m ", end='')
        print(str(int(meta_data_list[x]['duration']) % 60) + "secs")
        print("..." * 25)

    choice = None

    try:
        choice = int(raw_input("Download result[1-5], 0 for none: "))
    except ValueError:
        print("Invalid response. Adios!")
        exit()

    if choice == 0:
        print("Adios!")
        exit()
    elif 0 < choice <= 5:
        return meta_data_list[choice-1:choice]
    else:
        print("Invalid response. Adios!")
        exit()


def main():

    if version_info < (3, 0):           # Disable InsecurePlatform and SNIMissing Warnings for python <2.7.9.
        urllib3.disable_warnings()      # Might work.

    parser = argparse.ArgumentParser(description="InstaGaana: Instant Music Downloader for Saavn.")

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-s', action="store", nargs='+', help="Name of song.")
    group.add_argument('-l', action="store", nargs=1, help="Song link.")

    if len(argv) == 1:
        parser.print_help()
        print("\nDeveloper: Sumit Dhingra, ", end='')
        print("https://github.com/LinuxSDA/")

    result = parser.parse_args()

    if result.s:
        query = ' '.join(result.s)
        meta_data_list = fetchresult(query)
        link = meta_data_list[0]['perma_url']
        downloadmusic(link, meta_data_list)

    elif result.l:
        downloadmusic(result.l[0], [])


if __name__ == '__main__':
    main()
