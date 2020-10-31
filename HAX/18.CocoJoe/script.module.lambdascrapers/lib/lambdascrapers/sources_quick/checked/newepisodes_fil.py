# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.

import re,requests
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['newepisodes.co']
        self.base_link = 'https://newepisodes.co'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0', 'Referer': self.base_link}
        self.session = requests.Session()
        self.tm_user = control.setting('tm.user')


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvShowTitle = cleantitle.geturl(tvshowtitle)
            tmdburl = 'https://api.themoviedb.org/3/find/%s?external_source=tvdb_id&language=en-US&api_key=%s' % (tvdb, self.tm_user)
            tmdbresult = self.session.get(tmdburl, headers=self.headers).content
            tmdb_id = re.compile('"id":(.+?),',re.DOTALL).findall(tmdbresult)[0]
            url = '/watch-' + tvShowTitle + '-online-free/' + tmdb_id
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            episodeTitle = cleantitle.geturl(title)
            url = self.base_link + url + '/season-' + season + '-episode-' + episode + '-' + episodeTitle
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
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
            if url == None:
                return sources
            url = url.replace(' ','-')
            r = self.session.get(url, headers=self.headers).content
            match = re.compile('<li class="playlist_entry " id="(.+?)"><a><div class="list_number">.+?</div>(.+?)<span>></span></a></li>',re.DOTALL).findall(r)
            for id, host in match:
                url = self.base_link + '/embed/' + id
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
                valid, host = source_utils.is_host_valid(host, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            r = self.session.get(url, headers=self.headers).content
            url = re.compile('<iframe.+?src="(.+?)"').findall(r)[0]
            return url
        except:
            return url



