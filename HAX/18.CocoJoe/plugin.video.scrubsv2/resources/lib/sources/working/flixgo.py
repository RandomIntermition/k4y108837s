# -*- coding: UTF-8 -*-

import re
import base64

from six import ensure_text

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['flixgo.me']
        self.base_link = 'https://flixgo.me'
        self.search_link = '/index.php?do=search'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            check_title = cleantitle.get_dash(title)
            search_url = self.base_link + self.search_link
            post = ('do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s' % (check_title))
            html = ensure_text(client.request(search_url, post=post), errors='replace')
            r = client.parseDOM(html, 'div', attrs={'class': 'film'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'img', ret='alt'), re.findall('-(\d{4})-', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get_dash(i[1]) and year == i[2]][0]
            url = self.base_link + url
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.scrapePage(url).text
            links = re.compile('arr\["btn-.+?"\] = "(.+?)";', re.DOTALL).findall(html)
            for link in links:
                b64 = base64.b64decode(link)
                b64 = ensure_text(b64, errors='replace')
                link = b64.split('&size')[0]
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


