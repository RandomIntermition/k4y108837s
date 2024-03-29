# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import client
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import more_sources
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['cartoonhd.app']
        self.base_link = 'https://www.cartoonhd.app'
        self.search_link = '/?s=%s'
        self.scraper = cfscrape.create_scraper()


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            tvshowtitle = url
            url = self.base_link + '/episodes/%s-season-%s-episode-%s/?watching' % (tvshowtitle, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            hostDict = hostDict + hostprDict
            sourcePage = self.scraper.get(url).content
            links = re.compile('<iframe.+?src="(.+?)"', re.DOTALL).findall(sourcePage)
            for link in links:
                if "gomostream.com" in link:
                    for source in more_sources.more_gomo(link, hostDict):
                        sources.append(source)
                else:
                    quality, info = source_utils.get_release_quality(link, link)
                    valid, host = source_utils.is_host_valid(link, hostDict)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


