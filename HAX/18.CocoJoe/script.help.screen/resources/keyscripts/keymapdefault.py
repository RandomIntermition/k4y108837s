# use to REMOVE ALL CUSTOM KEYS

import os
import xbmc
import xbmcaddon
import xbmcgui

keyxml = xbmc.translatePath('special://home/userdata/keymaps/keymap.xml')

os.remove(keyxml)

xbmc.executebuiltin('Notification(Helper,Default controls restored,5000,special://home/addons/script.help.screen/icon.png)')
