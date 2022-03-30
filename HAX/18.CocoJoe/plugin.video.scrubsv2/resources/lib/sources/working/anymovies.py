# -*- coding: utf-8 -*-

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['downloads-anymovies.co', 'downloads-anymovies.com']
        self.base_link = 'https://www.downloads-anymovies.co'
        self.search_link = '/search.php?zoom_query=%s+%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['title']
            year = data['year']
            check_title = 'Watch %s (%s) Full Movie Online Free' % (title, year)
            check_title = cleantitle.get(check_title)
            search_title = cleantitle.get_plus(title)
            search_link = self.base_link + self.search_link % (search_title, year)
            search_html = client.scrapePage(search_link).text
            results = client.parseDOM(search_html, 'div', attrs={'class': 'result_title'})
            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in results]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            page_link = [i[0] for i in result if check_title == cleantitle.get(i[1])][0]
            page_html = client.scrapePage(page_link).text
            links = client.parseDOM(page_html, 'a', attrs={'target': '_blank'}, ret='href')
            for link in links:
                if 'report-error.html' in link:
                    continue
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


