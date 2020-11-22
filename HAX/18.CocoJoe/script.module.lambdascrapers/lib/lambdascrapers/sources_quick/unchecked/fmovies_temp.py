# -*- coding: utf-8 -*-
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import source_utils, control
from resources.lib.sources import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['fmovies.132movies.online']
        self.base_link = 'https://fmovies.132movies.online'
        self.search_link = '/episodes/watch-video-%s-123movies-gostream/'

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

            if url is None:
                return sources

            hostDict = hostprDict + hostDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = '%s-episode-%d-season-%d' % (data['tvshowtitle'], int(data['episode']), int(data['season']))
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query).lower().replace('+', '-').replace('sg-1', 'sg1').replace('--', '-')
            url = urlparse.urljoin(self.base_link, url)

            r = cfscrape.get(url, headers={'User-Agent': client.agent()}).content

            r = re.findall('<iframe src="(.+?)" scrolling=no', r)
            for r in r:
                log_utils.log('---Testing - Exception: \n' + str(r))
                valid, hoster = source_utils.is_host_valid(r, hostDict)
                sources.append(
                    {'source': hoster, 'quality': 'SD', 'language': 'en', 'url': r, 'direct': False,
                     'debridonly': False})

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---FMOVIES.132MOVIES.ONLINE Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        try:
            url = client.request(url)
            url = re.findall('sources: \[\{file:"*(.+?)"\}\]', url)[0]
            url = url.replace('https://', 'http://')
            return url
        except:
            return url
