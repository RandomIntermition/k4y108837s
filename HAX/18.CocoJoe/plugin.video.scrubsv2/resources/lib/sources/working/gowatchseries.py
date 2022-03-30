# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['gowatchseries.online', 'gowatchseries.io', 'gowatchseries.co', 'gowatchseries.tv', 'gowatchseries.bz']
        self.base_link = 'https://www1.gowatchseries.online'
        self.search_link = '/search.html?keyword=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('tvshow', 1)
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
            #log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            check = '%s - Season %s' % (title, season) if 'tvshowtitle' in data else '%s (%s)' % (title, year)
            check1 = cleantitle.get_dash(check)
            search = '%s Season %s' % (title, season) if 'tvshowtitle' in data else title
            check2 = cleantitle.get_dash(search)
            search_url = self.base_link + self.search_link % cleantitle.get_utf8(search)
            r = client.scrapePage(search_url).text
            r = client.parseDOM(r, 'ul', attrs={'class': 'listing items'})[0]
            r = client.parseDOM(r, 'li')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'div', attrs={'class': 'name'})) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            try:
                url = [i[0] for i in r if check1 == cleantitle.get_dash(i[1])][0]
            except:
                url = [i[0] for i in r if check2 == cleantitle.get_dash(i[1])][0]
            vurl = self.base_link +'%s-episode-%s' % (url.replace('/info', ''), episode)
            r = client.scrapePage(vurl).text
            check_year = client.parseDOM(r, 'div', attrs={'class': 'right'})[0]
            check_year = re.findall('(\d{4})', check_year)[0]
            if not year == check_year:
                raise Exception()
            links = client.parseDOM(r, 'li', ret='data-video')
            for link in links:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


