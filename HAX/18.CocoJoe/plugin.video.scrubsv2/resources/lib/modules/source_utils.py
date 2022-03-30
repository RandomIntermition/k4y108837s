# -*- coding: utf-8 -*-

import re

from kodi_six import xbmc
import six
from six.moves import urllib_parse

from resources.lib.modules import client
from resources.lib.modules import trakt


def append_headers(headers):
    return '|%s' % '&'.join(['%s=%s' % (key, urllib_parse.quote_plus(headers[key])) for key in headers])


def supported_video_extensions():
    supported_video_extensions = xbmc.getSupportedMedia('video').split('|')
    return [i for i in supported_video_extensions if i != '' and i != '.zip']


def is_anime(content, type, type_id):
    try:
        r = trakt.getGenre(content, type, type_id)
        return 'anime' in r or 'animation' in r
    except:
        return False


def aliases_to_array(aliases, filter=None):
    try:
        if not filter:
            filter = []
        if isinstance(filter, six.string_types):
            filter = [filter]
        return [x.get('title') for x in aliases if not filter or x.get('country') in filter]
    except:
        return []


def strip_domain(url):
    try:
        url = six.ensure_str(url)
        if url.lower().startswith('http') or url.startswith('/'):
            url = re.findall('(?://.+?|)(/.+)', url)[0]
        url = client.replaceHTMLCodes(url)
        return url
    except:
        return


def __top_domain(url):
    if not (url.startswith('//') or url.startswith('http://') or url.startswith('https://')):
        url = '//' + url
    elements = urllib_parse.urlparse(url)
    domain = elements.netloc or elements.path
    domain = domain.split('@')[-1].split(':')[0]
    regex = "(?:www\.)?([\w\-]*\.[\w\-]{2,3}(?:\.[\w\-]{2,3})?)$"
    res = re.search(regex, domain)
    if res:
        domain = res.group(1)
    domain = domain.lower()
    return domain


def is_host_valid(url, domains):
    try:
        host = __top_domain(url)
        hosts = [domain.lower() for domain in domains if host and host in domain.lower()]
        if hosts and '.' not in host:
            host = hosts[0]
        if hosts and any([h for h in ['google', 'picasa', 'blogspot'] if h in host]):
            host = 'gvideo'
        if hosts and any([h for h in ['akamaized', 'ocloud'] if h in host]):
            host = 'CDN'
        return any(hosts), host
    except:
        return False, ''


def get_host(url):
    try:
        elements = urllib_parse.urlparse(url)
        domain = elements.netloc or elements.path
        domain = domain.split('@')[-1].split(':')[0]
        res = re.search("(?:www\.)?([\w\-]*\.[\w\-]{2,3}(?:\.[\w\-]{2,3})?)$", domain)
        if res:
            domain = res.group(1)
        domain = domain.lower()
    except:
        elements = urllib_parse.urlparse(url)
        host = elements.netloc
        domain = host.replace('www.', '')
    return domain


def checkHost(url, hostList):
    host = get_host(url)
    validHost = False
    for i in hostList:
        if i.lower() in url.lower():
            host = i
            validHost = True
            return validHost, host
    return validHost, host


def get_release_quality(release_name, release_link=None):
    if release_name is None:
        return
    try:
        release_name = six.ensure_str(release_name)
    except:
        pass
    try:
        quality = None
        release_name = release_name.upper()
        fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', release_name)
        fmt = re.split('\.|\(|\)|\[|\]|\s|-', fmt)
        fmt = [i.lower() for i in fmt]
        if '4k' in fmt:
            quality = '4K'
        elif '2160p' in fmt:
            quality = '4K'
        elif '2160' in fmt:
            quality = '4K'
        elif '1080p' in fmt:
            quality = '1080p'
        elif '1080' in fmt:
            quality = '1080p'
        elif '720p' in fmt:
            quality = '720p'
        elif '720' in fmt:
            quality = '720p'
        elif 'brrip' in fmt:
            quality = '720p'
        elif 'hdtv' in fmt:
            quality = '720p'
        elif 'hd' in fmt:
            quality = '720p'
        elif 'bluray' in fmt:
            quality = '720p'
        elif 'webrip' in fmt:
            quality = '720p'
        elif '480p' in fmt:
            quality = '480p'
        elif '480' in fmt:
            quality = '480p'
        elif any(i in ['dvdscr', 'r5', 'r6'] for i in fmt):
            quality = 'SCR'
        elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in fmt):
            quality = 'CAM'
        if not quality:
            if release_link:
                release_link = release_link.lower()
                try:
                    release_link = six.ensure_str(release_link)
                except:
                    pass
                if '4k' in release_link:
                    quality = '4K'
                elif '2160' in release_link:
                    quality = '4K'
                elif '1080' in release_link:
                    quality = '1080p'
                elif '720' in release_link:
                    quality = '720p'
                elif 'hd' in release_link:
                    quality = '720p'
                else:
                    if any(i in ['dvdscr', 'r5', 'r6'] for i in release_link):
                        quality = 'SCR'
                    elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in release_link):
                        quality = 'CAM'
                    else:
                        quality = 'SD'
            else:
                quality = 'SD'
        info = []
        if '3d' in fmt or '.3D.' in release_name:
            info.append('3D')
        if any(i in ['hevc', 'h265', 'x265'] for i in fmt):
            info.append('HEVC')
        return quality, info
    except:
        return 'SD', []


def getFileType(url):
    try:
        url = six.ensure_str(url)
        url = client.replaceHTMLCodes(url)
        url = urllib_parse.unquote(url)
        url = url.lower()
        url = re.sub('[^a-z0-9 ]+', ' ', url)
    except:
        url = str(url)
    type = ''
    if 'bluray' in url:
        type += ' BLURAY /'
    if '.web-dl' in url:
        type += ' WEB-DL /'
    if '.web.' in url:
        type += ' WEB-DL /'
    if 'hdrip' in url:
        type += ' HDRip /'
    if 'bd-r' in url:
        type += ' BD-R /'
    if 'bd-rip' in url:
        type += ' BD-RIP /'
    if 'bd.r' in url:
        type += ' BD-R /'
    if 'bd.rip' in url:
        type += ' BD-RIP /'
    if 'bdr' in url:
        type += ' BD-R /'
    if 'bdrip' in url:
        type += ' BD-RIP /'
    if 'atmos' in url:
        type += ' ATMOS /'
    if 'truehd' in url:
        type += ' TRUEHD /'
    if '.dd' in url:
        type += ' DolbyDigital /'
    if '5.1' in url:
        type += ' 5.1 /'
    if '.xvid' in url:
        type += ' XVID /'
    if '.mp4' in url:
        type += ' MP4 /'
    if '.avi' in url:
        type += ' AVI /'
    if 'ac3' in url:
        type += ' AC3 /'
    if 'h.264' in url:
        type += ' H.264 /'
    if '.x264' in url:
        type += ' x264 /'
    if '.x265' in url:
        type += ' x265 /'
    if 'subs' in url: 
        if type != '':
            type += ' - WITH SUBS'
        else:
            type = 'SUBS'
    type = type.rstrip('/')
    return type


