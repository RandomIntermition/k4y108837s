# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.

import re,base64
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils
from resources.lib.modules import control

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['putlockertv.ws']
        self.base_link = 'http://putlockertv.ws'
        self.search_link = '/search-movies/%s.html'
        self.scraper = cfscrape.create_scraper()
        # Old 0123putlocker.com  Now craptcha


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            url = url.replace('-','+')
            return url
        except:
            return
 
 
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            query = url + '+season+' + season
            find = query.replace('+','-')
            url = self.base_link + self.search_link % query
            r = self.scraper.get(url).content
            match = re.compile('<a href="http://putlockertv.ws/watch/(.+?)-' + find + '.html"').findall(r)
            for url_id in match:
                url = 'http://putlockertv.ws/watch/' + url_id + '-' + find + '.html'
                r = self.scraper.get(url).content
                match = re.compile('<a class="episode episode_series_link" href="(.+?)">' + episode + '</a>').findall(r)
                for url in match:
                    return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
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
            videobee_limit = 3
            if url == None:
                return sources
            r = self.scraper.get(url).content
            match = re.compile('<p class="server_version"><img src="http://putlockertv.ws/themes/movies/img/icon/server/(.+?).png" width="16" height="16" /> <a href="(.+?)">').findall(r)
            for host, url in match:
                if host == 'internet':
                    pass
                if url in str(sources): continue
                
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
                    if 'videobee' in host:
                        if videobee_limit < 1: continue
                        else: videobee_limit -= 1
                if source_utils.limit_hosts() is True and host in str(sources):
                    continue
                valid, host = source_utils.is_host_valid(host, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False}) 
            return sources
        except Exception:
            return sources


    def resolve(self, url):
        r = self.scraper.get(url).content
        match = re.compile('decode\("(.+?)"').findall(r)
        for info in match:
            info = base64.b64decode(info)
            match = re.compile('src="(.+?)"').findall(info)
            for url in match:
                return url


