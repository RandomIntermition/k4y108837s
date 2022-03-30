# -*- coding: utf-8 -*-

import re
import requests

import simplejson as json
from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import jsunpack
from resources.lib.modules import source_utils
from resources.lib.modules import log_utils


"""Example...

from resources.lib.modules import scrape_sources
for source in scrape_sources.process(url, hostDict):
    sources.append(source)

scrape_sources.rescrape(url)

scrape_sources.prepare_link(url)

"""


def prepare_link(url):
    if not url:
        return
    url = "https:" + url if url.startswith('//') else url
    if 'doodstream.com' in url:
        url = url.replace('doodstream.com', 'dood.watch')
    if 'dood.so' in url:
        url = url.replace('dood.so', 'dood.la')
    if 'dood.to' in url:
        url = url.replace('dood.to', 'dood.ws')
    if 'eplayvid.com' in url:
        url = url.replace('eplayvid.com', 'eplayvid.net')
    if 'gomostream.com' in url:
        url = url.replace('gomostream.com', 'gomo.to')
    if 'sendit.cloud' in url:
        url = url.replace('sendit.cloud', 'send.cm')
    if 'vidcloud.icu' in url:
        url = url.replace('vidcloud.icu', 'vidembed.io')
    if 'vidcloud9.com' in url:
        url = url.replace('vidcloud9.com', 'vidembed.io')
    if 'vidembed.cc' in url:
        url = url.replace('vidembed.cc', 'vidembed.io')
    if 'vidnext.net' in url:
        url = url.replace('vidnext.net', 'vidembed.me')
    if 'vidoza.net' in url:
        url = url.replace('vidoza.net', 'vidoza.co')
    #log_utils.log('scrape_sources - prepare_link link: ' + str(url))
    return url


def rescrape(url): # unused old code saved.
    try:
        html = client.scrapePage(url).text
        link = re.findall(r'(?:file|source)(?:\:)\s*(?:\"|\')(.+?)(?:\"|\')', html)[0]
        return link
    except:
        #log_utils.log('rescrape', 1)
        return url


def process(hostDict, link, host=None, info=None):
    sources = []
    try:
        if not link:
            return sources
        link = prepare_link(link)
        host = link if host == None else host
        info = link if info == None else info
        #if 'google' in link:
            #link = googlestream.googlepass(link)
        if 'linkbin.me' in host:
            for source in linkbin(link, hostDict):
                sources.append(source)
        elif any(i in host for i in ['gomo.to', 'gomostream.com', 'gomoplayer.com']):
            for source in gomo(link, hostDict):
                sources.append(source)
        elif any(i in host for i in ['database.gdriveplayer.us', 'databasegdriveplayer.co', 'series.databasegdriveplayer.co']):
            for source in gdriveplayer(link, hostDict):
                sources.append(source)
        elif 'vidlink.org' in host:
            for source in vidlink(link, hostDict):
                sources.append(source)
        elif any(i in host for i in ['vidembed.me', 'vidembed.io', 'vidembed.cc', 'vidcloud9.com']):
            for source in vidembed(link, hostDict):
                sources.append(source)
        elif 'voxzer.org' in host:
            for source in voxzer(link, hostDict):
                sources.append(source)
        elif '2embed.ru' in host:
            for source in twoembed(link, hostDict):
                sources.append(source)
        else:
            valid, host = source_utils.is_host_valid(host, hostDict)
            if valid:
                quality, info = source_utils.get_release_quality(link, info)
                sources.append({'source': host, 'quality': quality, 'info': info, 'url': link, 'direct': False})
        return sources
    except Exception:
        #log_utils.log('process', 1)
        return sources


def linkbin(link, hostDict):
    sources = []
    try:
        html = client.scrapePage(link).text
        urls = re.findall('<li class="signle-link"><a href="(.+?)" target="_blank">', html)
        for url in urls:
            url = prepare_link(url)
            valid, host = source_utils.is_host_valid(url, hostDict)
            if valid:
                quality, info = source_utils.get_release_quality(url, url)
                sources.append({'source': host, 'quality': quality, 'info': info, 'url': url, 'direct': False})
        return sources
    except Exception:
        #log_utils.log('linkbin', 1)
        return sources


def gomo(link, hostDict):
    sources = []
    try:
        domain = re.findall('(?://|\.)(gomo\.to|gomostream\.com|gomoplayer\.com)/', link)[0]
        gomo_link = 'https://%s/decoding_v3.php' % domain
        result = client.request(link)
        tc = re.compile('tc = \'(.+?)\';').findall(result)[0]
        if (tc):
            token = re.compile('"_token": "(.+?)",').findall(result)[0]
            post = {'tokenCode': tc, '_token': token}
            def tsd(tokenCode):
                _13x48X = tokenCode
                _71Wxx199 = _13x48X[4:18][::-1]
                return _71Wxx199 + "18" + "432782"
            headers = {'Host': domain, 'Referer': link, 'User-Agent': client.UserAgent, 'x-token': tsd(tc)}
            urls = client.request(gomo_link, XHR=True, post=post, headers=headers, output='json')
            for url in urls:
                if not url:
                    continue
                url = prepare_link(url)
                headers = {'User-Agent': client.UserAgent, 'Referer': url}
                if 'gomo.to' in url:
                    url = client.request(url, headers=headers, output='geturl')
                    if not url:
                        continue
                    if 'gomoplayer.com' in url:
                        html = client.request(url, headers=headers)
                        unpacked = client.unpacked(html)
                        links = re.compile('file:"(.+?)"').findall(unpacked)
                        for link in links:
                            if '/srt/' in link:
                                continue
                            info = 'MP4' if link.endswith('.mp4') else 'm3u8'
                            link += '|%s' % urlencode({'Referer': url})
                            sources.append({'source': 'gomoplayer', 'quality': 'SD', 'info': info, 'url': link, 'direct': True})
                    elif any(i in url for i in ['database.gdriveplayer.us', 'databasegdriveplayer.co', 'series.databasegdriveplayer.co']):
                        for source in gdriveplayer(url, hostDict):
                            sources.append(source)
                    else:
                        valid, host = source_utils.checkHost(url, hostDict)
                        quality, info = source_utils.get_release_quality(url, url)
                        sources.append({'source': host, 'quality': quality, 'url': url, 'info': info, 'direct': False})
                        #sources.append({'source': 'gomo', 'quality': 'SD', 'url': url, 'direct': True})
                else:
                    valid, host = source_utils.checkHost(url, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(url, url)
                        sources.append({'source': host, 'quality': quality, 'url': url, 'info': info, 'direct': False})
        return sources
    except Exception:
        #log_utils.log('gomo', 1)
        return sources


def gdriveplayer(link, hostDict):
    sources = []
    try:
        html = client.scrapePage(link).text
        servers = client.parseDOM(html, 'ul', attrs={'class': 'list-server-items'})[0]
        urls = client.parseDOM(servers, 'a', ret='href')
        for url in urls:
            if not url or url.startswith('/player.php'):
                continue
            url = prepare_link(url)
            valid, host = source_utils.is_host_valid(url, hostDict)
            if valid:
                quality, info = source_utils.get_release_quality(url, url)
                sources.append({'source': host, 'quality': quality, 'info': info, 'url': url, 'direct': False})
        return sources
    except Exception:
        #log_utils.log('gdriveplayer', 1)
        return sources


def vidembed(link, hostDict):
    sources = []
    try:
        try:
            html = client.scrapePage(link).text
            urls = client.parseDOM(html, 'li', ret='data-video')
            if urls:
                for url in urls:
                    url = prepare_link(url)
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(url, url)
                        sources.append({'source': host, 'quality': quality, 'info': info, 'url': url, 'direct': False})
        except:
            pass
        valid, host = source_utils.is_host_valid(link, hostDict)
        if valid:
            quality, info = source_utils.get_release_quality(link, link)
            sources.append({'source': host, 'quality': quality, 'info': info, 'url': link, 'direct': False})
        return sources
    except Exception:
        #log_utils.log('vidembed', 1)
        return sources


def vidlink(link, hostDict):
    sources = []
    try:
        return sources # site for update_views bit needs cfscrape so the links are trash.
        # return sources is added to cock block the urls from being seen lol.
        postID = link.split('/embed/')[1]
        post_link = 'https://vidlink.org/embed/update_views'
        payload = {'postID': postID}
        headers = {'User-Agent': client.UserAgent, 'Referer': link}
        headers['X-Requested-With'] = 'XMLHttpRequest'
        ihtml = client.request(post_link, post=payload, headers=headers)
        if ihtml:
            linkcode = client.unpacked(ihtml)
            linkcode = linkcode.replace('\\', '')
            links = re.findall(r'var file1="(.+?)"', linkcode)[0]
            stream_link = links.split('/pl/')[0]
            headers = {'Referer': 'https://vidlink.org/', 'User-Agent': client.UserAgent}
            response = client.request(links, headers=headers)
            urls = re.findall(r'[A-Z]{10}=\d+x(\d+)\W[A-Z]+=\"\w+\"\s+\/(.+?)\.', response)
            if urls:
                for qual, url in urls:
                    url = stream_link + '/' + url + '.m3u8'
                    #log_utils.log('scrape_sources - process vidlink link: ' + str(url))
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(qual, url)
                        sources.append({'source': host, 'quality': quality, 'info': info, 'url': url, 'direct': False})
        return sources
    except Exception:
        #log_utils.log('vidlink', 1)
        return sources


def twoembed(link, hostDict):
    sources = []
    items = []
    try:
        return sources # site has changed and havent fixed this yet so the links are trash.
        # return sources is added to cock block the urls from being seen lol.
        r = client.request(link, headers={'User-Agent': client.UserAgent, 'Referer': link})
        r = re.compile('data-id="(.+?)">.+?</a>').findall(r)
        r = [i for i in r]
        items += r
        for item in items:
            item = 'https://www.2embed.ru/ajax/embed/play?id=%s&_token=' % item
            url = client.request(item, headers={'User-Agent': client.UserAgent, 'Referer': item})
            url = re.findall('"link":"(.+?)","sources"', url)
            for url in url:
                if 'vidcloud.pro' in url:
                    r = client.request(url, headers={'User-Agent': client.UserAgent, 'Referer': url})
                    r = re.findall('sources = \[{"file":"(.+?)","type"', r)[0]
                    r = r.replace('\\', '')
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    quality, info = source_utils.get_release_quality(url, url)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': r, 'direct': False, 'debridonly': False})
                else:
                    url = prepare_link(url)
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(url, url)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
        return sources
    except Exception:
        #log_utils.log('twoembed', 1)
        return sources


def voxzer(link, hostDict):
    sources = []
    try:
        link = link.replace('/view/', '/list/')
        html = client.scrapePage(link).json()
        url = html['link']
        url += '|%s' % urlencode({'Referer': link})
        valid, host = source_utils.is_host_valid(url, hostDict)
        sources.append({'source': host, 'quality': 'HD', 'url': url, 'direct': True})
        return sources
    except Exception:
        #log_utils.log('voxzer', 1)
        return sources


