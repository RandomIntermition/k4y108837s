import datetime
import glob
import os
import shutil
import sys

import xbmc
import xbmcgui

packages_path = xbmc.translatePath('special://home/addons/packages')

# delete package zips

folder = packages_path
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)


xbmcgui.Dialog().ok("Complete", "Finished deleting package cache")

