# -*- coding: UTF-8 -*-

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.results = []
        self.genre_filter = ['animation', 'anime']
        self.domains = ['animekisa.to', 'taganime.co']
        self.base_link = 'https://animekisa.to'
        self.search_link = '/search.html?keyword=%s'


##  taganime.co
#https://animekisa.to/
#https://animekisa.to/search?keyword=transformer





    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tv_maze = tvmaze.tvMaze()
            showtitle = tv_maze.showLookup('thetvdb', tvdb)
            url = showtitle['name']
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if not url:
            return
        try:
            tv_maze = tvmaze.tvMaze()
            num = tv_maze.episodeAbsoluteNumber(tvdb, int(season), int(episode))
            url = self.base_link + self.show_link % (url, num)
            return url
        except:
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            url = url.replace(' ','-')
            html = client.request(url)
            match = client.parseDOM(html, 'source', ret='src')
            for url in match:
                for source in scrape_sources.process(hostDict, url):
                    self.results.append(source)
            return self.results
        except Exception:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


