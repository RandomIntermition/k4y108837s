# -*- coding: utf-8 -*-

import glob
import os
import re
import traceback

import xbmc
import xbmcgui
import xbmcaddon

from xbmc import (LOGDEBUG, LOGERROR, LOGFATAL, LOGINFO,
                  LOGNONE, LOGNOTICE, LOGSEVERE, LOGWARNING)

'''
Temporary service to create new settings after each update
then prevent itself from running again.
prevents consecutive runs using both, remove in addon xml, and exit if version is the same as last run
'''

#############   ID SETTINGS AND ADDON (generic)  ###############

addon_name = 'Lambdascrapers Module'
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
addon_path = xbmc.translatePath(('special://home/addons/script.module.lambdascrapers')).decode('utf-8')
module_path = xbmc.translatePath(('special://home/addons/script.module.lambdascrapers')).decode('utf-8')

lambda_ver = xbmcaddon.Addon(id='script.module.lambdascrapers').getAddonInfo('version')
lambda_lastcheck = xbmcaddon.Addon(id='script.module.lambdascrapers').getSetting('module.vers')

if str(lambda_ver) == str(lambda_lastcheck):
    exit()

#############   DEFINE FUNCTIONS  ###############

def openfile(path_to_the_file):
    try:
        fh = open(path_to_the_file, 'rb')
        contents = fh.read()
        fh.close()
        return contents
    except Exception:
        failure = traceback.format_exc()
        print('Service Open File Exception - %s \n %s' % (path_to_the_file, str(failure)))
        return None


def savefile(path_to_the_file, content):
    try:
        fh = open(path_to_the_file, 'wb')
        fh.write(content)
        fh.close()
    except Exception:
        failure = traceback.format_exc()
        print('Service Save File Exception - %s \n %s' % (path_to_the_file, str(failure)))
        exit()


#############   LIST INDEPENDENT SETTINGS TO ADD  ###############
### (THREE ids need to be changed per set) ###

### nofity of update ###
xbmcgui.Dialog().notification(addon_name, 'Generating scraper details', addon_icon)


##### PREMIUM ####
## DEBRID ONLY
settings_xml_path = os.path.join(addon_path, 'resources/settings.xml')
scraper_path = os.path.join(module_path, 'lib/lambdascrapers/only_premium/Debrid')
try:
    xml = openfile(settings_xml_path)
except Exception:
    failure = traceback.format_exc()
    exit()

new_settings = []
new_settings = '<setting label="Debrid only" type="lsep" />\n'
for file in glob.glob("%s/*.py" % (scraper_path)):
    file = os.path.basename(file)
    if '__init__' not in file:
        file = file.replace('.py', '')
        new_settings += '        <setting id="provider.%s" type="bool" label="%s" default="false" />\n' % (
            file.lower(), file.upper())

xml = openfile(settings_xml_path)
xml = xml.replace('<setting label="Debrid only" type="lsep" />', str(new_settings))
savefile(settings_xml_path, xml)


################# PREMIUM END, KEEP TOP TO AVOID INCORRECT DEFAULTS #######################



##### QUICK ####
## CHECKED
settings_xml_path = os.path.join(addon_path, 'resources/settings.xml')
scraper_path = os.path.join(module_path, 'lib/lambdascrapers/sources_quick/checked')
try:
    xml = openfile(settings_xml_path)
except Exception:
    failure = traceback.format_exc()
    exit()

new_settings = []
new_settings = '<setting label="Quick (Checked)" type="lsep" />\n'
for file in glob.glob("%s/*.py" % (scraper_path)):
    file = os.path.basename(file)
    if '__init__' not in file:
        file = file.replace('.py', '')
        new_settings += '        <setting id="provider.%s" type="bool" label="%s" default="true" />\n' % (
            file.lower(), file.upper())

xml = openfile(settings_xml_path)
xml = xml.replace('<setting label="Quick (Checked)" type="lsep" />', str(new_settings))
savefile(settings_xml_path, xml)

## UNCHECKED
settings_xml_path = os.path.join(addon_path, 'resources/settings.xml')
scraper_path = os.path.join(module_path, 'lib/lambdascrapers/sources_quick/unchecked')
try:
    xml = openfile(settings_xml_path)
except Exception:
    failure = traceback.format_exc()
    exit()

new_settings = []
new_settings = '<setting label="Quick (unchecked)" type="lsep" />\n'
for file in glob.glob("%s/*.py" % (scraper_path)):
    file = os.path.basename(file)
    if '__init__' not in file:
        file = file.replace('.py', '')
        new_settings += '        <setting id="provider.%s" type="bool" label="%s" default="true" />\n' % (
            file.lower(), file.upper())

xml = openfile(settings_xml_path)
xml = xml.replace('<setting label="Quick (unchecked)" type="lsep" />', str(new_settings))
savefile(settings_xml_path, xml)


##### SCRUBS ####
## EN
settings_xml_path = os.path.join(addon_path, 'resources/settings.xml')
scraper_path = os.path.join(module_path, 'lib/lambdascrapers/sources_scrubs/en')
try:
    xml = openfile(settings_xml_path)
except Exception:
    failure = traceback.format_exc()
    exit()

new_settings = []
new_settings = '<setting label="Scrubs (en)" type="lsep" />\n'
for file in glob.glob("%s/*.py" % (scraper_path)):
    file = os.path.basename(file)
    if '__init__' not in file:
        file = file.replace('.py', '')
        new_settings += '        <setting id="provider.%s" type="bool" label="%s" default="true" />\n' % (
            file.lower(), file.upper())

xml = openfile(settings_xml_path)
xml = xml.replace('<setting label="Scrubs (en)" type="lsep" />', str(new_settings))
savefile(settings_xml_path, xml)

## DE
## ES
## FR
## GR
## KO
## PL
## RU




##### TEMPLATE ####
## EN
## DE
## ES
## GR
## PL




#############   FINALIZE  ###############

#########   update version ID to prevent launch until next update  ###########

xbmcaddon.Addon(id='script.module.lambdascrapers').setSetting('module.vers', str(lambda_ver))

#####   double-tap remove service from addon xml to prevent launch  ######

try:
    # addonFolderPath = xbmc.translatePath(ADDON.getAddonInfo('path')).decode('utf-8')
    addonXMLPath = os.path.join(addon_path, 'addon.xml')

    # Disabling is done by commenting out the XML line for the service extension so it doesn't run anymore.
    with open(addonXMLPath, 'r+') as addonXMLFile:
        xmlText = addonXMLFile.read()
        serviceFilename = 'ManifestSettings\.py'
        pattern = r'(<\s*?extension.*?' + serviceFilename + '.*?>)'
        updatedXML = re.sub(pattern, r'<!--  \1  -->', xmlText, count=1, flags=re.IGNORECASE)
        addonXMLFile.seek(0)
        addonXMLFile.write(updatedXML)
        addonXMLFile.truncate()
except:
    pass

### notify of update (COMPLETE) ###
xbmcgui.Dialog().notification(addon_name, 'Scraper settings updated', addon_icon)




