# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 02-14-2019 by JewBMX in Scrubs.
# Created by Tempest

import re
from resources.lib.modules import client,cleantitle,source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['gomovies.ink']
        self.base_link = 'https://www.gomovies.ink'
        self.search_link = '/?s=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('-', '+')
            u = self.base_link + self.search_link % title
            u = client.request(u)
            i = client.parseDOM(u, "div", attrs={"class": "movies-list movies-list-full"})
            for r in i:
                r = re.compile('<a href="(.+?)"').findall(r)
                for url in r:
                    title = cleantitle.geturl(title)
                    if not title in url:
                        continue
                    return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostprDict + hostDict
            r = client.request(url)
            qual = re.compile('class="quality">(.+?)<').findall(r)
            for i in qual:
                if 'HD' in i:
                    quality = '720p'
                else:
                    quality = 'SD'
            r = client.parseDOM(r, "div", attrs={"id": "mv-info"})
            for i in r:
                t = re.compile('<a href="(.+?)"').findall(i)
                for url in t:
                    t = client.request(url)
                    t = client.parseDOM(t, "div", attrs={"id": "content-embed"})
                    for u in t:
                        i = re.findall('iframe src="(.+?)"', u)
                        for url in i:
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            if valid:
                                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                return sources
        except:
            return


    def resolve(self, url):
        return url

