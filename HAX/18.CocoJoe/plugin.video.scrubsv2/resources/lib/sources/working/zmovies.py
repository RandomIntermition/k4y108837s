# -*- coding: UTF-8 -*-

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['zmovies.cc']
        self.base_link = 'https://zmovies.cc'
        self.search_link = '/search/%s/feed/rss2/'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title)
            search_url = self.base_link + self.search_link % search_title
            r = client.scrapePage(search_url).text
            r = client.parseDOM(r, 'item')
            r = [(client.parseDOM(i, 'link'), client.parseDOM(i, 'title'), client.parseDOM(i, 'pubDate')) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1]) and year in i[2]][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.scrapePage(url).text
            body = client.parseDOM(html, 'div', attrs={'class': 'tags_right'})[0]
            links = client.parseDOM(body, 'a', attrs={'rel': 'nofollow'}, ret='href')
            for link in links:
                if link == '/server1.html':
                    continue
                if any(i in link for i in ['openload.co', 'streamango.com']):
                    continue
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


