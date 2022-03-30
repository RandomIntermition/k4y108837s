# -*- coding: UTF-8 -*-

import re
import base64

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['moviesonline.fm'] # moviesonline.mx  moviesonline.la  moviesonline.mn
        self.base_link = 'https://moviesonline.fm'
        self.search_link = '/search-movies/%s.html'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title)
            search_url = self.base_link + self.search_link % search_title
            search_html = client.scrapePage(search_url).text
            r = client.parseDOM(search_html, 'div', attrs={'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href')[0], re.findall('<i>(.+?)</i>', i)[0], re.findall('Release:\s*(\d+)', i)[0]) for i in r]
            try:
                url = [i[0] for i in r if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            except:
                url = [i[0] for i in r if check_title == cleantitle.get(i[1]+year) and year == i[2]][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except Exception:
            #log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['premiered'], url['season'], url['episode'] = premiered, season, episode
            search_term = url['tvshowtitle'] + ' season %d' % int(season)
            search_title = cleantitle.get_plus(search_term)
            check_title = cleantitle.get(search_term)
            year = url['premiered'].split('-')[0]
            search_url = self.base_link + self.search_link % search_title
            search_html = client.scrapePage(search_url).text
            r = client.parseDOM(search_html, 'div', attrs={'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href')[0], re.findall('<i>(.+?)</i>', i)[0], re.findall('Release:\s*(\d+)', i)[0]) for i in r]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            data = client.scrapePage(url).text
            data = client.parseDOM(data, 'div', attrs={'id': 'details'})
            data = zip(client.parseDOM(data, 'a'), client.parseDOM(data, 'a', ret='href'))
            url = [(i[0], i[1]) for i in data if i[0] == str(int(episode))]
            return url[0][1]
        except Exception:
            #log_utils.log('episode', 1)
            return



    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            r = client.scrapePage(url).text
            try:
                v = re.findall(r'document.write\(Base64.decode\("(.+?)"\)', r)[0]
                b64 = base64.b64decode(v)
                link = client.parseDOM(b64, 'iframe', ret='src')[0]
                link = link.replace('\/', '/')
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            except:
                #log_utils.log('sources', 1)
                pass
            try:
                r = client.parseDOM(r, 'div', {'class': 'server_line'})
                r = [(client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'p', attrs={'class': 'server_servername'})[0]) for i in r]
                if r:
                    for i in r:
                        host = re.sub('Server|Link\s*\d+', '', i[1]).lower()
                        host = client.replaceHTMLCodes(host)
                        if 'other' in host:
                            continue
                        if host in str(self.results):
                            continue
                        link = i[0].replace('\/', '/')
                        valid, host = source_utils.is_host_valid(host, hostDict)
                        if valid:
                            self.results.append({'source': host, 'quality': 'SD', 'url': link, 'direct': False})
            except:
                #log_utils.log('sources', 1)
                pass
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        if any(x in url for x in self.domains):
            try:
                r = client.scrapePage(url).text
                try:
                    v = re.findall(r'document.write\(Base64.decode\("(.+?)"\)', r)[0]
                    b64 = base64.b64decode(v)
                    try:
                        url = client.parseDOM(b64, 'iframe', ret='src')[0]
                    except:
                        url = client.parseDOM(b64, 'a', ret='href')[0]
                    url = url.replace('///', '//')
                except:
                    u = client.parseDOM(r, 'div', attrs={'class': 'player'})
                    url = client.parseDOM(u, 'a', ret='href')[0]
            except:
                #log_utils.log('resolve', 1)
                pass
            return url
        else:
            return url


