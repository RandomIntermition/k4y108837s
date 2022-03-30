# -*- coding: utf-8 -*-

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['123movies.unblockninja.com']
        self.base_link = 'https://123movies.unblockninja.com'
        self.search_link = '/search/?q=%s'


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
            title = data['title']
            imdb = data['imdb']
            movie_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title)
            movie_link = self.base_link + self.search_link % movie_title
            results = client.scrapePage(movie_link).text
            results = client.parseDOM(results, 'div', attrs={'class': 'ml-item'})
            results = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'h2')) for i in results]
            results = [(i[0][0], client.remove_codes(i[1][0])) for i in results if len(i[0]) > 0 and len(i[1]) > 0]
            result_url = [i[0] for i in results if check_title == cleantitle.get(i[1])][0]
            result_html = client.scrapePage(result_url).text
            if not imdb in result_html:
                raise Exception()
            content = client.parseDOM(result_html, 'div', attrs={'class': 'les-content'})
            links = client.parseDOM(content, 'a', ret='href')
            for link in links:
                if '123movie.su' in link:
                    continue
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


"""


Scraper Testing - 123moviesunblockninja sources link: 'https://www.2embed.ru/embed/imdb/movie?id=tt2274648'
Scraper Testing - 123moviesunblockninja sources link: 'https://www.2embed.ru/embed/imdb/movie?id=tt4154664'


"""

