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
        self.domains = ['animeshow.tv']
        self.base_link = 'https://animeshow.tv'
        self.search_link = '/find.html?key=%s'
        self.episode_link = '/%s-episode-%s'
        self.tv_maze = tvmaze.tvMaze()


##  animeshow.tv
#https://www2.animeshow.tv/


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            #tvshowtitle = self.tv_maze.showLookup('thetvdb', tvdb)
            tvshowtitle = self.tv_maze.showLookup('imdb', imdb)
            tvshowtitle = tvshowtitle['name']
            t = cleantitle.get(tvshowtitle)
            q = self.base_link + self.search_link % tvshowtitle
            r = client.scrapePage(q).text
            match = re.compile('<div class="genres_result"><a href="(.+?)">', re.DOTALL).findall(r)
            for url in match:
                if t in cleantitle.get(url):
                    return url
            return
        except Exception:
            log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            #num = self.tv_maze.episodeAbsoluteNumber(tvdb, int(season), int(episode))
            num = self.tv_maze.episodeAbsoluteNumber(imdb, int(season), int(episode))
            url = [i for i in url.strip('/').split('/')][-1]
            url = self.episode_link % (url, num)
            return url
        except Exception:
            log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            try:
                vurl = self.base_link + url
                log_utils.log('Scraper Testing starting vurl: \n' + repr(vurl))
                html = client.scrapePage(vurl).text
                links = client.parseDOM(html, 'iframe', ret='src')
                for u in links:
                    if not 'http' in u:
                        continue
                    for source in scrape_sources.process(hostDict, u):
                        self.results.append(source)
            except:
                pass
            try:
                vurl2 = self.base_link + url + '-mirror-2/'
                log_utils.log('Scraper Testing starting vurl2: \n' + repr(vurl2))
                html2 = client.scrapePage(vurl2).text
                links2 = client.parseDOM(html2, 'iframe', ret='src')
                for u2 in links2:
                    if not 'http' in u2:
                        continue
                    for source in scrape_sources.process(hostDict, u2):
                        self.results.append(source)
            except:
                pass
            return self.results
        except Exception:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


