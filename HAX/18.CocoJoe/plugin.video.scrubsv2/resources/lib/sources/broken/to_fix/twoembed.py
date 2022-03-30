# -*- coding: utf-8 -*-
#**First Created by Tempest**

import re
import requests

from six import ensure_text
from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['2embed.ru']
        self.base_link = 'https://www.2embed.ru'
        self.ajax_link = '/ajax/embed/play?id=%s&_token=%s'
        self.session = requests.Session()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            if 'tvshowtitle' in data:
                search_url = self.base_link + '/embed/tmdb/tv?id=%s&s=%s&e=%s' % (data['tvdb'], data['season'], data['episode'])
            else:
                search_url = self.base_link + '/embed/imdb/movie?id=%s' % data['imdb']
            log_utils.log('Scraper Testing starting url: \n' + repr(search_url))
            search_html =  self.session.get(search_url).text
            token = re.findall('"token":"(.+?)","si"', search_html)[0]
            log_utils.log('Scraper Testing sources token: \n' + repr(token))
            results = client.parseDOM(search_html, 'a', ret='data-id')
            for result in results:
                try:
                    item_url = self.base_link + self.ajax_link % (result, token)
                    item_html = self.session.get(item_url).text
                    #item_html = ensure_text(item_html.content, errors='replace')
                    log_utils.log('Scraper Testing sources item_url: \n' + repr(item_url))
                    log_utils.log('Scraper Testing sources item_html: \n' + repr(item_html))
                    #links = re.findall('"link":"(.+?)","sources"', item_html)
                    #for link in links:
                        #log_utils.log('Scraper Testing sources link: \n' + repr(link))
                        #for source in scrape_sources.process(hostDict, link):
                            #self.results.append(source)
                except:
                    log_utils.log('sources', 1)
                    pass
            return self.results
        except:
            log_utils.log('sources', 1)
            return self.results


#https://www.2embed.ru/embed/imdb/movie?id=tt2274648

#<a class="dropdown-item item-server" href="javascript:;" data-id="1614554">Server Vidcloud</a>
#<a class="dropdown-item item-server" href="javascript:;" data-id="6135010">Server Streamlare</a>
#<a class="dropdown-item item-server" href="javascript:;" data-id="1056786">Server Upstream</a>
#<a class="dropdown-item item-server" href="javascript:;" data-id="2192009">Server Hydrax</a>

#https://www.2embed.ru/ajax/embed/play?id=1614554&_token=



    def resolve(self, url):
        return url


