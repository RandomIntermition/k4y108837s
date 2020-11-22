# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['telepisodes.org']
        self.base_link = 'https://telepisodes.org'
        self.tvshow_link = '/tv-series/%s/season-%s/episode-%s/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0', 'Referer': self.base_link}


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = self.base_link + self.tvshow_link % (url, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            results_limit = 100
            verystream_limit = 18
            clipwatch_limit = 10
            entervideo_limit = 10
            megamp4_limit = 7
            vidcloud_limit = 4
            flix555_limit = 4
            vidzi_limit = 4
            skyvids_limit = 4
            vev_limit = 4
            vshare_limit = 3
            vidoza_limit = 3
            vidlox_limit = 3
            vidup_limit = 3
            videobee_limit = 3
            if url == None:
                return sources
            hostDict = hostprDict + hostDict
            page = client.request(url, headers=self.headers)
            match = re.compile('rel="nofollow ugc" title="(.+?)" target="_blank" href="(.+?)">', flags=re.DOTALL|re.IGNORECASE).findall(page)
            for hoster, url in match:
                url = self.base_link + url
                if url in str(sources): continue
                if control.setting('sources.dont.filter') == 'false':
                        
                        if results_limit < 1: continue
                        else: results_limit -= 1

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
                        if 'vidcloud' in host:
                            if vidcloud_limit < 1: continue
                            else: vidcloud_limit -= 1
                        if 'flix555' in host:
                            if flix555_limit < 1: continue
                            else: flix555_limit -= 1
                        if 'vidzi' in host:
                            if vidzi_limit < 1: continue
                            else: vidzi_limit -= 1
                        if 'skyvids' in host:
                            if skyvids_limit < 1: continue
                            else: skyvids_limit -= 1
                        if 'vev' in host:
                            if vev_limit < 1: continue
                            else: vev_limit -= 1
                        if 'vshare' in host:
                            if vshare_limit < 1: continue
                            else: vshare_limit -= 1
                        if 'vidoza' in host:
                            if vidoza_limit < 1: continue
                            else: vidoza_limit -= 1
                        if 'vidlox' in host:
                            if vidlox_limit < 1: continue
                            else: vidlox_limit -= 1
                        if 'vidup' in host:
                            if vidup_limit < 1: continue
                            else: vidup_limit -= 1
                        if 'videobee' in host:
                            if videobee_limit < 1: continue
                            else: videobee_limit -= 1
                valid, host = source_utils.is_host_valid(hoster, hostDict)
                if source_utils.limit_hosts() is True and host in str(sources):
                    continue
                if valid:
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            page2 = client.request(url, headers=self.headers)
            match2 = re.compile('href="/open/site/(.+?)"', flags=re.DOTALL|re.IGNORECASE).findall(page2)
            for link in match2:
                link = self.base_link + "/open/site/" + link
                link = client.request(link, timeout='10', output='geturl')
                return link
        except:
            return


