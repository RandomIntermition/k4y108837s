# -*- coding: utf-8 -*-
# Universal Debrid
# checked 12/6/2019

import re
import urllib
import xbmc, xbmcaddon, time
from universaldebrid.common import clean_title, clean_search, send_log, error_log
from universaldebrid.scraper import Scraper
from universaldebrid.modules import client

dev_log = xbmcaddon.Addon('script.module.universaldebrid').getSetting("dev_log")            


class zooqle(Scraper):
    domains = ['https://zooqle.com/']
    name = "Zooqle"
    sources = []

    def __init__(self):
        self.base_link = 'https://zooqle.com/'
        self.search_link = '%s/search?q=%s'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            if not debrid:
                return self.sources
            search_id = clean_search(title.lower())
            start_url = '%s/search?q=%s %s' % (self.base_link, urllib.quote_plus(search_id),year)
            #print start_url+'>>>>>>>>>>>>>>>>>>>'
            self.get_source(start_url, title, year, '', '', start_time)
            
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            if not debrid:
                return self.sources
            hdlr = 'S%02dE%02d' % (int(season), int(episode))
            query = '%s+S%02dE%02d' % (urllib.quote_plus(title), int(season), int(episode))
            query = query.replace('++','')
            start_url='%ssearch?q=%s' %(self.base_link, query)
            print start_url
            self.get_source(start_url, title, show_year, season, episode, str(start_time))
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources
            
    def get_source(self,start_url,title,year,season,episode,start_time):
        try:
            print 'URL PASSED OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK'+start_url
            count = 0
            headers = {'User-Agent': client.agent()}
            r = client.request(start_url, headers=headers)
            #print r
            Endlinks=re.compile('class="text-muted3 smaller pad-l2".+?style="color:green"></i>(.+?)</span>.+?rel="nofollow" href="(.+?)".+?class="progress-bar prog-blue prog-l".+?>(.+?)</div></div>',re.DOTALL).findall(r)
            #print 'scraperchk - scrape_movie - EndLinks: '+str(Endlinks)
            for qual, Magnet, size in Endlinks:
                #print Magnet + '<><><><><>'+size
                count+=1
                self.sources.append({'source':'Torrent', 'quality':size +qual, 'scraper':self.name, 'url':Magnet, 'direct':False, 'debridonly': True})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]