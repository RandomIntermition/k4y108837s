# -*- coding: utf-8 -*-
# Add Tv Later
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse, requests, base64
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import source_utils, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['movie2k.123movies.online']
        self.base_link = 'https://movie2k.123movies.online'
        self.search_link = '/?search=%s&movie=&x=0&y=0'
        self.search_link2 = '/?search=%s&tv=&x=0&y=0'
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
                urls = self.search_link2 % (data['tvshowtitle'], data['season'], data['episode'])
            else:
                urls = self.search_link % urllib.quote_plus(data['title'])
            try:
                url = urlparse.urljoin(self.base_link, urls)
                posts = requests.get(url, headers=self.headers).content
                url = re.findall('href="(.+?)"><img alt=".+?" title=".+?"', posts)[0]
                url = self.base_link + url + '-full'
                url = requests.get(url, headers={'User-Agent': client.agent(), 'Referer': urls}).content
                url = re.compile('class="" href="(.+?)"').findall(url)
                url = [i for i in url]
                items += url
            except:
                pass
            try:
                for url in items:
                    url = url.split('link=')[1].split('&host')[0]
                    url = base64.b64decode(url)
                    if 'voxzer' in url: continue
                    url = url.split('new&&&')[1].split('&&&link')[0]
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
            log_utils.log('---MOVIE2K Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        if 'jetload' in url:
            url = requests.get(url, headers=self.headers).content
            url = re.findall("var x_source = '(.+?)'", url)[0]
            return url
        else:
            return url
