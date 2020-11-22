# use to map HUVOP AND custom remote keys

import os
import xbmc
import xbmcaddon
import xbmcgui
from shutil import copy

hlpxml = xbmc.translatePath('special://home/addons/script.help.screen/resources/keyfiles/CustomLinux/keymap.xml')
target = xbmc.translatePath('special://home/userdata/keymaps/')

copy(hlpxml, target)

xbmc.executebuiltin('Notification(Helper,Full Controls set,5000,special://home/addons/script.help.screen/icon.png)')
