# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: MuadDib

import time

from resources.lib.modules import log_utils
from resources.lib.modules import control

control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))

try:
    ModuleVersion = control.addon('script.module.placenta').getAddonInfo('version')
    AddonVersion = control.addon('plugin.video.placenta').getAddonInfo('version')
    RepoVersion = control.addon('plugin.video.placenta').getAddonInfo('version')

    log_utils.log('###############################################################', log_utils.LOGNOTICE)
    log_utils.log('### PLACENTA PLUGIN VERSION: %s ###' % str(AddonVersion), log_utils.LOGNOTICE)
    log_utils.log('### PLACENTA SCRIPT VERSION: %s ###' % str(ModuleVersion), log_utils.LOGNOTICE)
    log_utils.log('###############################################################', log_utils.LOGNOTICE)
except:
    log_utils.log('###############################################################', log_utils.LOGNOTICE)
    log_utils.log('####### ERROR GETTING PLACENTA VERSIONS  ######################', log_utils.LOGNOTICE)
    log_utils.log('###############################################################', log_utils.LOGNOTICE)

 ##### AUTO-SYNC LISTS ###########

def syncTraktLibrary():
    if control.setting('trakt.syncwatchtv') == 'true':
        control.execute('RunPlugin(plugin://%s)' % 'plugin.video.placenta/?action=tvshowsToLibrarySilent&url=traktwatchlist')
        
    if control.setting('trakt.syncwatchmovie') == 'true':
        control.execute('RunPlugin(plugin://%s)' % 'plugin.video.placenta/?action=moviesToLibrarySilent&url=traktwatchlist')
        
    if control.setting('trakt.synccollecttv') == 'true':
        control.execute('RunPlugin(plugin://%s)' % 'plugin.video.placenta/?action=tvshowsToLibrarySilent&url=traktcollection')
        
    if control.setting('trakt.synccollectmovie') == 'true':
        control.execute('RunPlugin(plugin://%s)' % 'plugin.video.placenta/?action=moviesToLibrarySilent&url=traktcollection')

    if control.setting('trakt.syncandupdate') == 'true' and not control.condVisibility('Library.IsScanningVideo') and not control.condVisibility('Player.HasVideo'):
        time.sleep(20)
        control.execute('UpdateLibrary(video)')


if control.setting('trakt.synctrakt') == 'true':
    time.sleep(10)
    syncTraktLibrary()

if int(control.setting('trakt.syncschedTime')) > 0:
    log_utils.log('#################### STARTING TRAKT SCHEDULING ################', log_utils.LOGNOTICE)
    log_utils.log('#################### SCHEDULED TIME FRAME '+ control.setting('trakt.syncschedTime')  + ' HOURS ################', log_utils.LOGNOTICE)
    timeout = 3600 * int(control.setting('trakt.syncschedTime'))
    schedTrakt = threading.Timer(timeout, syncTraktLibrary)
    schedTrakt.start()


