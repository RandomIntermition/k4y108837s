# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 02-11-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import client,cleantitle,source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['gomoviesclub.com']
        self.base_link = 'https://gomoviesclub.com'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + '/%s/' % title
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
            if not url: return
            tvshowtitle = url
            url = self.base_link + '/episode/%s-season-%s-episode-%s/' % (tvshowtitle,season,episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = client.request(url)
            try:
                match = re.compile('<iframe src="(.+?)"').findall(r)
                for url in match:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': 'HD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False}) 
            except:
                return
        except Exception:
            return
        return sources


    def resolve(self, url):
        return url
