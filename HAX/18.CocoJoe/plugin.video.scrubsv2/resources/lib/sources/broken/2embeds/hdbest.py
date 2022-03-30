# -*- coding: utf-8 -*-

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['hdbest.net']
        self.base_link = 'https://hdbest.net'
        self.search_link = '/search/%s/feed/rss2/'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            search_url = self.base_link + self.search_link % data['imdb']
            search_html = client.scrapePage(search_url).text
            search_items = client.parseDOM(search_html, 'item')
            item_links = [client.parseDOM(i, 'link') for i in search_items]
            movie_link = [i[0] for i in item_links][0]
            result_html = client.scrapePage(movie_link).text
            result_links = client.parseDOM(result_html, 'iframe', ret='src')
            for link in result_links:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


"""


Scraper Testing - hdbest sources link: 'https://www.2embed.ru/embed/imdb/movie?id=tt0021814'
Scraper Testing - hdbest sources link: 'https://www.2embed.ru/embed/imdb/movie?id=tt0089218'
Scraper Testing - hdbest sources link: 'https://www.2embed.ru/embed/imdb/movie?id=tt0090555'
Scraper Testing - hdbest sources link: 'https://www.2embed.ru/embed/imdb/movie?id=tt1469304'
Scraper Testing - hdbest sources link: 'https://www.2embed.ru/embed/imdb/movie?id=tt1877830'
Scraper Testing - hdbest sources link: 'https://www.2embed.ru/embed/imdb/movie?id=tt2231461'
Scraper Testing - hdbest sources link: 'https://www.2embed.ru/embed/imdb/movie?id=tt2274648'
Scraper Testing - hdbest sources link: 'https://www.2embed.ru/embed/imdb/movie?id=tt3861390'
Scraper Testing - hdbest sources link: 'https://www.2embed.ru/embed/imdb/movie?id=tt4154664'


"""


