# -*- coding: UTF-8 -*-
'''
    openloadmovie scraper for Exodus forks.
    Nov 9 2018 - Checked
    Oct 10 2018 - Cleaned and Checked

    Updated and refactored by someone.
    Originally created by others.
'''
import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy
# openloadmovies.ch opens to openloadmovie.org always.
# could remove it but o well it can go down first.

class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['openloadmovie.org','openloadmovies.ch']
		self.base_link = 'https://openloadmovies.ch'

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			title = cleantitle.geturl(title)
			url = self.base_link + '/movies/%s-%s' % (title,year)
			return url
		except:
			return
			
	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			r = client.request(url)
			match = re.compile('<iframe class="metaframe rptss" src="(.+?)"').findall(r)
			for url in match: 
				sources.append({'source': 'Openload','quality': 'HD','language': 'en','url': url,'direct': False,'debridonly': False})
		except Exception:
			return
		return sources

	def resolve(self, url):
		return url
