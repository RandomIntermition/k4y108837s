# -*- coding: UTF-8 -*-

from six import ensure_text

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['flenix.plus']
        self.base_link = 'https://flenix.plus'
        self.search_link = '/index.php?do=search&filter=true'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            check_title = cleantitle.get_dash(title)
            search_url = self.base_link + self.search_link
            post = ('do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s' % (imdb))
            html = ensure_text(client.request(search_url, post=post), errors='replace')
            posts = client.parseDOM(html, 'div', attrs={'class': 'post'})
            post = [(client.parseDOM(i, 'div', attrs={'class': 'title'})) for i in posts]
            urls = [(client.parseDOM(i, 'a', ret='href')) for i in post]
            url = [i[0] for i in urls][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.scrapePage(url).text
            links = client.parseDOM(html, 'iframe', ret='src')
            for link in links:
                if any(i in link for i in ['123files.club', 'api.hdv.fun', 'consistent.stream', 'dbgo.fun']):
                    continue
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


