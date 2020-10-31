import os
import xbmc
import xbmcaddon
import xbmcgui

changetxt = xbmc.translatePath('special://home/addons/script.help.screen/changelog.txt')
ochanget = open(changetxt)
changefull = ochanget.read()

xbmcgui.Dialog().textviewer('Full ChangeLog:', changefull)

