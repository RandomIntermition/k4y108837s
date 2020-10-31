from tulip.control import setting, selectDialog, lang, condVisibility
from tulip.init import *


try:
    from urllib import unquote_plus
except ImportError:
    from urllib.parse import unquote_plus

action = params.get('action')
url = params.get('url')


def pair_tool(dialog=True):

    items = [
        {
            'title': 'OpenLoad',
            'url': 'https://olpair.com/',
            'icon': 'openload.png'
        }
        ,
        {
            'title': 'TheVideo',
            'url': 'https://thevideo.cc/pair',
            'icon': 'thevideo.png'
        }
        ,
        {
            'title': 'VidUP',
            'url': 'https://vidup.me/pair',
            'icon': 'vidup.png'
        }
        ,
        {
            'title': 'Streamango',
            'url': 'https://streamango.com/pair',
            'icon': 'streamango.jpg'
        }
        ,
        {
            'title': 'FlashX',
            'url': 'https://www.flashx.tv/pairing.php',
            'icon': 'flashx.png'
        }
    ]

    for i in items:
        i.update({'action': 'pair'})

    if not dialog:

        from tulip import directory
        directory.add(items)

    else:

        choice = selectDialog([i['title'] for i in items], lang(30004))

        if choice >= 0:

            selection = [i['url'] for i in items][choice]
            pair(selection)


def pair(link):

    link = unquote_plus(link)

    if condVisibility('system.platform.android'):
        from tulip.control import android_activity
        android_activity(link)
    else:
        import webbrowser
        webbrowser.open(link)


if action is None:

    pair_tool(dialog=True if setting('dialog') == 'true' else False)

elif action == 'pair':

    pair(url)
