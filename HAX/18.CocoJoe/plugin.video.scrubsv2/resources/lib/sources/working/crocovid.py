# -*- coding: utf-8 -*-

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['crocovid.com']
        self.base_link = 'https://crocovid.com'
        self.search_link = '/search/?type=title&query=%s'


# tt0371746
# Iron Man 2008
# Watch Iron Man 2008
# Watch seal team s05e03
# Watching SEAL Team S05E03

#movie year
#tvshow S00E00

# Might need more work to refine the results and search.


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
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            search_term = '%s %s' % (title, hdlr)
            check_term1 = cleantitle.get_plus('Watch %s' % search_term)
            check_term2 = cleantitle.get_plus('Watching %s' % search_term)
            search_url = self.base_link + self.search_link % cleantitle.get_plus(search_term)
            cookie = client.request(self.base_link, output='cookie')
            search_html = client.request(search_url, cookie=cookie)
            search_results = client.parseDOM(search_html, 'div', attrs={'class': 'search-row'})
            search_result = [(client.parseDOM(i, 'a', attrs={'class': 'videoLink'}, ret='href'), client.parseDOM(i, 'a', attrs={'class': 'videoLink'}, ret='title')) for i in search_results]
            search_result = [(i[0][0], i[1][0]) for i in search_result if len(i[0]) > 0 and len(i[1]) > 0]
            result_urls = [i[0] for i in search_result if check_term1 in cleantitle.get_plus(i[1]) or check_term2 in cleantitle.get_plus(i[1])]
            for result_url in result_urls:
                try:
                    result_url = self.base_link + result_url
                    link = client.request(result_url, cookie=cookie, output='geturl')
                    if not link or 'mcafee.com' in link: # might be different elsewhere, could try to filter out that dead host sooner.
                        continue
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
                except:
                    #log_utils.log('sources', 1)
                    pass
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


