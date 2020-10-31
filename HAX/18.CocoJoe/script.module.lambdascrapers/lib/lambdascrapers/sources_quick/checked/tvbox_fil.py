# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.

import re, urllib, urlparse
from resources.lib.modules import client
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import dom_parser
from resources.lib.modules import source_utils
from resources.lib.modules import control

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['tvbox.ag']
        self.base_link = 'http://tvbox.ag'
        self.search_link = 'http://tvbox.ag/search?q=%s'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:            
            query = self.search_link % urllib.quote_plus(cleantitle.query(title))           
            for i in range(3):
                result = self.scraper.get(query).content
                if not result == None:
                    break
            t = [title] + [localtitle] + source_utils.aliases_to_array(aliases)
            t = [cleantitle.get(i) for i in set(t) if i]
            items = dom_parser.parse_dom(result, 'div', attrs={'class':'result'})
            url = None
            for i in items:
                result = re.findall(r'href="([^"]+)">(.*)<', i.content)
                if re.sub('<[^<]+?>', '', cleantitle.get(cleantitle.normalize(result[0][1]))) in t and year in result[0][1]:
                    url = result[0][0]
                if not url == None:
                    break
            url = url.encode('utf-8')
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            query = self.search_link % urllib.quote_plus(cleantitle.query(tvshowtitle))
            for i in range(3):
                result = self.scraper.get(query).content
                if not result == None:
                    break
            t = [tvshowtitle] + source_utils.aliases_to_array(aliases)
            t = [cleantitle.get(i) for i in set(t) if i]
            items = dom_parser.parse_dom(result, 'div', attrs={'class':'result'})
            url = None
            for i in items:
                result = re.findall(r'href="([^"]+)">(.*)<', i.content)
                if re.sub('<[^<]+?>', '', cleantitle.get(cleantitle.normalize(result[0][1]))) in t and year in result[0][1]:
                    url = result[0][0]
                if not url == None:
                    break
            url = url.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            url = urlparse.urljoin(self.base_link, url)
            for i in range(3):
                result = self.scraper.get(url).content
                if not result == None:
                    break
            title = cleantitle.get(title)
            premiered = re.compile('(\d{4})-(\d{2})-(\d{2})').findall(premiered)[0]
            premiered = '%s/%s/%s' % (premiered[2], premiered[1], premiered[0])
            result = re.findall(r'<h\d>Season\s+%s<\/h\d>(.*?<\/table>)' % season, result)[0]
            result = dom_parser.parse_dom(result, 'a', attrs={'href': re.compile('.*?episode-%s/' % episode)}, req='href')[0]
            url = result.attrs['href']
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            results_limit = 100
            openload_limit = 10
            mango_limit = 10
            verystream_limit = 20
            clipwatch_limit = 20
            streamplay_limit = 4
            vidcloud_limit = 4
            flix555_limit = 4
            vidzi_limit = 4
            streamcherry_limit = 4
            vev_limit = 4
            vshare_limit = 3
            flashx_limit = 3
            speedvid_limit = 3
            vidoza_limit = 3
            vidlox_limit = 3
            vidto_limit = 3
            vidup_limit = 3
            url = urlparse.urljoin(self.base_link, url)
            for i in range(3):
                result = self.scraper.get(url).content
                if not result == None:
                    break
            links = re.compile('onclick="report\(\'([^\']+)').findall(result)         
            for link in links:
                try:
                    valid, hoster = source_utils.is_host_valid(link, hostDict)
                    if not valid:
                        continue
                    urls, host, direct = source_utils.check_directstreams(link, hoster)

                    if control.setting('sources.dont.filter') == 'false':

                        if results_limit < 1: continue
                        else: results_limit -= 1
                        
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
                    for x in urls:
                        sources.append({'source': host, 'quality': x['quality'], 'language': 'en', 'url': x['url'], 'direct': direct, 'debridonly': False})
                except:
                    pass
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


