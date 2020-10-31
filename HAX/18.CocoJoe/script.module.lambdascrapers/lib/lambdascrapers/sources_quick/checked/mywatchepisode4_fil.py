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
            if url == None: return sources
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
            hostDict = hostprDict + hostDict
            r = client.request(url)
            r = re.compile('class="watch-button" data-actuallink="(.+?)"').findall(r)
            for url in r:
                if url in str(sources): continue
                valid, host = source_utils.is_host_valid(url, hostDict)

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
                if valid:
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
        except Exception:
            return
        return sources


    def resolve(self, url):
        return url

