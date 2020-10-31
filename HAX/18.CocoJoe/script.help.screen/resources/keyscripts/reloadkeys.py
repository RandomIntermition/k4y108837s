# use to RELOAD keymaps in kodi

import os
import xbmc
import xbmcaddon
import xbmcgui

xbmc.executebuiltin('action(reloadkeymaps)')

xbmc.executebuiltin('Notification(Helper,Controls updated,5000,special://home/addons/script.help.screen/icon.png)')
