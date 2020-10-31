# -*- coding: UTF-8 -*-


def get():
    import os, xbmcgui
    from resources.lib.modules import control
    changelogfile = os.path.join(control.addonPath, 'changelog.txt')
    r = open(changelogfile)
    text = r.read()
    id = 10147
    control.execute('ActivateWindow(%d)' % id)
    control.sleep(500)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            control.sleep(10)
            retry -= 1
            win.getControl(1).setLabel('--[ [COLOR darkorange] v%s [/COLOR]ChangeLog ]--' %(control.addonInfo('version')))
            win.getControl(5).setText(text)
            return
        except:
            pass


def get(version):
    try:
        import xbmc,xbmcgui,xbmcaddon,xbmcvfs

        f = xbmcvfs.File(xbmcaddon.Addon().getAddonInfo('changelog'))
        text = f.read() ; f.close()

        label = '%s - %s' % (xbmc.getLocalizedString(24054), xbmcaddon.Addon().getAddonInfo('name'))

        id = 10147

        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(100)

        win = xbmcgui.Window(id)

        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                win.getControl(1).setLabel(label)
                win.getControl(5).setText(text)
                retry = 0
            except:
                retry -= 1

        return '1'
    except:
        return '1'


