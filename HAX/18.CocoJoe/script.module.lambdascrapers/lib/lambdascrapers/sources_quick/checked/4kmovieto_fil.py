# -*- coding: UTF-8 -*-

#  ..#######.########.#######.##....#..######..######.########....###...########.#######.########..######.
#  .##.....#.##.....#.##......###...#.##....#.##....#.##.....#...##.##..##.....#.##......##.....#.##....##
#  .##.....#.##.....#.##......####..#.##......##......##.....#..##...##.##.....#.##......##.....#.##......
#  .##.....#.########.######..##.##.#..######.##......########.##.....#.########.######..########..######.
#  .##.....#.##.......##......##..###.......#.##......##...##..########.##.......##......##...##........##
#  .##.....#.##.......##......##...##.##....#.##....#.##....##.##.....#.##.......##......##....##.##....##
#  ..#######.##.......#######.##....#..######..######.##.....#.##.....#.##.......#######.##.....#..######.

'''
    4kmovieto scraper for Exodus forks.
    Nov 9 2018 - Checked

    Updated and refactored by someone.
    Originally created by others.
'''
import re
import urllib
import urlparse

from openscrapers.modules import cfscrape
from openscrapers.modules import cleantitle
from openscrapers.modules import client
from openscrapers.modules import dom_parser
from openscrapers.modules import source_utils
from openscrapers.modules import control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['movie4k.org']
        self.base_link = 'https://movie4kto.org/'
        self.search_link = '/movies.php?list=search&search=%s'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search(imdb, [localtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and title != localtitle:
                url = self.__search(imdb, [title] + source_utils.aliases_to_array(aliases), year)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
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
        try:
            if not url:
                return sources

            url = urlparse.urljoin(self.base_link, url)

            r = self.scraper.get(url).content
            r = r.replace('\\"', '"')

            links = dom_parser.parse_dom(r, 'tr', attrs={'id': 'tablemoviesindex2'})

            for i in links:
                try:
                    host = dom_parser.parse_dom(i, 'img', req='alt')[0].attrs['alt']
                    host = host.split()[0].rsplit('.', 1)[0].strip().lower()
                    host = host.encode('utf-8')

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

                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if not valid: continue

                    url = dom_parser.parse_dom(i, 'a', req='href')[0].attrs['href']
                    url = client.replaceHTMLCodes(url)
                    url = urlparse.urljoin(self.base_link, url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False,
                                    'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            h = urlparse.urlparse(url.strip().lower()).netloc

            r = self.scraper.get(url).content
            r = r.rsplit('"underplayer"')[0].rsplit("'underplayer'")[0]

            u = re.findall('\'(.+?)\'', r) + re.findall('\"(.+?)\"', r)
            u = [client.replaceHTMLCodes(i) for i in u]
            u = [i for i in u if i.startswith('http') and not h in i]

            url = u[-1].encode('utf-8')
            return url
        except:
            return

    def __search(self, imdb, titles, year):
        try:
            q = self.search_link % urllib.quote_plus(cleantitle.query(titles[0]))
            q = urlparse.urljoin(self.base_link, q)

            t = [cleantitle.get(i) for i in set(titles) if i]
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = self.scraper.get(q).content

            r = dom_parser.parse_dom(r, 'tr', attrs={'id': re.compile('coverPreview.+?')})
            r = [(dom_parser.parse_dom(i, 'a', req='href'),
                  dom_parser.parse_dom(i, 'div', attrs={'style': re.compile('.+?')}),
                  dom_parser.parse_dom(i, 'img', req='src')) for i in r]
            r = [(i[0][0].attrs['href'].strip(), i[0][0].content.strip(), i[1], i[2]) for i in r if i[0] and i[2]]
            r = [(i[0], i[1], [x.content for x in i[2] if x.content.isdigit() and len(x.content) == 4], i[3]) for i in
                 r]
            r = [(i[0], i[1], i[2][0] if i[2] else '0', i[3]) for i in r]
            r = [i for i in r if any('us_flag' in x.attrs['src'] for x in i[3])]
            r = [(i[0], i[1], i[2], [re.findall('(\d+)', x.attrs['src']) for x in i[3] if 'smileys' in x.attrs['src']])
                 for i in r]
            r = [(i[0], i[1], i[2], [x[0] for x in i[3] if x]) for i in r]
            r = [(i[0], i[1], i[2], int(i[3][0]) if i[3] else 0) for i in r]
            r = sorted(r, key=lambda x: x[3])[::-1]
            r = [(i[0], i[1], i[2], re.findall('\((.+?)\)$', i[1])) for i in r]
            r = [(i[0], i[1], i[2]) for i in r if not i[3]]
            r = [i for i in r if i[2] in y]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year

            r = [(client.replaceHTMLCodes(i[0]), i[1], i[2]) for i in r]

            match = [i[0] for i in r if cleantitle.get(i[1]) in t and year == i[2]]

            match2 = [i[0] for i in r]
            match2 = [x for y, x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if match: url = match[0]; break
                    r = self.scraper.get.get(urlparse.urljoin(self.base_link, i)).content
                    r = re.findall('(tt\d+)', r)
                    if imdb in r: url = i; break
                except:
                    pass

            return source_utils.strip_domain(url)
        except:
            return

    def __get_base_url(self, fallback):
        try:
            for domain in self.domains:
                try:
                    url = 'http://%s' % domain
                    r = self.scraper.get(url, timeout='10').content
                    r = dom_parser.parse_dom(r, 'meta', attrs={'name': 'author'}, req='content')
                    if r and 'movie4k.to' in r[0].attrs.get('content').lower():
                        return url
                except:
                    pass
        except:
            pass

        return fallback
