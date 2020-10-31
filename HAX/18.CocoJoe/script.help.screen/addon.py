import os
import xbmc
import xbmcaddon
import xbmcgui
 
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addonInfo   = xbmcaddon.Addon().getAddonInfo
addonPath   = xbmc.translatePath(addonInfo('path'))
addonversion = addon.getAddonInfo('version')
changetxt = os.path.join(addonPath, 'changelog.txt')
ochanget = open(changetxt)
changefull = ochanget.read()

# BASIC
phelpbasic = os.path.join(addonPath, 'helpfiles/helpbasic.txt')
ohelpbasic = open(phelpbasic)
vhelpbasic = ohelpbasic.read()

# PLAYBACK
phelpplayback = os.path.join(addonPath, 'helpfiles/helpplayback.txt')
ohelpplayback = open(phelpplayback)
vhelpplayback = ohelpplayback.read()

# PLAYBACK SETTING
phelpplaysetting = os.path.join(addonPath, 'helpfiles/helpplaysetting.txt')
ohelpplaysetting = open(phelpplaysetting)
vhelpplaysetting = ohelpplaysetting.read()

# SPECIAL
phelpspecial = os.path.join(addonPath, 'helpfiles/helpspecial.txt')
ohelpspecial = open(phelpspecial)
vhelpspecial = ohelpspecial.read()

# ALL
phelpall = os.path.join(addonPath, 'helpfiles/helpall.txt')
ohelpall = open(phelpall)
vhelpall = ohelpall.read()

TERMS = ['[COLOR blue]Select a Category:[/COLOR]',
         '    - Basic Controls',
         '    - Playback Controls',
         '    - Playback Settings',
         '[COLOR gold]    - Special keys[/COLOR]',
         '',
         '',
         '[View All]',
         '[COLOR darkred]Close[/COLOR]']
dialog = xbmcgui.Dialog()
selected = dialog.select('Help Guide: ' + addonversion, TERMS)
picked = TERMS[selected]

if picked == '    - Basic Controls':
    xbmcgui.Dialog().textviewer(addonname, vhelpbasic)

if picked == '    - Playback Controls':
    xbmcgui.Dialog().textviewer(addonname, vhelpplayback)

if picked == '    - Playback Settings':
    xbmcgui.Dialog().textviewer(addonname, vhelpplaysetting)

if picked == '[COLOR gold]    - Special keys[/COLOR]':
    xbmcgui.Dialog().textviewer(addonname, vhelpspecial)

if picked == '[View All]':
    xbmcgui.Dialog().textviewer('View All Controls', vhelpall)

# 'on exit' dialog
if picked == '[COLOR darkred]Close[/COLOR]':
    xbmcgui.Dialog().notification(addonname, 'help closed', xbmcgui.NOTIFICATION_INFO, 1000)
