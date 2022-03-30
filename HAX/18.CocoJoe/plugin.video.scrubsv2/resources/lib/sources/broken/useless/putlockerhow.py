# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['putlocker.how', 'putlockerhd.co']
        self.base_link = 'https://putlocker.how'
        self.search_link = '/results?q=%s'


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
            check_term = '%s (%s)' % (title, year)
            check_title = cleantitle.get(check_term)
            search_title = cleantitle.get_plus(title)
            search_link = self.base_link + self.search_link % search_title
            search_html = client.scrapePage(search_link).text
            results = client.parseDOM(search_html, 'div', attrs={'class': 'thumb'})
            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in results]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            page_link = [i[0] for i in result if check_title in cleantitle.get(i[1])][0]
            page_link = self.base_link + page_link
            page_html = client.scrapePage(page_link).text
            page_links = re.compile('var frame_url = "(.+?)"', re.DOTALL|re.M).findall(page_html)
            for link in page_links:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


"""


Scraper Testing - putlockerhow sources link: '//vidlink.org/embed/5ac0f785914be6d66c8db9e8'
Scraper Testing - putlockerhow sources link: '//vidlink.org/embed/5b290643914be6d66c0f8bf7'
Scraper Testing - putlockerhow sources link: '//vidlink.org/embed/5ced78dbab249a0a952d3152'
Scraper Testing - putlockerhow sources link: '//vidlink.org/embed/5d0543e7b723f0536317b043'
Scraper Testing - putlockerhow sources link: '//vidlink.org/embed/5d32e09fb723f03e0a49a152'
Scraper Testing - putlockerhow sources link: '//vidlink.org/embed/5f04647dc352d083d9f5736e'
Scraper Testing - putlockerhow sources link: '//vidlink.org/embed/59eee43ef893828c34ca9eb7'
# links cant be processed properly due to cf problems.


"""


