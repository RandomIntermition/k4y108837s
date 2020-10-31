# -*- coding: UTF-8 -*-
'''
    putlocker scraper for Exodus forks.
    Nov 9 2018 - Checked
    Oct 11 2018 - Cleaned and Checked

    Updated and refactored by someone.
    Originally created by others.
'''
import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['putlockerr.is','putlockers.movie'] 
        self.base_link = 'https://www6.putlockerr.is/'
        self.search_link = '/embed/%s/'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url + '/%s-%s/' % (season, episode)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = self.scraper.get(url).content
            try:
                match = re.compile('<iframe src="(.+?)://(.+?)/(.+?)"').findall(r)
                for http, host, url in match: 
                    url = '%s://%s/%s' % (http, host, url)
                    sources.append({'source': host,'quality': 'HD','language': 'en','url': url,'direct': False,'debridonly': False})
            except:
                return
        except Exception:
            return
        return sources

    def resolve(self, url):
        return url
