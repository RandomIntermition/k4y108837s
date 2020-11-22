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
        self.domains = ['2embed.ru']
        self.base_link = 'https://www.2embed.ru'
        self.search_link = '/embed/imdb/movie?id=%s'
        self.search_link2 = '/embed/tmdb/tv?id=%s&s=%s&e=%s'
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
                urls = self.search_link2 % (data['tvdb'], data['season'], data['episode'])
            else:
                urls = self.search_link % urllib.quote_plus(data['imdb'])

            try:
                url = urlparse.urljoin(self.base_link, urls)
                posts = requests.get(url, headers=self.headers).content
                r = re.compile('data-id="(.+?)">.+?</a>').findall(posts)
                r = [i for i in r]
                items += r
            except:
                return

            for item in items:
                try:
                    item = 'https://www.2embed.ru/ajax/embed/play?id=%s&_token=' % item
                    url = requests.get(item, headers={'User-Agent': client.agent(), 'Referer': urls}).content
                    url = re.findall('"link":"(.+?)","sources"', url)
                    for url in url:
                        valid, host = source_utils.is_host_valid(url, hostDict)
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
