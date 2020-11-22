# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.
# -Mod'D by Tempest

import re
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils
from resources.lib.modules import control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['watchepisodes4.com']
        self.base_link = 'https://www.watchepisodes4.com/'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(tvshowtitle)
            url = self.base_link + clean_title
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
            r = client.request(url)
            r = re.compile('<a title=".+? Season ' + season + ' Episode ' + episode + ' .+?" href="(.+?)">').findall(r)
            for url in r:
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
            if url == None: return sources
            hostDict = hostprDict + hostDict
            r = client.request(url)
            r = re.compile('class="watch-button" data-actuallink="(.+?)"').findall(r)
            for url in r:
                if url in str(sources): continue
                valid, host = source_utils.is_host_valid(url, hostDict)

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
                if valid:
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
        except Exception:
            return
        return sources


    def resolve(self, url):
        return url

