import datetime
import glob
import os
import shutil
import sys

import xbmc
import xbmcgui

packages_path = xbmc.translatePath('special://home/addons/packages')

# delete package zips

for root, dirs, files in os.walk(packages_path):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))


xbmcgui.Dialog().ok("Complete", "Finished deleting package cache")

