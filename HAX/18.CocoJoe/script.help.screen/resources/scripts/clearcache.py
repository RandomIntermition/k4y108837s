import datetime
import glob
import os
import shutil
import sys

import xbmc
import xbmcgui

home_home = xbmc.translatePath('special://home')
home_dump = os.path.join(home_home, '*.dmp')
home_crash = os.path.join(home_home, '*.txt')

cache_cache = xbmc.translatePath('special://temp')
cache_path = os.path.join(cache_cache, '*.fi')
cache_subs = os.path.join(cache_cache, '*/*.fi')
cache_subs2 = os.path.join(cache_cache, '*/*/*.fi')

# DELETE DUMPS AND LOGS FROM HOME FOLDER

# MAIN
homedumplist=glob.glob(home_dump)
for file in homedumplist:
    os.remove(file)
# SUBS
homecrashlist=glob.glob(home_crash)
for file in homecrashlist:
    os.remove(file)


# DELETE FILES FROM TEMP CACHE FOLDER

# MAIN
cachepathlist=glob.glob(cache_path)
for file in cachepathlist:
    os.remove(file)
# SUBS
cachesubslist=glob.glob(cache_subs)
for file in cachesubslist:
    os.remove(file)

cachesubslist2=glob.glob(cache_subs2)
for file in cachesubslist2:
    os.remove(file)


xbmcgui.Dialog().ok("Complete", "Finished clearing cache")
