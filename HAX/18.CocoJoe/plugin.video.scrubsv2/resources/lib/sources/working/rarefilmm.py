# -*- coding: UTF-8 -*-

import re

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['rarefilmm.com']
        self.base_link = 'https://rarefilmm.com'
        self.search_link = '/?s=%s+%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_plus(title)
            check_term = '%s (%s)' % (title, year)
            url = self.base_link + self.search_link % (title, year)
            searchPage = client.scrapePage(url).text
            section = client.parseDOM(searchPage, "h2", attrs={"class": "excerpt-title"})
            for item in section:
                results = re.compile('<a href="(.+?)">(.+?)</a>').findall(item)
                for url, checkit in results:
                    if cleantitle.get_plus(check_term) == cleantitle.get_plus(checkit):
                        return url
            return
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            sourcesPage = client.scrapePage(url).text
            resultsA = client.parseDOM(sourcesPage, 'iframe', ret='src')
            for link in resultsA:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            resultsB = re.compile('href="(.+?)"><strong>').findall(sourcesPage)
            for link in resultsB:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


