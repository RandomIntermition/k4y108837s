# -*- coding: utf-8 -*-

import re
import sys

from six.moves.urllib_parse import urlparse, urlencode

from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils


class nightride:
    def __init__(self):
        self.list = []
        self.stations_link = 'https://nightride.fm/stations'
        self.streamsafe_link = 'https://streamsafe.nightride.fm'


    def streamsafe(self):
        try:
            html = client.scrapePage(self.streamsafe_link).text
            items = client.parseDOM(html, 'a', ret='href', attrs={'class': 'preview'})
            for item in items:
                title = re.findall('/.+?/.+?/(.+?)$', item)[0]
                label = '[B]%s[/B]' % title
                url =  self.streamsafe_link + item
                self.list.append({'title': label, 'url': url, 'image': 'DefaultAudio.png', 'action': 'music_play'})
            addDirectory(self.list)
            return self.list
        except:
            log_utils.log('streamsafe', 1)
            return self.list


    def stations(self):
        try:
            html = client.scrapePage(self.stations_link).text
            channels = re.findall('<a class="station" data-station=".+?" data-type="stream" href="(.+?)" title=".+?"><h3>(.+?)</h3><h4>(.+?)</h4></a>', html)
            for href, title, type in channels:
                label = '[B]%s[/B][CR][I]%s[/I]' % (title, type)
                station = re.findall('\?station=(.+?)$', href)[0]
                url = 'https://stream.nightride.fm/%s.m4a' % station
                self.list.append({'title': label, 'url': url, 'image': 'DefaultAudio.png', 'action': 'music_play'})
            addDirectory(self.list)
            return self.list
        except:
            log_utils.log('stations', 1)
            return self.list


def play(url):
    try:
        elements = urlparse(url)
        base = '%s://%s' % (elements.scheme, (elements.netloc or elements.path))
        url += '|%s' % urlencode({'Referer': base})
        control.execute('PlayMedia(%s)' % url)
    except:
        log_utils.log('play', 1)
        return


def addDirectory(items, queue=False, isFolder=True):
    if items == None or len(items) == 0:
        control.idle()
        sys.exit()
    sysaddon = sys.argv[0]
    syshandle = int(sys.argv[1])
    addonFanart = control.addonFanart()
    for i in items:
        try:
            url = '%s?action=%s&url=%s' % (sysaddon, i['action'], i['url'])
            title = i['title']
            thumb = i['image'] or 'DefaultAudio.png'
            item = control.item(label=title)
            item.setProperty('IsPlayable', 'true')
            item.setArt({'icon': thumb, 'thumb': thumb, 'fanart': addonFanart})
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
        except Exception:
            log_utils.log('addDirectory', 1)
            pass
    control.content(syshandle, 'addons')
    control.directory(syshandle, cacheToDisc=True)


