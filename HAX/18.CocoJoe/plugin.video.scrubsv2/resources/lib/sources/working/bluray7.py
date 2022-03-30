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
        self.domains = ['bluray7.com']
        self.base_link = 'https://bluray7.com'
        self.search_link = '/?s=%s'
        self.ajax_link = '/wp-admin/admin-ajax.php'
        self.session = requests.Session()
        self.cookie = client.request(self.base_link, output='cookie')


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_title = cleantitle.get_plus(title)
            check_term = '%s (%s)' % (title, year)
            check_title = cleantitle.get_plus(check_term)
            search_url = self.base_link + self.search_link % movie_title
            r = client.request(search_url, cookie=self.cookie)
            r = client.parseDOM(r, 'div', attrs={'class': 'result-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'img', ret='alt'), client.parseDOM(i, 'span', attrs={'class': 'year'})) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get_plus(i[1]) and year == i[2]][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.request(url, cookie=self.cookie)
            customheaders = {
                'Host': self.domains[0],
                'Accept': '*/*',
                'Origin': self.base_link,
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': client.UserAgent,
                'Referer': url,
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
                for source in scrape_sources.process(hostDict, p):
                    self.results.append(source)
            tbody = client.parseDOM(html, 'tbody')
            downloads = client.parseDOM(tbody, 'a', ret='href')
            for download in downloads:
                html = client.request(download, cookie=self.cookie)
                link = client.parseDOM(html, 'a', attrs={'id': 'link'}, ret='href')[0]
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


