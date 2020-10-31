# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

 # -Cleaned and Checked on 29-03-2019 by someone. # IGNORES

# Addon Name: Yoda
# Addon id: plugin.video.Yoda
# Addon Provider: Supremacy

import base64
import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy
from resources.lib.modules import control


class source:
        def __init__(self):
                self.priority = 1
                self.language = ['en']
                self.domains = ['sockshare.ac']
                self.base_link = 'http://sockshare.ac'
                self.search_link = '/search-movies/%s.html'

        def movie(self, imdb, title, localtitle, aliases, year):
                try:
                        q = cleantitle.geturl(title)
                        q2 = q.replace('-','+')
                        url = self.base_link + self.search_link % q2
                        r = client.request(url)
                        match = re.compile('<a class="title" href="(.+?)-'+q+'\.html"').findall(r)
                        for url in match:
                                url = '%s-%s.html' % (url,q)
                                return url
                except:
                        return
                        
        def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
                try:
                        url = cleantitle.geturl(tvshowtitle)
                        return url
                except:
                        return
 
        def episode(self, url, imdb, tvdb, title, premiered, season, episode):
                try:
                        if not url: return
                        
                        q = url + '-season-' + season
                        q2 = url.replace('-','+')
                        url = self.base_link + self.search_link % q2
                        r = client.request(url)
                        match = re.compile('<a class="title" href="(.+?)-'+q+'\.html"').findall(r)
                        for url in match:
                                url = '%s-%s.html' % (url,q)
                                r = client.request(url)
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
                        r = client.request(url)
                        try:
                                match = re.compile('<img src="http\://sockshare\.ac/themes/movies/img/icon/server/(.+?)\.png" width="16" height="16" /> <a href="(.+?)">Version ').findall(r)
                                for host, url in match:
                                        if host == 'internet': continue

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
                                        
                                        sources.append({
                                                'source': host,
                                                'quality': 'SD',
                                                'language': 'en',
                                                'url': url,
                                                'direct': False,
                                                'debridonly': False
                                                })
                        except:
                                return
                except Exception:
                        return
                return sources

        def resolve(self, url):
                r = client.request(url)
                match = re.compile('Base64\.decode\("(.+?)"').findall(r)
                for iframe in match:
                        iframe = base64.b64decode(iframe)
                        match = re.compile('src="(.+?)"').findall(iframe)
                        for url in match:
                                return url
