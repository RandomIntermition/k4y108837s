# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.

import re,urllib,urlparse,json
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import more_sources
from resources.lib.modules import proxy
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['swatchseries.to', 'watchseries.unblocker.cc']
        self.base_link = 'https://www1.swatchseries.to'
        self.search_link = 'https://www1.swatchseries.to/show/search-shows-json'
        self.search_link_2 = 'https://www1.swatchseries.to/search/%s'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            t = cleantitle.get(tvshowtitle)
            q = urllib.quote_plus(cleantitle.query(tvshowtitle))
            p = urllib.urlencode({'term': q})
            r = client.request(self.search_link, post=p, XHR=True)
            try:
                r = json.loads(r)
            except:
                r = None
            if r:
                r = [(i['seo_url'], i['value'], i['label']) for i in r if 'value' in i and 'label' in i and 'seo_url' in i]
            else:
                r = proxy.request(self.search_link_2 % q, 'tv shows')
                r = client.parseDOM(r, 'div', attrs = {'valign': '.+?'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), client.parseDOM(i, 'a')) for i in r]
                r = [(i[0][0], i[1][0], i[2][0]) for i in r if i[0] and i[1] and i[2]]
            r = [(i[0], i[1], re.findall('(\d{4})', i[2])) for i in r]
            r = [(i[0], i[1], i[2][-1]) for i in r if i[2]]
            r = [i for i in r if t == cleantitle.get(i[1]) and year == i[2]]
            url = r[0][0]
            url = proxy.parse(url)
            url = url.strip('/').split('/')[-1]
            url = url.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            url = '%s/serie/%s' % (self.base_link, url)
            r = proxy.request(url, 'tv shows')
            r = client.parseDOM(r, 'li', attrs = {'itemprop': 'episode'})
            t = cleantitle.get(title)
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs = {'itemprop': 'name'}), re.compile('(\d{4}-\d{2}-\d{2})').findall(i)) for i in r]
            r = [(i[0], i[1][0].split('&nbsp;')[-1], i[2]) for i in r if i[1]] + [(i[0], None, i[2]) for i in r if not i[1]]
            r = [(i[0], i[1], i[2][0]) for i in r if i[2]] + [(i[0], i[1], None) for i in r if not i[2]]
            r = [(i[0][0], i[1], i[2]) for i in r if i[0]]
            url = [i for i in r if t == cleantitle.get(i[1]) and premiered == i[2]][:1]
            if not url:
                url = [i for i in r if t == cleantitle.get(i[1])]
            if len(url) > 1 or not url:
                url = [i for i in r if premiered == i[2]]
            if len(url) > 1 or not url:
                raise Exception()
            url = url[0][0]
            url = proxy.parse(url)
            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostprDict + hostDict
            if url == None:
                return sources
            url = urlparse.urljoin(self.base_link, url)
            r = proxy.request(url, 'tv shows')
            links = client.parseDOM(r, 'a', ret='href', attrs = {'target': '.+?'})
            links = [x for y,x in enumerate(links) if x not in links[:y]]
            for i in links:
                try:
                    url = i
                    url = proxy.parse(url)
                    url = urlparse.parse_qs(urlparse.urlparse(url).query)['r'][0]
                    url = url.decode('base64')
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if source_utils.limit_hosts() is True and host in str(sources):
                        continue
                    host = host.encode('utf-8')
                    for source in more_sources.more_gomo(url, hostDict):
                        sources.append(source)
                    if valid:
                        sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


