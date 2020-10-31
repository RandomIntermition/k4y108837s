import os
import xbmc
import xbmcaddon
import xbmcgui

koditxt = xbmc.translatePath('special://home/kodi.log')
okodit = open(koditxt)
kodifull = okodit.read()

xbmcgui.Dialog().textviewer('Current Session KodiLog:', kodifull)

