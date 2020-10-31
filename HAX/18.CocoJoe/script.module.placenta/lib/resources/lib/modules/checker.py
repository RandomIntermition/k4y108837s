# -*- coding: utf-8 -*-

import re,requests,urllib,urlparse,HTMLParser


def name_clean(name):
    name = HTMLParser.HTMLParser().unescape(name)
    name = name.replace('&quot;', '\"')
    name = name.replace('&amp;', '&')
    name = name.strip()
    return name

def url_clean(url):
    url = HTMLParser.HTMLParser().unescape(url)
    url = url.replace('&quot;', '\"')
    url = url.replace('&amp;', '&')
    url = url.strip()
    return url

def check_quality(quality):
    try:
        quality = quality.lower().replace('p','').replace('-',' ')
        if 'http' in quality:
            if '2160' in quality: quality = '4K'
            elif '1080' in quality: quality = '1080p'
            elif '720' in quality: quality = '720p'
            else: quality = 'SD'
        else:
            if '2160' in quality: quality = '4K'
            elif '1080' in quality: quality = '1080p'
            elif '720' in quality: quality = '720p'
            elif 'hd' in quality: quality = '720p'
            elif 'blu' in quality: quality = '720p'
            elif 'bd' in quality: quality = '720p'
            elif 'br' in quality: quality = '720p'
            elif 'dvd' in quality: quality = '720p'
            else: quality = 'SD'
        return quality
    except:
        return 'SD'


def check_site(host):
    try:
        Resolve = ['openload', 'oload', 'streamango', 'downace', 'rapidvideo', 'vidoza', 'clicknupload', 'estream',
            'vidnode', 'vidzi', 'putload', 'blazefile', 'gorillavid', 'yourupload', 'entervideo', 'youtube', 'youtu', 'vimeo',
            'vk', 'streamcherry', 'mp4upload', 'trollvid', 'vidstreaming', 'dailymotion', 'uptostream', 'uptobox',
            'vidcloud', 'vcstream', 'vidto', 'flashx', 'thevideo', 'vshare', 'vidup', 'xstreamcdn', 'vev', 'xvidstage']
        Debrid = ['1fichier', 'rapidgator', 'userscloud', 'vidlox', 'filefactory', 'turbobit', 'nitroflare']
        if host in Resolve:
            return host+'Resolve'
        elif host in Debrid:
            return host+'Debrid'
        return host
    except:
        return


def check_playable(url):
    """
checks if passed url is a live link
    :param str url: stream url
    :return: playable stream url or None
    :rtype: str or None
    """
    try:
        headers = url.rsplit('|', 1)[1]
    except:
        headers = ''
    headers = urllib.quote_plus(headers).replace('%3D', '=') if ' ' in headers else headers
    headers = dict(urlparse.parse_qsl(headers))
    result = None
    try:
        if url.startswith('http') and '.m3u8' in url:
            result = requests.head(url.split('|')[0], headers=headers, timeout=5)
            if result is None:
                return None
        elif url.startswith('http'):
            result = requests.head(url.split('|')[0], headers=headers, timeout=5)
            if result is None:
                return None
    except:
        pass
    return result

