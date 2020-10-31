# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 05-06-2019 by JewBMX in Scrubs.
# Mix of Tempest and Other.

import re
from resources.lib.modules import client,cleantitle,source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123movies4u.ch', '123movies4u.me']
        self.base_link = 'https://123movies4u.cz'
        self.movie_link = '/movie/%s'
        self.tv_link = '/show/%s/season/%s/episode/%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + self.movie_link % title
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = self.base_link + self.tv_link % (url,season,episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []
        if url == None: return sources
        if 'movie' in url: quality = '720p'
        if 'show' in url: quality = 'SD'
        try:
            r = client.request(url)
            try:
                match = re.compile('<IFRAME style="z-index:9999;WIDTH:100%; " SRC="(.+?)://(.+?)/(.+?)"').findall(r)
                for http,host,url in match:
                    if 'vidoza' in host: continue
                    if 'vidzi' in host: continue
                    if 'vidlox' in host: continue
                    if 'streamplay' in host: continue
                    url = '%s://%s/%s' % (http,host,url)
                    if url in str(sources): continue
                    host = host.replace('www.','')
                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False}) 
                match2 = re.compile('onclick="window.open\("(.+?)://(.+?)/(.+?)"\)').findall(r)
                for http,host,url in match2:
                    if 'vidoza' in host: continue
                    if 'vidzi' in host: continue
                    if 'vidlox' in host: continue
                    if 'streamplay' in host: continue
                    url = '%s://%s/%s' % (http,host,url)
                    if url in str(sources): continue
                    host = host.replace('www.','')
                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False}) 
            except:
                return
        except Exception:
            return
        except Exception:
            return
        return sources


    def resolve(self, url):
        return url

