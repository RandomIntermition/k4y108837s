import datetime
import glob
import os
import shutil
import sys

import xbmc
import xbmcgui

# delete ONLY zipz from packages folder

packages_path = os.path.join(xbmc.translatePath('special://home/addons/packages'), '*.zip')
packages_subs = os.path.join(xbmc.translatePath('special://home/addons/packages'), '*/*.zip')

packagepathlist=glob.glob(packages_path)
for file in packagepathlist:
    os.remove(file)

packagepathsub=glob.glob(packages_subs)
for file in packagepathsub:
    os.remove(file)

xbmcgui.Dialog().ok("Deleting Packages...", "[COLOR red]Warning![/COLOR]",
                    "(This may take 1-2mins)",
                    "[ONLY Zip Archives have been deleted, NOT actual add-ons]")
