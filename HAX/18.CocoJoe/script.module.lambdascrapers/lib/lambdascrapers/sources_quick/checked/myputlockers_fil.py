# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.

import re,urlparse,urllib,base64
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import cache
from resources.lib.modules import source_utils
from resources.lib.modules import control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['putlockers.la','putlockers.mn','putlockers.tw']
        self.base_link = 'http://putlockers.la'
        self.search_link = '/search-movies/%s.html'
        # Spare  putlockers.tf


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title)
            search_url = urlparse.urljoin(self.base_link, self.search_link % clean_title.replace('-', '+'))
            r = cache.get(client.request, 1, search_url)
            r = client.parseDOM(r, 'div', {'id': 'movie-featured'})
            r = [(client.parseDOM(i, 'a', ret='href'), re.findall('.+?elease:\s*(\d{4})</', i), re.findall('<b><i>(.+?)</i>', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if (cleantitle.get(i[2][0]) == cleantitle.get(title) and i[1][0] == year)]
            url = r[0][0]
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['premiered'], url['season'], url['episode'] = premiered, season, episode
            try:
                clean_title = cleantitle.geturl(url['tvshowtitle']) + '-season-%d' % int(season)
                search_url = urlparse.urljoin(self.base_link, self.search_link % clean_title.replace('-', '+'))
                r = cache.get(client.request, 1, search_url)
                r = client.parseDOM(r, 'div', {'id': 'movie-featured'})
                r = [(client.parseDOM(i, 'a', ret='href'), re.findall('<b><i>(.+?)</i>', i)) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if cleantitle.get(i[1][0]) == cleantitle.get(clean_title)]
                url = r[0][0]
            except:
                pass
            data = client.request(url)
            data = client.parseDOM(data, 'div', attrs={'id': 'details'})
            data = zip(client.parseDOM(data, 'a'), client.parseDOM(data, 'a', ret='href'))
            url = [(i[0], i[1]) for i in data if i[0] == str(int(episode))]
            return url[0][1]
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            results_limit = 120
            openload_limit = 10
            mango_limit = 10
            verystream_limit = 18
            clipwatch_limit = 15
            entervideo_limit = 10
            megamp4_limit = 7
            streamplay_limit = 4
            vidcloud_limit = 4
            flix555_limit = 4
            vidzi_limit = 4
            streamcherry_limit = 4
            skyvids_limit = 4
            vev_limit = 4
            vshare_limit = 3
            flashx_limit = 0
            speedvid_limit = 3
            vidoza_limit = 3
            vidlox_limit = 3
            vidto_limit = 0
            vidup_limit = 3
            r = cache.get(client.request, 1, url)
            try:
                v = re.findall('document.write\(Base64.decode\("(.+?)"\)', r)[0]
                b64 = base64.b64decode(v)
                url = client.parseDOM(b64, 'iframe', ret='src')[0]
                try:
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if valid:
                        sources.append({ 'source': host, 'quality': 'SD', 'language': 'en', 'url': url.replace('\/', '/'), 'direct': False, 'debridonly': False })
                except:
                    pass
            except:
                pass
            r = client.parseDOM(r, 'div', {'class': 'server_line'})
            r = [(client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'p', attrs={'class': 'server_servername'})[0]) for i in r]
            if r:
                for i in r:
                    try:
                        host = re.sub('Server|Link\s*\d+', '', i[1]).lower()
                        url = i[0]
                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')
                        if 'other' in host:
                            continue

                        if control.setting('sources.dont.filter') == 'false':

                            if results_limit < 1: continue
                            else: results_limit -= 1

                            if 'thevideobee' in host: continue
                            if 'openload' in host:
                                if openload_limit < 1: continue
                                else: openload_limit -= 1
                            if 'mango' in host:
                                if mango_limit < 1: continue
                                else: mango_limit -= 1
                            if 'verystream' in host:
                                if verystream_limit < 1: continue
                                else: verystream_limit -= 1
                            if 'clipwatch' in host:
                                if clipwatch_limit < 1: continue
                                else: clipwatch_limit -= 1
                            if 'entervideo' in host:
                                if entervideo_limit < 1: continue
                                else: entervideo_limit -= 1
                            if 'megamp4' in host:
                                if megamp4_limit < 1: continue
                                else: megamp4_limit -= 1
                            if 'streamplay' in host:
                                if streamplay_limit < 1: continue
                                else: streamplay_limit -= 1
                            if 'vidcloud' in host:
                                if vidcloud_limit < 1: continue
                                else: vidcloud_limit -= 1
                            if 'flix555' in host:
                                if flix555_limit < 1: continue
                                else: flix555_limit -= 1
                            if 'vidzi' in host:
                                if vidzi_limit < 1: continue
                                else: vidzi_limit -= 1
                            if 'streamcherry' in host:
                                if streamcherry_limit < 1: continue
                                else: streamcherry_limit -= 1
                            if 'skyvids' in host:
                                if skyvids_limit < 1: continue
                                else: skyvids_limit -= 1
                            if 'vev' in host:
                                if vev_limit < 1: continue
                                else: vev_limit -= 1
                            if 'vshare' in host:
                                if vshare_limit < 1: continue
                                else: vshare_limit -= 1
                            if 'flashx' in host:
                                if flashx_limit < 1: continue
                                else: flashx_limit -= 1
                            if 'speedvid' in host:
                                if speedvid_limit < 1: continue
                                else: speedvid_limit -= 1
                            if 'vidoza' in host:
                                if vidoza_limit < 1: continue
                                else: vidoza_limit -= 1
                            if 'vidlox' in host:
                                if vidlox_limit < 1: continue
                                else: vidlox_limit -= 1
                            if 'vidto' in host:
                                if vidto_limit < 1: continue
                                else: vidto_limit -= 1
                            if 'vidup' in host:
                                if vidup_limit < 1: continue
                                else: vidup_limit -= 1
                        if source_utils.limit_hosts() is True and host in str(sources):
                            continue
                        valid, host = source_utils.is_host_valid(host, hostDict)
                        if valid:
                            sources.append({ 'source': host, 'quality': 'SD', 'language': 'en', 'url': url.replace('\/', '/'), 'direct': False, 'debridonly': False })
                    except:
                        pass
            return sources
        except:
            return sources


    def resolve(self, url):
        if self.base_link in url:
            url = client.request(url)
            v = re.findall('document.write\(Base64.decode\("(.+?)"\)', url)[0]
            b64 = base64.b64decode(v)
            url = client.parseDOM(b64, 'iframe', ret='src')[0]
        return url

