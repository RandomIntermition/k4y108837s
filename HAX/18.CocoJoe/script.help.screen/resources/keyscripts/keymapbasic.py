# use to map HP

import os
import xbmc
import xbmcaddon
import xbmcgui
from shutil import copy

hlpxml = xbmc.translatePath('special://home/addons/script.help.screen/resources/keyfiles/Basic/keymap.xml')
target = xbmc.translatePath('special://home/userdata/keymaps/')

copy(hlpxml, target)

xbmc.executebuiltin('Notification(Helper,Basic controls set,5000,special://home/addons/script.help.screen/icon.png)')
