# -*- coding: UTF-8 -*-

import re

from six.moves.urllib_parse import quote_plus

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.results = []
        self.genre_filter = ['animation', 'anime']
        self.domains = ['gogoanime.video', 'gogoanime.vc', 'gogoanime.film']
        self.base_link = 'https://gogoanime.film'
        self.search_link = '/search.html?keyword=%s'
        self.episode_link = '/%s-episode-%s'
        self.tv_maze = tvmaze.tvMaze()


#self.domains = ['gogoanimes.tv', 'gogoanimes.to']
#self.base_link = 'https://gogoanimes.to'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowtitle = self.tv_maze.showLookup('imdb', imdb)
            tvshowtitle = tvshowtitle['name']
            t = cleantitle.get(tvshowtitle)
            q = self.base_link + self.search_link % quote_plus(tvshowtitle)
            r = client.scrapePage(q).text
            r = client.parseDOM(r, 'ul', attrs={'class': 'items'})
            r = client.parseDOM(r, 'li')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall('\d{4}', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][-1]) for i in r if i[0] and i[1] and i[2]]
            r = [i for i in r if t == cleantitle.get(i[1]) and year == i[2]]
            r = r[0][0]
            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except Exception:
            log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            num = self.tv_maze.episodeAbsoluteNumber(imdb, int(season), int(episode))
            url = [i for i in url.strip('/').split('/')][-1]
            url = self.base_link + self.episode_link % (url, num)
            return url
        except Exception:
            log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.scrapePage(url).text
            r = client.parseDOM(html, 'a', ret='data-video')
            for u in r:
                for source in scrape_sources.process(hostDict, u):
                    self.results.append(source)
            return self.results
        except Exception:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


