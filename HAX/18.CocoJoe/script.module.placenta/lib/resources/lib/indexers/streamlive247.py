# -*- coding: utf-8 -*-
# --[ Streamlive v1.0 ]--|--[ From JewBMX & Tempest ]--
# IPTV Indexer made just for the one site as of now.

import re, os, sys, urllib
from resources.lib.modules import client
from resources.lib.modules import control


class streamlive:
    def __init__(self):
        self.list = []
        self.base_link = 'https://www.streamlive.to/%s'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0', 'Referer': self.base_link}

    def root(self):
        channels = [
            ('-----24-7------', '', 'https://fonolo.com/wp-content/uploads/2016/03/A-Guide-to-247-Customer-Service.jpg'),
            ('Bleach', 'view/36820/Bleach-anime-full', 'https://upload.wikimedia.org/wikipedia/en/thumb/7/72/Bleachanime.png/220px-Bleachanime.png'),
            ('Detective Conan', 'view/38223/Detective-Conan-the-movies', 'https://vignette.wikia.nocookie.net/detectivconan/images/a/a2/Characters5.png/revision/latest?cb=20140428232345'),
            ('Dragon Ball', 'view/37044/Dragon-Ball', 'https://m.media-amazon.com/images/M/MV5BMjRlYTYyMDUtOGY5MC00MmFiLTljOTMtM2QzOWZjMWViN2FiL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_UY268_CR7,0,182,268_AL_.jpg'),
            ('Dragon Ball GT', 'view/53105/Dragon-Ball-GT', 'https://img.sharetv.com/shows/standard/dragon_ball_gt.jpg'),
            ('Dragon Ball Z', 'view/40156/Dragon-Balll-Z', 'https://m.media-amazon.com/images/M/MV5BMGMyOThiMGUtYmFmZi00YWM0LWJiM2QtZGMwM2Q2ODE4MzhhXkEyXkFqcGdeQXVyMjc2Nzg5OTQ@._V1_.jpg'),
            ('Friends', 'view/36673/Friends-show', 'https://www.shopyourtv.com/wp-content/uploads/2019/05/friends.jpg'),
            ('House MD', 'view/40783/House-MD', 'https://blog.cyrildason.com/wp-content/uploads/2016/11/House-MD.png'),
            ('King of Queens', 'view/38213/King-of-Queens', 'http://static.tvgcdn.net/feed/1/925/116356925.jpg'),
            ('Jackie Chan', 'view/37002/Jackie-Chan', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmYEhCqEtCQQoaydP_SyFekW2bcWuMM2TK66mxPilV5djQwS2b7Q'),
            ('Jackie Chan movies', 'view/36983/Jackie-Chan-movies', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmYEhCqEtCQQoaydP_SyFekW2bcWuMM2TK66mxPilV5djQwS2b7Q'),
            ('Naruto', 'view/37161/Naruto', 'https://a.wattpad.com/cover/100451910-288-k756864.jpg'),
            ('South Park', 'view/40155/South-Park', 'https://images2.minutemediacdn.com/image/upload/c_crop,h_358,w_640,x_0,y_49/f_auto,q_auto,w_1100/v1555003945/shape/mentalfloss/06804986093.png'),
            ('SuperHero movie channel', 'view/38366/SuperHero-movie-channel', 'https://qph.fs.quoracdn.net/main-qimg-24d02d403ce4a1947cac37f51003e620.webp'),
            ('That\'s 70 show', 'view/38217/That\'s-70-show', 'https://m.media-amazon.com/images/M/MV5BN2RkZGE0MjAtZGVkOS00MzVhLTg0OWItZTc4OGRjOTQ1ZTM4XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_.jpg'),
            ('The Office', 'view/40750/The-Office-(Show)', 'https://m.media-amazon.com/images/M/MV5BMTgzNjAzMDE0NF5BMl5BanBnXkFtZTcwNTEyMzM3OA@@._V1_.jpg')
        ]
        for channel in channels:
            self.list.append({'name': channel[0], 'url': self.base_link % channel[1], 'image': channel[2], 'action': 'streamlivePlay'})
        self.addDirectory(self.list)
        return self.list

    def play(self, url):
        try:
            stream = client.request(url, headers=self.headers)
            url = re.compile('href="(https://nl2.streamlive.to/vlc/?.+?)"').findall(stream)[0]
            control.execute('PlayMedia(%s)' % url)
        except Exception:
            return

    def addDirectory(self, items, queue=False, isFolder=True):
        if items is None or len(items) is 0:
            control.idle()
            sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()
        for i in items:
            try:
                name = i['name']
                if i['image'].startswith('http'):
                    thumb = i['image']
                elif artPath is not None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb
                item = control.item(label=name)
                if isFolder:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % urllib.quote_plus(i['url'])
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'false')
                else:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % i['url']
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'true')
                    item.setInfo("mediatype", "video")
                    item.setInfo("audio", '')
                item.setArt({'icon': thumb, 'thumb': thumb})
                if addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
            except Exception:
                pass
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
