# -*- coding: UTF-8 -*-

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['main.dailyflix.stream', 'dailyflix.stream']
        self.base_link = 'https://main.dailyflix.stream'
        self.search_link = '/search/%s/feed/rss2/'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_link = self.base_link + self.search_link % imdb
            html = client.scrapePage(movie_link).text
            items = client.parseDOM(html, 'item')
            r = [(client.parseDOM(i, 'title'), client.parseDOM(i, 'link')) for i in items]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            url = [i[1] for i in r if cleantitle.get(title) == cleantitle.get(i[0])][0]
            return url
        except Exception:
            log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.scrapePage(url).text
            links = client.parseDOM(html, 'iframe', ret='src')
            for link in links:
                log_utils.log('Scraper dailyflix sources link: ' + repr(link))
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


