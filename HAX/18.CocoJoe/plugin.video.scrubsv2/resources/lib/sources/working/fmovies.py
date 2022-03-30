# -*- coding: UTF-8 -*-

import re

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['fmovies.vision', 'gostream.cool']
        self.base_link = 'https://fmovies.vision'
        self.search_link = '/index.php?do=search&filter=true'
        self.cookie = client.request(self.base_link, output='cookie')


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title)
            search_url = self.base_link + self.search_link
            post = ('do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s' % movie_title)
            html = client.request(search_url, post=post, cookie=self.cookie).replace('\n', '')
            r = client.parseDOM(html, 'div', attrs={'class': 'item'})
            r = [(client.parseDOM(i, 'a', attrs={'class': 'poster'}, ret='href'), client.parseDOM(i, 'img', ret='alt'), re.findall('<div class="meta">(\d{4}) <i class="dot">', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.request(url, cookie=self.cookie)
            try:
                links = client.parseDOM(html, 'div', ret='data-link')
                for link in links:
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
            except:
                #log_utils.log('sources', 1)
                pass
            try:
                result = re.compile('<script src="https://simplemovie.xyz/(.+?)" type').findall(html)[0]
                result_url = 'https://simplemovie.xyz/' + result
                result_html = client.request(result_url, cookie=self.cookie).replace("\\", "")
                links = re.compile('''<tr onclick="window\.open\( \\'(.+?)\\' \)">''').findall(result_html)
                for link in links:
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
            except:
                #log_utils.log('sources', 1)
                pass
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


