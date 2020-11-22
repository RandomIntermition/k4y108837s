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
        self.domains = ['filmheaven.com']
        self.base_link = 'https://filmheaven.com'
        self.search_link = '/?s=%s'
        self.headers={'User-Agent': client.agent(), 'Referer': self.base_link}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
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
            hdlr = '%s (%s)' % (data['title'], int(data['year']))
            query = '%s+%s' % (data['title'], int(data['year']))

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)
            try:
                posts = requests.get(url, headers=self.headers).content
                r = [i for i in re.findall('<a href="(.+?)">(.+?)</a>', posts) if hdlr in i[1]]
                items += r
            except:
                pass

            for item in items:
                r = requests.get(item[0], headers=self.headers).content
                url = re.findall('src=\'(.+?)\'', r)
                for url in url:
                    if url.endswith('.xyz'): continue
                    if 'url=' in url:
                        url = url.split('url=')[1]
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append(
                            {'source': host, 'quality': '1080p', 'language': 'en', 'url': url,
                             'direct': False, 'debridonly': False})

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---FILMHEAVEN Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
