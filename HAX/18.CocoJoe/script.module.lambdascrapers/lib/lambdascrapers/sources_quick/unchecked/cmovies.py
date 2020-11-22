# -*- coding: utf-8 -*-
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse, requests
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import source_utils, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['cmovies.is']
        self.base_link = 'https://cmovies.is'
        self.search_link = '/film/%s/watching.html?ep=0'
        self.search_link2 = '/film/%s-season-%s/watching.html?ep=%s'
        self.headers={'User-Agent': client.agent(), 'Referer': self.base_link}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            items = []

            if url is None:
                return sources

            hostDict = hostprDict + hostDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            if 'tvdb' in data:
                urls = self.search_link2 % (data['tvshowtitle'].replace('.',''), data['season'], data['episode'])
            else:
                urls = self.search_link % urllib.quote_plus(data['title'].replace('.',''))
            try:
                url = urlparse.urljoin(self.base_link, urls).replace('%3A-', '-').replace('\'', '').replace(' ', '-').replace('+', '-')
                posts = requests.get(url, headers=self.headers).content
                url = re.findall('player-data="(.+?)"', posts)[0]
                if url.startswith('//'):
                    r = 'https:' + url
                url = requests.get(r, headers={'User-Agent': client.agent(), 'Referer': urls}).content
                url = re.findall('data-video="(.+?)">.+?</li>', url)
                for url in url:
                    if url.startswith('//'):
                        url = 'https:' + url
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append(
                            {'source': host, 'quality': 'SD', 'language': 'en', 'url': url,
                             'direct': False, 'debridonly': False})
            except:
                pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---2EMBED Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url