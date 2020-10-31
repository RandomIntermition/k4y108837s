# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 03-21-2019 by JewBMX in Scrubs.

import os.path

files = os.listdir(os.path.dirname(__file__))
__all__ = [filename[:-3] for filename in files if not filename.startswith('__') and filename.endswith('.py')]

###Dev Shit.
# TIP = '(this is fake and just a lazy way to force a scraper to not run lol.)'
# if test.status() is False: raise Exception()

# from resources.lib.modules import cfscrape
# self.scraper = cfscrape.create_scraper()
# r = self.scraper.get(url).content

# import xbmcgui
# TIP = '(name as in you name it.)'
# xbmcgui.Dialog ().textviewer ("data",str (name))
# xbmcgui.Dialog ().textviewer ("data",str (info))

# from resources.lib.modules import log_utils
# log_utils.log('---Scraper Testing - Sources - host: ' + str(host))
# log_utils.log('---Scraper Testing - Sources - quality: ' + str(quality))
# log_utils.log('---Scraper Testing - Sources - info: ' + str(info))
# log_utils.log('---Scraper Testing - Sources - url: ' + str(url))

