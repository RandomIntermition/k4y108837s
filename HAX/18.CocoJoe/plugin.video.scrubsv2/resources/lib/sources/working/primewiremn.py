# -*- coding: UTF-8 -*-

import re
import base64

from six import ensure_text
from six.moves.urllib_parse import parse_qs, urlparse, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['primewire.mn']
        self.base_link = 'https://primewire.mn'
        self.search_link = '/search-movies/%s.html'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
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
            if url is None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.get_plus(title)
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            query = '%s+season+%s' % (title, data['season']) if 'tvshowtitle' in data else title
            search_url = self.base_link + self.search_link % query
            html = client.scrapePage(search_url).text
            results = client.parseDOM(html, 'div', attrs={'class': 'ml-item'})
            results = [(client.parseDOM(i, 'a', ret='href'), re.findall('Tip\(\'<b><i>(.+?)</i></b>', i), re.findall('<b>Release:\s*(\d+)</b>', i)) for i in results]
            results = [(i[0][0], i[1][0], i[2][0]) for i in results if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in results if query == cleantitle.get_plus(i[1]) and year == i[2]][0]
            if 'tvshowtitle' in data:
                sepi = 'season-%1d/episode-%1d.html' % (int(data['season']), int(data['episode']))
                data = client.scrapePage(url).text
                link = client.parseDOM(data, 'a', ret='href')
                url = [i for i in link if sepi in i][0]
            r = client.scrapePage(url).text
            try:
                v = re.findall(r'document.write\(Base64.decode\("(.+?)"\)', r)[0]
                b64 = base64.b64decode(v)
                b64 = ensure_text(b64, errors='ignore')
                link = client.parseDOM(b64, 'iframe', ret='src')[0]
                link = link.replace('\/', '/')
                host = re.findall('([\w]+[.][\w]+)$', urlparse(link.strip().lower()).netloc)[0]
                host = client.replaceHTMLCodes(host)
                valid, host = source_utils.is_host_valid(host, hostDict)
                if valid:
                    self.results.append({'source': host, 'quality': 'SD', 'url': link, 'direct': False})
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
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        if any(x in url for x in self.domains):
            try:
                r = client.scrapePage(url).text
                try:
                    v = re.findall(r'document.write\(Base64.decode\("(.+?)"\)', r)[0]
                    b64 = base64.b64decode(v)
                    b64 = ensure_text(b64, errors='ignore')
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


