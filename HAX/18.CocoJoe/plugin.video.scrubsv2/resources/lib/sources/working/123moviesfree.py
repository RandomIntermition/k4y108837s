# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urljoin, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['123moviesfree.so', '123movie.movie']
        self.base_link = 'https://123moviesfree.so'
        self.search_link = '/movie/search/%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
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
            aliases = eval(data['aliases'])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            search = '%s Season %s' % (title, season) if 'tvshowtitle' in data else title
            url = urljoin(self.base_link, self.search_link % cleantitle.geturl(search))
            r = client.scrapePage(url).text
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            if 'tvshowtitle' in data:
                r = [(i[0], i[1], re.findall('(.*?)\s+-\s+Season\s+(\d)', i[1])) for i in r]
                r = [(i[0], i[1], i[2][0]) for i in r if len(i[2]) > 0]
                url = [i[0] for i in r if cleantitle.match_alias(i[2][0], aliases) and i[2][1] == season][0]
                url = urljoin(self.base_link, '%s/watching.html?ep=%s' % (url, episode))
            else:
                results = [(i[0], i[1], re.findall('\((\d{4})', i[1])) for i in r]
                try:
                    r = [(i[0], i[1], i[2][0]) for i in results if len(i[2]) > 0]
                    url = [i[0] for i in r if cleantitle.match_alias(i[1], aliases) and (year == i[2])][0]
                except:
                    url = [i[0] for i in results if cleantitle.match_alias(i[1], aliases)][0]
                url = urljoin(self.base_link, '%s/watching.html' % url)
            if url == None:
                raise Exception()
            r = client.scrapePage(url).text
            check_year = client.parseDOM(r, 'div', attrs={'class': 'mvici-right'})[0]
            check_year = re.findall('(\d{4})', check_year)[0]
            if not year == check_year:
                raise Exception()
            r = client.parseDOM(r, 'div', attrs={'class': 'les-content'})
            if 'tvshowtitle' in data:
                links = client.parseDOM(r, 'a', attrs={'episode-data': episode}, ret='player-data')
            else:
                links = client.parseDOM(r, 'a', ret='player-data')
            for link in links:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


