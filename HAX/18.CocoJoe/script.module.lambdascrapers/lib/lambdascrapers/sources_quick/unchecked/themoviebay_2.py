# -*- coding: utf-8 -*-
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse, requests
import traceback
from resources.lib.modules import log_utils, jsunpack
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['vww.themoviebay.net']
        self.base_link = 'https://vww.themoviebay.net'
        self.search_link = '/search?q=%s'
        self.headers = {'User-Agent': client.agent(), 'Referer': self.base_link}

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

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            hdlr = '%s-%s' % (data['title'].lower().replace(': ', '-').replace('\'', '').replace(' ', '-').replace('.', ''), int(data['year']))
            query = '%s %s' % (data['title'], int(data['year']))

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url).replace('%3A+', '+')
            r = requests.get(url, headers=self.headers).content

            posts = client.parseDOM(r, 'div', attrs={'class': 'container'})

            for post in posts:
                try:
                    u = client.parseDOM(post, "li", attrs={"class": "grid-item"})
                    u = client.parseDOM(u, 'a', ret='href')
                    u = [i for i in u if hdlr in i]
                    items += u
                except:
                    pass

            for item in items:
                r = requests.get(item, headers=self.headers).content
                url = re.findall('src="(.+?)"></iframe>', r)[0]
                url = requests.get(url, headers=self.headers).content
                url = re.compile('(eval.*?\)\)\))').findall(url)[-1]
                url = jsunpack.unpack(url)
                url = re.findall('src:"(.+?)",', url)[0]
                sources.append(
                    {'source': 'CDN', 'quality': '720p', 'language': 'en', 'url': url,
                     'direct': True, 'debridonly': False})

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---LUNCHFLIX Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
