# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.results = []
        self.domains = ['bnwmovies.com']
        self.base_link = 'https://bnwmovies.com'
        self.search_link = '/?s=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['title']
            year = data['year']
            if int(year) > 1970:
                return self.results
            check_title = cleantitle.get(title)
            search_title = cleantitle.get_plus(title)
            search_link = self.base_link + self.search_link % search_title
            search_html = client.scrapePage(search_link).text
            results = client.parseDOM(search_html, 'div', attrs={'class': 'post'})
            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in results]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            page_link = [i[0] for i in result if check_title == cleantitle.get(i[1])][0]
            page_html = client.scrapePage(page_link).text
            links = client.parseDOM(page_html, 'source', ret='src')
            for link in links:
                valid, host = source_utils.is_host_valid(link, hostDict)
                quality, info = source_utils.get_release_quality(link, link)
                link += '|%s' % urlencode({'Referer': page_link})
                self.results.append({'source': host, 'quality': quality, 'url': link, 'info': info, 'direct': True})
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


