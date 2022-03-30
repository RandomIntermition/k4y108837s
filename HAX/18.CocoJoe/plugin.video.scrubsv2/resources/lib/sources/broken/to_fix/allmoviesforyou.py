# -*- coding: utf-8 -*-

import re

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['allmoviesforyou.net']
        self.base_link = 'https://allmoviesforyou.net'
        self.search_link = '/?s=%s'
        self.cookie = client.request(self.base_link, output='cookie')


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title)
            movie_link = self.base_link + self.search_link % movie_title
            r = client.request(movie_link, cookie=self.cookie)
            r = client.parseDOM(r, 'article', attrs={'class': 'TPost B'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'h2', attrs={'class': 'Title'}), client.parseDOM(i, 'span', attrs={'class': 'Qlty Yr'})) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            return url
        except Exception:
            log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshow_title = cleantitle.get_plus(tvshowtitle)
            check_title = cleantitle.get(tvshowtitle)
            tvshow_link = self.base_link + self.search_link % tvshow_title
            r = client.request(tvshow_link, cookie=self.cookie)
            r = client.parseDOM(r, 'article', attrs={'class': 'TPost B'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'h2', attrs={'class': 'Title'}), client.parseDOM(i, 'span', attrs={'class': 'Qlty Yr'})) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            return url
        except Exception:
            log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url[:-1]
            url = url.replace('/series/', '/episode/')
            url = url + '-%sx%s/' % (season, episode)
            return url
        except Exception:
            log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            page_html = client.request(url, cookie=self.cookie)
            results = client.parseDOM(page_html, 'iframe', ret='src')
            for result in results:
                if 'youtube.com' in result:
                    continue
                result = client.replaceHTMLCodes(result)
                log_utils.log('Scraper allmoviesforyou sources link1: ' + repr(result))
                result_html = client.request(result, cookie=self.cookie)
                links = client.parseDOM(result_html, 'iframe', ret='src')
                for link in links:
                    link = client.replaceHTMLCodes(link)
                    log_utils.log('Scraper allmoviesforyou sources link2: ' + repr(result))
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
            return self.results
        except Exception:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


