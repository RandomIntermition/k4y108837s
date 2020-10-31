# -*- coding: utf-8 -*-
# LambdaScrapers Cleanup Service

import os
import re

import xbmc
import xbmcvfs
import xbmcaddon

from lib.lambdascrapers import getAllHosters
from lib.lambdascrapers import providerSources


#############   THIS IS PERSONAL VERSION  #############################
'''
Temporary service to TRY to make some file changes, and then prevent itself from running again.
'''

ADDON = xbmcaddon.Addon()

# 1) Delete OLD settings file. (commented out set provider default, as not needed)
try:
    profileFolderPath = xbmc.translatePath(ADDON.getAddonInfo('profile')).decode('utf-8')
    settingsPath = os.path.join(profileFolderPath, 'settings.xml')

    if xbmcvfs.exists(settingsPath):
        os.remove(settingspath)
    # Reset obsolete module providers to Lambdascrapers.
    #elif ADDON.getSetting('module.provider') not in providerSources():
    #    ADDON.setSetting('module.provider', ' Lambdascrapers')
    else:pass
    
except:
    pass


# 2) Remove the service from 'addon.xml'.
try:
    addonFolderPath = xbmc.translatePath(ADDON.getAddonInfo('path')).decode('utf-8')
    addonXMLPath = os.path.join(addonFolderPath, 'addon.xml')

    # Disabling is done by commenting out the XML line with the service extension so it doesn't run anymore.
    with open(addonXMLPath, 'r+') as addonXMLFile:
        xmlText = addonXMLFile.read()
        serviceFilename = 'CleanupService\.py'
        pattern = r'(<\s*?extension.*?' + serviceFilename + '.*?>)'
        updatedXML = re.sub(pattern, r'<!--  \1  -->', xmlText, count=1, flags=re.IGNORECASE)
        addonXMLFile.seek(0)
        addonXMLFile.write(updatedXML)
        addonXMLFile.truncate()
except:
    pass
