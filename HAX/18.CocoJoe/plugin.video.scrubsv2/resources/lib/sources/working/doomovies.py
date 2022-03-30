# -*- coding: utf-8 -*-

import re
import requests

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['doomovies.ga']
        self.base_link = 'https://doomovies.ga'
        self.search_link = '/?s=%s'
        self.ajax_link = '/wp-admin/admin-ajax.php'
        self.session = requests.Session()


# a source found and unused to maybe look into.
#<li id="player-option-3" class="dooplay_player_option pp" data-post="pp" data-type=movie data-nume="pp" data-pp="https://doomovies.ga/wp-content/themes/dooplay/play_video.php?video_id=UlYydmJHM2gxMndONmc9PQ==&tmdb=0&season=0&episode=0">
#https://doomovies.ga/wp-content/themes/dooplay/play_video.php?video_id=UlYydmJHM2gxMndONmc9PQ==&tmdb=0&season=0&episode=0
# redirects to...
#https://2embedplayer.net/?token=TnJ5N0IrRmR5MU1kS0lRRnVsc2hOMG92NER6d2tWb3hhajRTeDcwdEZTcVkrNWhtWDA4RlpNd3hSelVyMzB4aWhRbWVCTXpVMmkyZ1Z5QUp6blUzOUNuMHdUbz0=


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['title']
            year = data['year']
            search_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title)
            search_url = self.base_link + self.search_link % search_title
            html = client.scrapePage(search_url).text
            results = client.parseDOM(html, 'div', attrs={'class': 'result-item'})
            results = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'img', ret='alt'), client.parseDOM(i, 'span', attrs={'class': 'year'})) for i in results]
            results = [(i[0][0], i[1][0], i[2][0]) for i in results if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            result_url = [i[0] for i in results if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            html = client.scrapePage(result_url).text
            customheaders = {
                'Host': self.domains[0],
                'Accept': '*/*',
                'Origin': self.base_link,
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': client.UserAgent,
                'Referer': result_url,
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            post_link = self.base_link + self.ajax_link
            results = re.compile("data-type='(.+?)' data-post='(.+?)' data-nume='(\d+)'>", re.DOTALL).findall(html)
            for data_type, data_post, data_nume in results:
                payload = {'action': 'doo_player_ajax', 'post': data_post, 'nume': data_nume, 'type': data_type}
                r = self.session.post(post_link, headers=customheaders, data=payload)
                i = r.json()
                if not i['type'] == 'iframe':
                    continue
                p = i['embed_url'].replace('\\', '')
                if 'imdb.com' in p:
                    continue
                for source in scrape_sources.process(hostDict, p):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


