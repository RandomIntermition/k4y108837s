import datetime
import glob
import os
import shutil
import sys

import xbmc
import xbmcgui

# delete ONLY subdirs from thumbnails folder

thumbpath_path = xbmc.translatePath('special://thumbnails')

folder = thumbpath_path
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print(e)


xbmcgui.Dialog().ok("Deleting Thumbnails...", "[COLOR red]Warning![/COLOR]",
                    "(This may take 1-2mins)",
                    "[Kodi may run slowly until thumbnails have been 're-cached']")

