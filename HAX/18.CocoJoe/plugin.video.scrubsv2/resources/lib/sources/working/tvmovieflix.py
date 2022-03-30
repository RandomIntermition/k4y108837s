# -*- coding: utf-8 -*-

import re
import requests

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['tvmovieflix.com']
        self.base_link = 'https://tvmovieflix.com'
        self.search_link = '/search/%s/feed/rss2/'
        self.ajax_link = '/wp-admin/admin-ajax.php'
        self.session = requests.Session()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('tvshow', 1)
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
            #log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = data['year']
            search_title = cleantitle.get_plus(title)
            check_title = cleantitle.get_plus(title)
            check_type = '/tvshows/' if 'tvshowtitle' in data else '/movies/'
            search_url = self.base_link + self.search_link % search_title
            search_html = client.scrapePage(search_url).text
            results = client.parseDOM(search_html, 'item')
            result = [(client.parseDOM(i, 'link')[0], client.parseDOM(i, 'title')[0]) for i in results]
            result_url = [i[0] for i in result if check_title == cleantitle.get_plus(i[1]) and check_type in i[0]][0]
            if 'tvshowtitle' in data:
                season, episode = data['season'], data['episode']
                check = '-%sx%s' % (season, episode)
                show_html = client.scrapePage(result_url).text
                results = client.parseDOM(show_html, 'div', attrs={'class': 'episodiotitle'})
                results = [(client.parseDOM(i, 'a', ret='href')) for i in results]
                result_url = [i[0] for i in results if check in i[0]][0]
            html = client.scrapePage(result_url).text
            results = re.compile("class='dooplay_player_option' data-type='(.+?)' data-post='(.+?)' data-nume='(.+?)'>", re.DOTALL).findall(html)
            for data_type, data_post, data_nume in results:
                customheaders = {
                    'Host': self.domains[0],
                    'Accept': '*/*',
                    'Origin': self.base_link,
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': client.UserAgent,
                    'Referer': result_url,
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9'
                }
                post_link = self.base_link + self.ajax_link
                payload = {'action': 'doo_player_ajax', 'post': data_post, 'nume': data_nume, 'type': data_type}
                r = self.session.post(post_link, headers=customheaders, data=payload).json()
                p = r['embed_url']
                if 'imdbembed.xyz' in p:
                    for source in self.imdbembed(p, hostDict):
                        self.results.append(source)
                if any(x in p for x in self.domains):
                    try:
                        page_html = client.scrapePage(p).text
                        links = client.parseDOM(page_html, 'source', ret='src')
                        for link in links:
                            valid, host = source_utils.is_host_valid(link, hostDict)
                            quality, info = source_utils.get_release_quality(link, link)
                            link += '|%s' % urlencode({'Referer': p})
                            self.results.append({'source': host, 'quality': quality, 'url': link, 'info': info, 'direct': True})
                    except:
                        pass
                else:
                    for source in scrape_sources.process(hostDict, p):
                        self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


    def imdbembed(self, link, hostDict):
        sources = []
        try:
            type, pattern = re.findall('/(movie|tv)/(?:[A-Za-z0-9]+)/([A-Za-z0-9-]+)', link)[0]
            base = 'https://imdbembed.xyz/%s/%s/%s' % (type, '%s', pattern)
            if pattern.startswith('tt'):
                mirrors = ['imdb', 'imdb2', 'imdb3', 'imdb4', 'imdb5']
            else:
                mirrors = ['tmdb', 'tmdb2', 'tmdb3', 'tmdb4', 'tmdb5']
            for i in mirrors:
                try:
                    item_link = base % i
                    html = client.scrapePage(item_link).text
                    urls = client.parseDOM(html, 'iframe', ret='src')
                    for url in urls:
                        if any(i in url for i in ['vidsrc.me', 'firesonic.sc']):
                            continue
                        url = re.findall('javascript:window\.location\.replace\(\"(.+?)\"\)', url)[0]
                        for source in scrape_sources.process(hostDict, url):
                            sources.append(source)
                except:
                    pass
            return sources
        except:
            #log_utils.log('imdbembed', 1)
            return sources


