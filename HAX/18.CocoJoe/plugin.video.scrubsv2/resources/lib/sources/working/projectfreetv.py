# -*- coding: UTF-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.results = []
        self.domains = ['projectfreetv.stream']
        self.base_link = 'https://www.projectfreetv.stream'
        self.search_link = '/%s-%sx%02d'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle']
            season, episode = data['season'], data['episode']
            year = data['premiered'].split('-')[0]
            search_title = cleantitle.get_dash(title)
            url = self.base_link + self.search_link % (search_title, int(season), int(episode))
            html = client.scrapePage(url).text
            check_year = client.parseDOM(html, 'span', attrs={'class': 'airdateb'})[0]
            check_year = re.findall('(\d{4})', check_year)[0]
            if not year == check_year:
                return self.results
            links = client.parseDOM(html, 'tr')
            links = [(client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'a', ret='title')[0]) for i in links]
            for i in links:
                valid, host = source_utils.is_host_valid(i[1], hostDict)
                if host in str(self.results):
                    continue
                if valid:
                    link = self.base_link + i[0]
                    self.results.append({'source': host, 'quality': 'SD', 'url': link, 'direct': False})
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        try:
            if not url:
                return
            html = client.scrapePage(url).text
            item = client.parseDOM(html, 'a', attrs={'rel': 'external nofollow'}, ret='href')[0]
            link = client.scrapePage(item).url
            return link
        except:
            return #url


